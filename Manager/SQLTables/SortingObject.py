__author__ = 'sulantha'

class SortingObject:
    def __init__(self, values):
        self.record_id = 0 if 'record_id' not in values else values['record_id']
        self.study = values['study']
        self.rid = values['rid']
        self.scan_type = values['scan_type']
        self.scan_date = values['scan_date']
        self.scan_time = values['scan_time']
        self.s_identifier = values['s_identifier']
        self.i_identifier = values['i_identifier']
        self.file_type = values['file_type']
        self.download_folder = values['download_folder']
        self.raw_folder = values['raw_folder']
        self.moved = values['moved']

    def sqlInsert(self):
        return ("NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %d"
                % (self.study, self.rid, self.scan_type, self.scan_date, self.scan_time,
                   self.s_identifier, self.i_identifier, self.file_type,
                   self.download_folder, self.raw_folder, self.moved))

    def getValuesDict(self):
        return {'record_id': self.record_id,
                'study': self.study, 'rid': self.rid,
                'scan_type': self.scan_type,
                'scan_date': self.scan_date,
                'scan_time': self.scan_time,
                's_identifier': self.s_identifier,
                'i_identifier': self.i_identifier,
                'download_folder': self.download_folder,
                'raw_folder': self.raw_folder,
                'file_type': self.file_type,
                'moved': self.moved}