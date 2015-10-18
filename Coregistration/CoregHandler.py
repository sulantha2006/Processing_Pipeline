__author__ = 'Sulantha'

from Utils.DbUtils import DbUtils

class CoregHandler:
    def __init__(self):
        self.DBClient = DbUtils()

    def requestCoreg(self, study, rid, type, pet_folder, t1_folder, petScanType, t1ScanType, xfm_name):
        regsql = "INSERT IGNORE INTO Coregistration VALUES (Null, '{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', 0, 0, 0, Null)".format(study.upper(), rid,
                                                                                                                         type.upper(),
                                                                                                                         pet_folder,
                                                                                                                         t1_folder, petScanType, t1ScanType, xfm_name)

        self.DBClient.executeNoResult(regsql)
