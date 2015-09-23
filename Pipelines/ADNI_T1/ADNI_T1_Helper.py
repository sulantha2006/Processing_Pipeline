__author__ = 'sulantha'

from Utils.PipelineLogger import PipelineLogger
from Utils.DbUtils import DbUtils
import Config.PipelineConfig as pc

class ADNI_T1_Helper:
    def __init__(self):
        self.DBClient = DbUtils()
        self.MatchDBClient = DbUtils(database=pc.ADNI_dataMatchDBName)

    def getMatchingT1(self, processingItemObj):
        getPETRecordSQL = "SELECT * FROM PET_META_LIST WHERE subject LIKE '%_%_{0}' AND seriesid = {1} AND imageid = {2}".format(processingItemObj.subject_rid, processingItemObj.s_identifier.replace('S', ''), processingItemObj.i_identifier.replace('I', ''))


        petrecord = self.MatchDBClient.executeAllResults(getPETRecordSQL)
        if not petrecord:
            PipelineLogger.log('root', 'error', 'Cannot find PET record : {0} - {1} - {2}'.format(processingItemObj.subject_rid, processingItemObj.s_identifier.replace('S', ''), processingItemObj.i_identifier.replace('I', '')))
            return None
        visit_code = pc.ADNI_visitCode_Dict[petrecord[0][2]]

        getMRIRecordsSQL = "SELECT * FROM MPRAGEMETA WHERE subjectid LIKE '%_%_{0}'".format(processingItemObj.subject_rid)
        mrirecords = self.MatchDBClient.executeAllResults(getMRIRecordsSQL)
        if not mrirecords:
            PipelineLogger.log('root', 'error', 'Cannot find any MRI records : {0}}'.format(processingItemObj.subject_rid))
            return None

        getMRISecondarySQL = "SELECT * FROM MRILIST WHERE subject LIKE '%_%_{0}'".format(processingItemObj.subject_rid)
        mriSecondaryRecords = self.MatchDBClient.executeAllResults(getMRISecondarySQL)
        t_mrirecords = mrirecords
        for record in mriSecondaryRecords:
            distint = 1
            for i in t_mrirecords:
                if record[7] == i[7] and record[8] == i[8]:
                    distint = 0
            if distint:
                mrirecords.append(record)

        matchedT1Recs = []
        for rec in mrirecords:
            if pc.ADNI_visitCode_Dict[rec[2]] == visit_code:
                matchedT1Recs.append(rec)
        if len(matchedT1Recs) == 0:
            PipelineLogger.log('root', 'error', 'Cannot match visit codes for : {0} - {1} - {2}'.format(processingItemObj.subject_rid, processingItemObj.modality, visit_code))
            return None

        matchedT1withScanDescriptions = []
        for rec in matchedT1Recs:
            getScanFromConversionSQL = "SELECT * FROM Conversion WHERE STUDY = '{0}' AND VERSION = '{1}' AND S_IDENTIFIER = '{2}' AND I_IDENTIFIER = '{3}'".format(processingItemObj.study, processingItemObj.version, 'S{0}'.format(rec[7]), 'I{0}'.format(rec[8]))
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
                    return matchedT1withScanDescriptions[0]
                else:
                    PipelineLogger.log('root', 'error', 'Matched T1s is not accepted scan type. : Matched T1 s - \n {0}'.format(matchedT1withScanDescriptions[0]))
                    return None

            else:
                #### MORE THAN ONE FOUND. SELECT ONE BASED ON SCAN TYPE PRIORITY
                sourtedList = sorted(matchedT1withScanDescriptions, key=lambda x:pc.ADNI_T1_match_scantype_priorityList.index(x[3]))
                return sourtedList[0]

