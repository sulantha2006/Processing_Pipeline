__author__ = 'Sulantha'

from Utils.DbUtils import DbUtils
import glob, os, sys, fileinput

if __name__ == '__main__':
    DBClient = DbUtils
    sql = "SELECT * FROM ADNI_T1_Pipeline WHERE CIVET = 1 AND ADDITIONAL_1 ='OLD_PROC'"
    res = DBClient.executeAllResults(sql)
    for result in res:
        proc_id = result[1]
        sql2 = "SELECT * FROM Processing WHERE RECORD_ID = {0}".format(proc_id)
        process_rec = DBClient.executeAllResults(sql2)

        T1Path = process_rec[8]

        civet_nl_xfm_name = '{0}/civet/transforms/nonlinear/*nlfit_It.xfm'.format(T1Path)
        civet_nl_xfm_file = glob.glob(civet_nl_xfm_name)[0]

        civet_nl_mnc_name = '{0}/civet/transforms/nonlinear/*nlfit_It_grid_0.mnc'.format(T1Path)
        civet_nl_mnc_file = glob.glob(civet_nl_mnc_name)[0]
        civet_nl_mnc_name_base = os.path.basename(civet_nl_mnc_file)

        for line in fileinput.input(civet_nl_xfm_file, inplace=True):
            if 'Displacement_Volume' in line:
		        line = 'Displacement_Volume = {0};'.format(civet_nl_mnc_name_base)
            sys.stdout.write(line)
