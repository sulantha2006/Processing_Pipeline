__author__ = 'sulantha'

from Utils.PipelineLogger import PipelineLogger
from Utils.DbUtils import DbUtils
import Config.PipelineConfig as pc
from datetime import datetime
import itertools

class DIAN_T1_Helper:
    def __init__(self):
        self.DBClient = DbUtils()
        self.MatchDBClient = DbUtils(database=pc.DIAN_dataMatchDBName)

    def getMatchingT1(self, processingItemObj):
        modalityID = '{0}{1}{2}{3}{4}{5}{6}'.format(processingItemObj.study, processingItemObj.version,
                                                    processingItemObj.subject_rid, processingItemObj.modality,
                                                    processingItemObj.scan_date.replace('-', ''),
                                                    processingItemObj.s_identifier, processingItemObj.i_identifier)
        getFromMatchTableSQL = "SELECT * FROM MatchT1 WHERE MODALITY_ID = '{0}'".format(modalityID)
        existingMatchedRec = self.DBClient.executeAllResults(getFromMatchTableSQL)
        if len(existingMatchedRec) == 1:
            getConvSQL = "SELECT * FROM Conversion WHERE RECORD_ID = '{0}'".format(existingMatchedRec[0][3])
            return self.DBClient.executeAllResults(getConvSQL)[0]
        else:

            if processingItemObj.modality == 'FMRI':
                PipelineLogger.log('root', 'error',
                                   'FMRI T1 Matching not implemented. {0} - {1} - {2}'.format(processingItemObj.subject_rid,
                                                                                     processingItemObj.s_identifier.replace(
                                                                                         'S', ''),
                                                                                     processingItemObj.i_identifier.replace(
                                                                                         'I', '')))
                return None

            else:  # By Default, for PET images
                date_str = processingItemObj.scan_date.replace('-','')
                name_and_Mod = '{0}{1}'.format(processingItemObj.subject_rid, processingItemObj.modality)
                visit = processingItemObj.i_identifier.split('x')[0].replace(date_str,'').replace(name_and_Mod, '')
                pet_label = '{0}_{1}_{2}'.format(processingItemObj.subject_rid, visit, processingItemObj.modality.lower())
                getRecordSQL = "SELECT * FROM PET_MRI_Proc_Match WHERE Label LIKE '{0}'".format(pet_label)

            petrecord = self.MatchDBClient.executeAllResults(getRecordSQL)
            if not petrecord:
                PipelineLogger.log('root', 'error', 'Cannot find PET record : {0} - {1} - {2}'.format(processingItemObj.subject_rid, processingItemObj.s_identifier.replace('S', ''), processingItemObj.i_identifier.replace('I', '')))
                return None

            mr_name = petrecord[0][5]
            if mr_name == '':
                ### Processed with MR entry not found. Have to switch to date based matching.
                PipelineLogger.log('root', 'error',
                                       'Processed with MR entry not found. : {0} - {1} - {2} - Searching based on scan date. +/- 60 days from PET date'.format(
                                           processingItemObj.subject_rid, processingItemObj.modality, visit))
                return None

            mr_fid = petrecord[0][6]
            mr_visit = mr_name.split('_')[1]

            matchedT1withScanDescriptions= []

            for t1_type in ['MPRAGE', 'IRFSPGR', 'MPR', 'FSPGR']:
                mr_DB_iid = '{0}{3}{1}%x{2}'.format(processingItemObj.subject_rid, mr_visit, mr_fid, t1_type)
                getScanFromConversionSQL = "SELECT * FROM Conversion WHERE STUDY = '{0}' AND I_IDENTIFIER LIKE '{1}' AND SKIP = 0".format(processingItemObj.study,mr_DB_iid)
                t1_conversion = self.DBClient.executeAllResults(getScanFromConversionSQL)
                if len(t1_conversion) > 0:
                    matchedT1withScanDescriptions.append(t1_conversion[0])
            if len(matchedT1withScanDescriptions) < 1:
                PipelineLogger.log('root', 'error', 'Matched T1s are not in the database. : Subject, visit and FID - {0} {1} {2}'.format(processingItemObj.subject_rid, mr_visit, mr_fid))
                return None
            else:
                if len(matchedT1withScanDescriptions) == 1:
                    ## ONLY ONE MATCHED T1. GOOD> CHECK IF THE T1 is a good scan type and not a bluff !!!
                    self.addToMatchT1Table(processingItemObj, modalityID, matchedT1withScanDescriptions[0])
                    return matchedT1withScanDescriptions[0]

                else:
                    #### MORE THAN ONE FOUND. Very weird fro DIAN.
                    PipelineLogger.log('root', 'error',
                                       'MORE THAN ONE T1 Match FOUND. Very weird fro DIAN. : Subject and visit - {0} {1}'.format(
                                           processingItemObj.subject_rid, mr_visit))
                    return None

    def checkProcessed(self, t1Record):
        subject_id = t1Record[2]
        version = t1Record[11]
        s_id = t1Record[6]
        i_id = t1Record[7]
        checkProcessedSQL = "SELECT * FROM Processing WHERE RID = '{0}' AND VERSION = '{1}' AND S_IDENTIFIER = '{2}' AND I_IDENTIFIER = '{3}'".format(subject_id, version, s_id, i_id)
        result = self.DBClient.executeAllResults(checkProcessedSQL)[0]
        if len(result) < 1:
            PipelineLogger.log('root', 'error', 'Matched T1 is not added to the processing table. {0} - {1} - {2}'.format(subject_id, s_id, i_id))
            return False
        else:
            if result[12] == 1 and result[13] == 1:
                return result[8]
            else:
                PipelineLogger.log('root', 'error', 'Matched T1 is not process or QC failed. {0} - {1} - {2}'.format(subject_id, s_id, i_id))
                self.startProcessOFT1(result)
                return False

    def addToMatchT1Table(self, processingItemObj, modalityID, t1Record):
        pet_date = datetime.strptime(processingItemObj.scan_date, '%Y-%m-%d')
        mri_date =datetime.combine(t1Record[4], datetime.min.time())
        date_diff = abs(mri_date - pet_date)
        t1ID = '{0}{1}{2}_x_{3}_x_{4}{5}{6}'.format(t1Record[1], t1Record[11], t1Record[2], t1Record[3], t1Record[4].strftime('%Y-%m-%d').replace('-', ''), t1Record[6], t1Record[7])
        conversionID = t1Record[0]
        sql = "INSERT IGNORE INTO MatchT1 VALUES (Null, '{0}', '{1}', '{2}', {3}, Null)".format(modalityID, t1ID, conversionID, date_diff.days)
        self.DBClient.executeNoResult(sql)

    def startProcessOFT1(self, processTableEntry):
        recordId = processTableEntry[0]
        study = processTableEntry[1]
        sql = "UPDATE {0}_T1_Pipeline SET SKIP = 0 WHERE PROCESSING_TID = {1}".format(study, recordId)
        self.DBClient.executeNoResult(sql)
