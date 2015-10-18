__author__ = 'Sulantha'
from Utils.DbUtils import DbUtils
from Utils.PipelineLogger import PipelineLogger
from Coregistration.CoregHandler import CoregHandler

class PETHelper:
    def __init__(self):
        self.DBClient = DbUtils()
        self.CoregHand = CoregHandler()

    def getManualXFM(self, processingItemObj, matchedT1entry):
        study = processingItemObj.study
        rid = processingItemObj.subject_rid
        pet_sid = processingItemObj.s_identifier
        pet_iid = processingItemObj.i_identifier
        t1_sid = matchedT1entry[6]
        t1_iid = matchedT1entry[7]

        xfmUID = 'PET_{0}_{1}_T1_{2}_{3}'.format(pet_sid, pet_iid, t1_sid, t1_iid)

        getXFMSQL = "SELECT * FROM MANUAL_XFM WHERE STUDY = '{0}' AND RID = '{1}' AND XFM_UNIQUEID = '{2}'".format(study, rid, xfmUID)
        res = self.DBClient.executeAllResults(getXFMSQL)

        if len(res) > 0:
            PipelineLogger.log('root', 'INFO', '++ Manual XFM found. - {0} - {1}'.format(processingItemObj.subject_rid, processingItemObj.scan_date))
            manXFM = res[0][4]
            updateSQL = "UPDATE {0}_{1}_Pipeline SET MANUAL_XFM = '{2}' WHERE RECORD_ID = {3}".format(study, processingItemObj.modality, manXFM, processingItemObj.processing_rid)
            self.DBClient.executeNoResult(updateSQL)
            return manXFM
        else:
            PipelineLogger.log('root', 'INFO', '$$$$$$$ Manual XFM not found. Requesting manual XFM. - {0} - {1}'.format(processingItemObj.subject_rid, processingItemObj.scan_date))
            pet_folder = processingItemObj.converted_folder
            pet_scanType = self.getScanType(processingItemObj)
            t1_folder = matchedT1entry[10]
            t1_scanType = matchedT1entry[3]
            xfmFileName = '{0}_{1}_PET_{2}_{3}_T1_{4}_{5}'
            self.CoregHand.requestCoreg(study, rid, processingItemObj.modality, pet_folder, t1_folder, pet_scanType, t1_scanType, xfmFileName)

    def getScanType(self, processingItemObj):
        r = self.DBClient.executeAllResults("SELECT SCAN_TYPE FROM Conversion WHERE STUDY = '{0}' AND RID = '{1}' "
                                        "AND SCAN_DATE = '{2}' AND S_IDENTIFIER = '{3}' "
                                        "AND I_IDENTIFIER = '{4}'".format(processingItemObj.study,
                                                                          processingItemObj.subject_rid,
                                                                          processingItemObj.scan_date,
                                                                          processingItemObj.s_identifier,
                                                                          processingItemObj.i_identifier))
        return r[0][0]


