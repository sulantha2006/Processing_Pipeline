#!/home/sulantha/anaconda3/bin/python
__author__ = 'Sulantha'
import argparse
import sys
sys.path.append('/home/sulantha/PycharmProjects/Processing_Pipeline')
from Utils.DbUtils import DbUtils
from Config import CoregConfig
import os, subprocess, signal
import getpass
import hashlib
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('-s','--study', help='Study name. ', choices=['adni'])
parser.add_argument('-t','--type', help='The type of pet. ', choices=['av45', 'fdg'])
parser.add_argument('-u','--user', help='Username ')
parser.add_argument('--createUser', help=argparse.SUPPRESS)
args = parser.parse_args()

DBClient = DbUtils()
currentRec = None

DBClient = DbUtils()
currentRec = None

xfmFile = '1.xfm'
tagFile = '1.tag'


def runCoreg(study, type, username):
    while 1:
        getEntrySql = "SELECT * FROM Coregistration WHERE TYPE = '{0}' AND STUDY = '{1}' AND SKIP = 0 AND START = 0 AND END = 0 LIMIT 1".format(type, study)
        resT = DBClient.executeAllResults(getEntrySql)
        if len(resT) < 1:
            print('No files to coregister. ')
            break
        res = resT[0]
        recID = res[0]
        global currentRec
        currentRec = recID
        setStartSql = "UPDATE Coregistration SET START = 1, USER = '{1}' WHERE RECORD_ID = '{0}'".format(recID, username)
        DBClient.executeNoResult(setStartSql)

        petPath  = res[4]
        t1Path = res[5]
        petScanType = res[6]
        t1ScanType = res[7]
        regCMD = 'register {0}/*_{2}.mnc {1}/*_{3}.mnc'.format(petPath, t1Path, petScanType, t1ScanType)
        subprocess.Popen(regCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/bin/sh').wait()

        if os.path.exists(xfmFile) and os.path.exists(tagFile):
            xfmName = res[8]
            try:
                invCMD = 'xfminvert {0} {1}/{2}.xfm'.format(xfmFile, CoregConfig.MANUAL_XFM_FOLDER, xfmName)
                subprocess.Popen(invCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/bin/sh').wait()
                shutil.move(tagFile, '{0}/{1}.tag'.format(CoregConfig.MANUAL_TAG_FOLDER, xfmName))
            except:
                print('File move error. Check for system folder permissions. ')
                if currentRec:
                    resetSql = "UPDATE QC SET START = 0, USER = Null WHERE RECORD_ID = '{0}'".format(currentRec)
                    DBClient.executeNoResult(resetSql)
                sys.exit(0)
            rid = res[2]
            xfmID = xfmName.replace('{0}_{1}_'.format(study.upper(), rid), '')
            resSQL = "INSERT IGNORE INTO MANUAL_XFM VALUES (Null, '{0}', '{1}', '{2}', '{3}')".format(study.upper(), rid, xfmID, '{0}/{1}.xfm'.format(CoregConfig.MANUAL_XFM_FOLDER, xfmName))
            DBClient.executeNoResult(resSQL)
            finSQL = "UPDATE Coregistration SET END = 1 WHERE RECORD_ID = {0}".format(recID)
            DBClient.executeNoResult(finSQL)
        else:
            if currentRec:
                resetSql = "UPDATE QC SET START = 0, USER = Null WHERE RECORD_ID = '{0}'".format(currentRec)
                DBClient.executeNoResult(resetSql)
                continue


if __name__ == '__main__':
    os.setpgrp()
    try:
        if args.study is None and args.type is None and args.user is None and args.createUser is not None:
            ## Create User
            user = input('Admin username : ')
            passwd = getpass.getpass('Admin Password : ')
            hash_object = hashlib.sha256(passwd.encode('utf-8'))
            hex_dig = hash_object.hexdigest()
            sql = "SELECT * FROM Auth WHERE USER = '{0}' AND PASS = '{1}' AND LEVEL = 9".format(user, hex_dig)

            res = DBClient.executeAllResults(sql)

            if len(res) > 0:

                if len(DBClient.executeAllResults("SELECT * FROM Auth WHERE USER = '{0}'".format(args.createUser))) > 0:
                    print('User already exists. ')
                    sys.exit(0)

                newpass1 =  getpass.getpass('Enter password for {0} : '.format(args.createUser))
                newpass2 =  getpass.getpass('Re-enter password : '.format(args.createUser))
                if newpass1 == newpass2 :
                    hash_object = hashlib.sha256(newpass1.encode('utf-8'))
                    passHex = hash_object.hexdigest()

                    sqlInsert = "INSERT INTO Auth VALUES (Null, '{0}', 1, '{1}')".format(args.createUser, passHex)
                    DBClient.executeNoResult(sqlInsert)
                else:
                    print('Password mismatch. ')
                    sys.exit(0)

            else:
                print('Not authorized')
                sys.exit(0)

            sys.exit(0)



        elif args.study is not None and args.type is not None and args.user is not None and args.createUser is None:

            passwd = getpass.getpass('Password : ')
            hash_object = hashlib.sha256(passwd.encode('utf-8'))
            hex_dig = hash_object.hexdigest()
            sql = "SELECT * FROM Auth WHERE USER = '{0}' AND PASS = '{1}'".format(args.user, hex_dig)

            res = DBClient.executeAllResults(sql)

            if len(res) > 0:
                print('Starting coregistration. ')

                if not os.access(os.getcwd(), os.W_OK):
                    print('Current directory is not writable. Exiting. ')
                    sys.exit(0)

                if os.path.exists(xfmFile):
                    os.remove(xfmFile)
                if os.path.exists(tagFile):
                    os.remove(tagFile)

                runCoreg(args.study.upper(), args.type.upper(), args.user)
                print('Corestration finished. ')
            else:
                print('Username/password incorrect.. ')
                sys.exit(0)

        else:
            parser.error('Please specify QC type and username')
    except KeyboardInterrupt:
        if currentRec:
            resetSql = "UPDATE QC SET START = 0, USER = Null WHERE RECORD_ID = '{0}'".format(currentRec)
            DBClient.executeNoResult(resetSql)
        print('\nThank you for doing QC. Your input is very valuable. See you next time. :-)')
        os.killpg(0, signal.SIGTERM)



