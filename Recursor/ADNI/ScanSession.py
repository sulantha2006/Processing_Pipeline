__author__ = 'Seqian Wang'

# A class for each scan session


class ScanSession:
    def __init__(self, study, rid, scan_type, scan_date, scan_time,
                 s_identifier, i_identifier, download_folder, raw_folder, file_type, moved=0):
        self.study = study
        self.rid = rid
        self.scan_type = scan_type
        self.scan_date = scan_date
        self.scan_time = scan_time
        self.s_identifier = s_identifier
        self.i_identifier = i_identifier
        self.download_folder = download_folder
        self.raw_folder = raw_folder
        self.file_type = file_type
        self.moved = moved

    def printObject(self):
        print('{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}'.format(
            self.study, self.rid, self.scan_type, self.scan_date, self.scan_time, self.s_identifier,
            self.i_identifier, self.download_folder, self.raw_folder, self.file_type, self.moved))

    def printScanType(self):
        print('{0}'.format(self.scan_type))
