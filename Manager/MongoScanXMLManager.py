import Config.MongoXMLConfig as moncfg
import glob, os, xmltodict, shutil
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from Utils.PipelineLogger import PipelineLogger

class MongoScanXMLManager:
    def __init__(self):
        pass

    def get_xml_list(self):
        return glob.glob('{0}/*.xml'.format(moncfg.XMLArchivePath))

    def get_subid_sid_iid(self, filepath):
        base = os.path.splitext(os.path.basename(filepath))[0]
        valid = False
        try:
            sid = base.split('_')[-2]
            iid = base.split('_')[-1]
            subid = base.split('_')[3]
            if len(subid) == 4 and sid.startswith('S') and iid.startswith('I'):
                valid = True
            return subid, sid, iid, valid
        except:
            return 0,0,0,False

    def add_to_mongoDB(self, file):
        f = open(file, 'r').read()
        try:
            o = xmltodict.parse(f)
        except:
            print('XML cannot be read - {0}.'.format(f))
            PipelineLogger.log('root', 'exception', 'XML cannot be read - {0}.'.format(f))
            return 0
        subId, SID, IID, valid = self.get_subid_sid_iid(file)
        if valid:
            _id = '{0}_{1}_{2}'.format(subId, SID, IID)
            o['_id'] = _id
            client = MongoClient('localhost', 27017)
            db = client.ADNI_Database
            collection = db.Scan_XML_Collection
            try:
                post_id = collection.insert_one(o).inserted_id
            except DuplicateKeyError:
                PipelineLogger.log('root', 'exception', 'XML already in DB - {0}.'.format(_id))
                post_id = _id
            try:
                shutil.move(file, moncfg.XMLProcessedArchivePath)
            except shutil.Error:
                PipelineLogger.log('root', 'Info', 'XML already in processed path  - {0}.'.format(_id))
                os.remove(file)
                post_id = _id
            return post_id

    def processXMLs(self):
        for f in self.get_xml_list():
            self.add_to_mongoDB(f)

