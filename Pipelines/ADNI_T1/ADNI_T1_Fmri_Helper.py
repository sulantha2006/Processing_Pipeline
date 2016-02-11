__author__ = 'sulantha'

from Utils.PipelineLogger import PipelineLogger
from Utils.DbUtils import DbUtils
import Config.PipelineConfig as pc
from datetime import datetime
import itertools

class ADNI_T1_Fmri_Helper:
    def __init__(self):
        self.DBClient = DbUtils()
        self.MatchDBClient = DbUtils(database=pc.ADNI_dataMatchDBName)

    def getMatchingT1(self, processingItemObj):
        modalityID = '{0}{1}{2}{3}{4}{5}{6}'.format(processingItemObj.study, processingItemObj.version, processingItemObj.subject_rid, processingItemObj.modality, processingItemObj.scan_date.replace('-', ''), processingItemObj.s_identifier, processingItemObj.i_identifier)
        getFromMatchTableSQL = "SELECT * FROM MatchT1 WHERE MODALITY_ID = '{0}'".format(modalityID)

        # Find matching record in matching T1 table
        existingMatchedRec = self.DBClient.executeAllResults(getFromMatchTableSQL)
        if len(existingMatchedRec) == 1:
            getConvSQL = "SELECT * FROM Conversion WHERE RECORD_ID = '{0}'".format(existingMatchedRec[0][3])
            return self.DBClient.executeAllResults(getConvSQL)[0]
        else:
            # If can't find them, look into MRIList to find an equivalent
            getFmriRecordSQL = "SELECT * FROM MRILIST WHERE subject LIKE '%_%_{0}' AND seriesid = {1} AND imageuid = {2}".format(processingItemObj.subject_rid, processingItemObj.s_identifier.replace('S', ''), processingItemObj.i_identifier.replace('I', ''))
            FmriRecord = self.MatchDBClient.executeAllResults(getFmriRecordSQL)
            if not FmriRecord:
                PipelineLogger.log('root', 'error', 'Cannot find Fmri record : {0} - {1} - {2}'.format(processingItemObj.subject_rid, processingItemObj.s_identifier.replace('S', ''), processingItemObj.i_identifier.replace('I', '')))
                return None

            visit_code = pc.ADNI_visitCode_Dict[FmriRecord[0][2]]
            getMRIRecordsSQL = "SELECT * FROM MPRAGEMETA WHERE subjectid LIKE '%_%_{0}'".format(processingItemObj.subject_rid)

            mrirecords = self.MatchDBClient.executeAllResults(getMRIRecordsSQL)
            if not mrirecords:
                PipelineLogger.log('root', 'error', '################################  - Error !!!!! Cannot find any MRI records : {0} - Please check ADNI recs. ################################'.format(processingItemObj.subject_rid))
                return None

            # getMRISecondarySQL = "SELECT * FROM MRILIST WHERE subject LIKE '%_%_{0}'".format(processingItemObj.subject_rid)
            # mriSecondaryRecords = self.MatchDBClient.executeAllResults(getMRISecondarySQL)
            # t_mrirecords = mrirecords
            # for record in mriSecondaryRecords:
            #     distint = 1
            #     for i in t_mrirecords:
            #         if record[7] == i[7] and record[8] == i[8]:
            #             distint = 0
            #     if distint:
            #         mrirecords.append(record)

            matchedT1Recs = []
            for rec in mrirecords:
                if pc.ADNI_visitCode_Dict[rec[2]] == visit_code:
                    matchedT1Recs.append(rec)
            if len(matchedT1Recs) == 0:
                PipelineLogger.log('root', 'error', 'Cannot match visit codes for : {0} - {1} - {2} - Searching based on scan date. +/- 60 days from PET date'.format(processingItemObj.subject_rid, processingItemObj.modality, visit_code))
                pet_date = datetime.strptime(processingItemObj.scan_date, '%Y-%m-%d')
                sortedRecs = sorted(mrirecords, key=lambda x:abs(datetime.strptime(x[5], '%Y-%m-%d') - pet_date))
                closestDate = [k for k,g in itertools.groupby(sortedRecs, key=lambda x:abs(datetime.strptime(x[5], '%Y-%m-%d') - pet_date))][0]
                PipelineLogger.log('root', 'error', 'PET MRI Matching based on dates - match visit codes for : {0} - {1} - {2} - Distance between MRI/PET : {3} days.'.format(processingItemObj.subject_rid, processingItemObj.modality, visit_code, closestDate))
                closestMatchedRecs = [list(g) for k,g in itertools.groupby(sortedRecs, key=lambda x:abs(datetime.strptime(x[5], '%Y-%m-%d') - pet_date))][0]
                matchedT1Recs = closestMatchedRecs
            if len(matchedT1Recs) == 0:
                PipelineLogger.log('root', 'error', 'Cannot match visit codes for : {0} - {1} - {2}'.format(processingItemObj.subject_rid, processingItemObj.modality, visit_code))
                return None

            matchedT1withScanDescriptions = []
            for rec in matchedT1Recs:
                getScanFromConversionSQL = "SELECT * FROM Conversion WHERE STUDY = '{0}' AND S_IDENTIFIER = '{1}' AND I_IDENTIFIER = '{2}' AND SKIP = 0".format(processingItemObj.study,'S{0}'.format(rec[7]), 'I{0}'.format(rec[8]))
                t1_conversion = self.DBClient.executeAllResults(getScanFromConversionSQL)
                if len(t1_conversion) > 0 :
                    matchedT1withScanDescriptions.append(t1_conversion[0])
                else:
                    PipelineLogger.log('root', 'error', 'Correspoding MRI was not found in the system : {0} - {1} - {2}'.format(processingItemObj.subject_rid, 'S{0}'.format(rec[7]), 'I{0}'.format(rec[8])))
                    continue
            if len(matchedT1withScanDescriptions) < 1:
                PipelineLogger.log('root', 'error', 'Matched T1s are not in the database. : Matched T1 s - \n {0}'.format(matchedT1Recs))
                return None
            else:
                if len(matchedT1withScanDescriptions) == 1:
                    ## ONLY ONE MATCHED T1. GOOD> CHECK IF THE T1 is a good scan type and not a bluff !!!
                    if matchedT1withScanDescriptions[0][3] in pc.ADNI_T1_match_accepted_scantypes:
                        self.addToMatchT1Table(processingItemObj, modalityID, matchedT1withScanDescriptions[0])
                        return matchedT1withScanDescriptions[0]
                    else:
                        PipelineLogger.log('root', 'error', 'Matched T1s is not accepted scan type. : Matched T1 s - \n {0}'.format(matchedT1withScanDescriptions[0]))
                        return None

                else:
                    #### MORE THAN ONE FOUND. SELECT ONE BASED ON SCAN TYPE PRIORITY
                    sortedList = sorted(matchedT1withScanDescriptions, key=lambda x: (pc.ADNI_T1_match_scantype_priorityList.index(x[3]), -x[5]))
                    self.addToMatchT1Table(processingItemObj, modalityID, sortedList[0])
                    return sortedList[0]

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
                PipelineLogger.log('root', 'debug', 'Matched T1 is processed and QC passed. {0} - {1} - {2}'.format(subject_id, s_id, i_id))
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
        sql = "INSERT IGNORE INTO MatchT1 VALUES (Null, '{0}', '{1}', '{2}', {3})".format(modalityID, t1ID, conversionID, date_diff.days)
        self.DBClient.executeNoResult(sql)

    def startProcessOFT1(self, processTableEntry):
        recordId = processTableEntry[0]
        study = processTableEntry[1]
        sql = "UPDATE {0}_T1_Pipeline SET SKIP = 0 WHERE PROCESSING_TID = {1}".format(study, recordId)
        self.DBClient.executeNoResult(sql)
