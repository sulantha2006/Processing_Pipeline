__author__ = 'Sulantha'

from Utils.DbUtils import DbUtils
import glob, os, sys, fileinput

if __name__ == '__main__':
    DBClient = DbUtils()
    sql1 = "SELECT * FROM Processing WHERE PROCESSED = 1 AND MODALITY ='T1'"
    res = DBClient.executeAllResults(sql1)
    for result in res:
        proc_id = result[0]
        #sql2 = "SELECT * FROM Processing WHERE RECORD_ID = {0}".format(proc_id)
        #process_rec = DBClient.executeAllResults(sql2)[0]

        T1Path = result[8]
        try:
            civet_nl_xfm_name = '{0}/civet/transforms/nonlinear/*nlfit_It.xfm'.format(T1Path)
            civet_nl_xfm_file = glob.glob(civet_nl_xfm_name)[0]

            civet_nl_mnc_name = '{0}/civet/transforms/nonlinear/*nlfit_It_grid_0.mnc'.format(T1Path)
            civet_nl_mnc_file = glob.glob(civet_nl_mnc_name)[0]
            civet_nl_mnc_name_base = os.path.basename(civet_nl_mnc_file)

            for line in fileinput.input(civet_nl_xfm_file, inplace=True):
                if 'Displacement_Volume' in line:
                    line = 'Displacement_Volume = {0};'.format(civet_nl_mnc_name_base)
                sys.stdout.write(line)
        except:
            s = "UPDATE Processing SET QCPASSED = 0 WHERE RECORD_ID = {0}".format(proc_id)
            DBClient.executeNoResult(s)
            print('Files not found - {0} - {1}'.format(proc_id, T1Path))