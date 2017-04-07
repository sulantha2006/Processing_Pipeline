#!/data/data02/sulantha/bin/anaconda35/bin/python
__author__ = 'sulantha'
import argparse
import sys
sys.path.append('/home/sulantha/PycharmProjects/Processing_Pipeline')
from Utils.DbUtils import DbUtils
from Config import QCConfig
import os, subprocess, signal
import getpass
import hashlib
import psutil

parser = argparse.ArgumentParser()
parser.add_argument('-s','--study', help='Study name. ', choices=['adni', 'dian'])
parser.add_argument('-t','--type', help='The type of qc. ', choices=['civet', 'av45', 'beast', 'fdg', 'fmri', 'av1451', 'pib'])
parser.add_argument('-u','--user', help='Username ')
parser.add_argument('--createUser', help=argparse.SUPPRESS)
args = parser.parse_args()

DBClient = DbUtils()
currentRec = None

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc_ in process.children(recursive=True):
        proc_.kill()
    process.kill()

def runCIVETQC(study, username):
    while 1:
        getEntrySql = "SELECT * FROM QC WHERE QC_TYPE = 'civet' AND STUDY = '{0}' AND SKIP = 0 AND START = 0 AND END = 0 LIMIT 1".format(study)
        try:
            resT = DBClient.executeSomeResults(getEntrySql, 1)[0]
        except IndexError:
            print('No files to QC. ')
            break
        res = resT[0]
        recID = res[0]
        global currentRec
        currentRec = recID
        setStartSql = "UPDATE QC SET START = 1, USER = '{1}' WHERE RECORD_ID = '{0}'".format(recID, username)
        DBClient.executeNoResult(setStartSql)


        civetpath = res[6]
        displayCMD = 'display {0}/verify/*_verify.png'.format(civetpath)
        proc = subprocess.Popen(displayCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/bin/bash')

        qcpass = 'z'
        while not (qcpass.lower() == 'y' or qcpass.lower() == 'n'):
                qcpass = input('QC [y/n] : ')

        if qcpass.lower() == 'y':
            resSQL = "UPDATE {0} SET {1} = 1 WHERE RECORD_ID = {2}".format(res[2], res[4], res[3])
            DBClient.executeNoResult(resSQL)
            finSQL = "UPDATE QC SET END = 1, PASS = 1 WHERE RECORD_ID = {0}".format(recID)
            DBClient.executeNoResult(finSQL)
        if qcpass.lower() == 'n':
            resSQL = "UPDATE {0} SET {1} = -1 WHERE RECORD_ID = {2}".format(res[2], res[4], res[3])
            DBClient.executeNoResult(resSQL)
            finSQL = "UPDATE QC SET END = 1, PASS = 0 WHERE RECORD_ID = {0}".format(recID)
            DBClient.executeNoResult(finSQL)

        kill(proc.pid)

def runBEASTQC(study, username):
    while 1:
        getEntrySql = "SELECT * FROM QC WHERE QC_TYPE = 'beast' AND STUDY = '{0}' AND SKIP = 0 AND START = 0 AND END = 0 LIMIT 1".format(study)
        try:
            res = DBClient.executeSomeResults(getEntrySql, 1)[0]
        except IndexError:
            print('No files to QC. ')
            break
        recID = res[0]
        global currentRec
        currentRec = recID
        setStartSql = "UPDATE QC SET START = 1, USER = '{1}' WHERE RECORD_ID = '{0}'".format(recID, username)
        DBClient.executeNoResult(setStartSql)


        beastPath = res[6]
        regCMD = 'register {0}/mask/*_skull_mask_native.mnc {0}/native/*_t1.mnc'.format(beastPath)
        proc = subprocess.Popen(regCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/bin/bash')

        qcpass = 'z'
        while not (qcpass.lower() == 'y' or qcpass.lower() == 'n'):
                qcpass = input('QC [y/n] : ')

        if qcpass.lower() == 'y':
            resSQL = "UPDATE {0} SET {1} = 1 WHERE RECORD_ID = {2}".format(res[2], res[4], res[3])
            DBClient.executeNoResult(resSQL)
            finSQL = "UPDATE QC SET END = 1, PASS = 1 WHERE RECORD_ID = {0}".format(recID)
            DBClient.executeNoResult(finSQL)
        if qcpass.lower() == 'n':
            resSQL = "UPDATE {0} SET {1} = -1 WHERE RECORD_ID = {2}".format(res[2], res[4], res[3])
            DBClient.executeNoResult(resSQL)
            finSQL = "UPDATE QC SET END = 1, PASS = 0 WHERE RECORD_ID = {0}".format(recID)
            DBClient.executeNoResult(finSQL)

        kill(proc.pid)

def runPETQC(study, type, username):
    while 1:
        getEntrySql = "SELECT * FROM QC WHERE QC_TYPE = '{0}' AND STUDY = '{1}' AND SKIP = 0 AND START = 0 AND END = 0 LIMIT 1".format(type.lower(), study)
        try:
            res = DBClient.executeSomeResults(getEntrySql, 1)[0]
        except IndexError:
            print('No files to QC. ')
            break

        recID = res[0]
        global currentRec
        currentRec = recID
        setStartSql = "UPDATE QC SET START = 1, USER = '{1}' WHERE RECORD_ID = '{0}'".format(recID, username)
        DBClient.executeNoResult(setStartSql)

        if study == 'ADNI' or study == 'adni':
            template = QCConfig.ADNIT1_TemplatePath
        elif study == 'DIAN' or study == 'dian':
            temaplte = QCConfig.ICBMT1_TemplatePath

        petPath = res[6]
        if type.lower() == 'av45':
            regCMD2 = 'register {0}/verify/*_final_qcVerify.mnc {1}'.format(petPath, temaplte)
        elif type.lower() == 'fdg':
            regCMD2 = 'register {0}/verify/*_final_qcVerify.mnc {1}'.format(petPath, temaplte)
        elif type.lower() == 'av1451':
            regCMD2 = 'register {0}/verify/*_final_qcVerify.mnc {1}'.format(petPath, temaplte)
        elif type.lower() == 'pib':
            regCMD2 = 'register {0}/verify/*_final_qcVerify.mnc {1}'.format(petPath, temaplte)
        proc2 = subprocess.Popen(regCMD2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/bin/bash')

        qcpass = 'z'
        while not (qcpass.lower() == 'y' or qcpass.lower() == 'n'):
                qcpass = input('QC [y/n] : ')

        if qcpass.lower() == 'y':
            resSQL = "UPDATE {0} SET {1} = 1 WHERE RECORD_ID = {2}".format(res[2], res[4], res[3])
            DBClient.executeNoResult(resSQL)
            finSQL = "UPDATE QC SET END = 1, PASS = 1 WHERE RECORD_ID = {0}".format(recID)
            DBClient.executeNoResult(finSQL)
        if qcpass.lower() == 'n':
            resSQL = "UPDATE {0} SET {1} = -1 WHERE RECORD_ID = {2}".format(res[2], res[4], res[3])
            DBClient.executeNoResult(resSQL)
            finSQL = "UPDATE QC SET END = 1, PASS = 0 WHERE RECORD_ID = {0}".format(recID)
            DBClient.executeNoResult(finSQL)

        kill(proc2.pid)


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
                if args.type == 'civet':
                    print('Starting {0} QC. '.format(args.type.upper()))
                    runCIVETQC(args.study.upper(), args.user)
                    print('{0} QC finished '.format(args.type.upper()))
                if args.type == 'beast':
                    print('Starting {0} QC. '.format(args.type.upper()))
                    runBEASTQC(args.study.upper(), args.user)
                    print('{0} QC finished '.format(args.type.upper()))
                if args.type == 'av45' or args.type == 'fdg' or args.type == 'av1451' or args.type == 'pib':
                    print('Starting {0} QC. '.format(args.type.upper()))
                    runPETQC(args.study.upper(), args.type, args.user)
                    print('{0} QC finished '.format(args.type.upper()))
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



