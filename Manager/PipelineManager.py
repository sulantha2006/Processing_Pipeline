__author__ = 'sulantha'
from Recursor.Recursor import Recursor
from Utils.DbUtils import DBUtils

class PipelineManager:
    def __init__(self):
        self.recursor = None
        self.DBClient = DBUtils()

def main():
    pipeline = PipelineManager
    pipeline.recursor = Recursor('ADNI', '/data/data02/ADNI/downloads/New2')
    instances = pipeline.recursor.recurse()

    for i in instances:
        i.printObject()

        DBUtils.execute(
            "If Not Exists (Select * from Sorting_Table where (studyID, rid, scan_type, study_date, s_identifider, i_identifier) = ({0},{1},{2},{3},{4})"
            "Begin"
            "Insert into Sorting {5} "
            "End".format())

if __name__ == '__main__':
    main()

