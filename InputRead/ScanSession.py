#!/usr/bin/python
__author__ = 'Seqian Wang'

# A class for each scan session


class ScanSession:
    def __init__(self, study, rid, scan_type, scan_date, scan_time, download_folder, raw_folder, file_type, moved=0):
        self.study = study
        self.rid = rid
        self.scan_type = scan_type
        self.scan_date = scan_date
        self.scan_time = scan_time
        self.download_folder = download_folder
        self.raw_folder = raw_folder
        self.file_type = file_type
        self.moved = moved
