__author__ = 'sulantha'

class ProcessingObject:
    def __init__(self, values):
        self.record_id = 0 if 'record_id' not in values else values['record_id']
        self.study = values['study']
        self.rid = values['rid']
        self.modality = values['modality']
        self.scan_date = values['scan_date']
        self.scan_time = values['scan_time']
        self.s_identifier = values['s_identifier']
        self.i_identifier = values['i_identifier']
        self.root_folder = values['root_folder']
        self.converted_folder = values['converted_folder']
        self.version = values['version']

    def sqlInsert(self):
        return ("NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 0, 0, 0, NULL, NULL, NULL"
                % (self.study, self.rid, self.modality, self.scan_date, self.scan_time,
                   self.s_identifier, self.i_identifier, self.root_folder, self.converted_folder, self.version))

    def getValuesDict(self):
        return {'record_id': self.record_id,
                'study': self.study, 'rid': self.rid,
                'modality':self.modality,
                'scan_date': self.scan_date,
                'scan_time': self.scan_time,
                's_identifier': self.s_identifier,
                'i_identifier': self.i_identifier,
                'root_folder':self.root_folder,
                'converted_folder':self.converted_folder,
                'version': self.version}
