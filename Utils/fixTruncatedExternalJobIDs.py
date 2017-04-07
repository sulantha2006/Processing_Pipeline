from Utils.DbUtils import DbUtils
DBClient = DbUtils()

getAllTodoSQL = "SELECT JOB_ID FROM externalWaitingJobs WHERE `JOB_ID` NOT LIKE '%CIVETRUN'"
res = DBClient.executeAllResults(getAllTodoSQL)

for job_id in res:
    job_id = job_id[0]
    job_type = job_id.split('_')[-1]
    old_job_id = job_id
    new_job_id = job_id.replace(job_type, 'CIVETRUN')
    ins_sql = "UPDATE externalWaitingJobs SET `JOB_ID` = \'{0}\' WHERE `JOB_ID` = \'{1}\'".format(new_job_id,old_job_id)
    try:
        DBClient.executeNoResult(ins_sql)
    except Exception as e:
        print(new_job_id)
