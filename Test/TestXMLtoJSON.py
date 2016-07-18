import xmltodict, json
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

f = open('/data/data03/sulantha/Downloads/ADNI/PET/xmls/ADNI_041_S_4143_AV45-Early_Coreg,_Avg,_Std_Img_and_Vox_Siz,_Uniform_Resolution_S199300_I389855.xml', 'r').read()
o = xmltodict.parse(f)
o['_id'] = '4143_S199300_I389855'
#print(json.dumps(o))

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.test_database
collection = db.test_collection
try:
    post_id = collection.insert_one(o).inserted_id
    print('Added')
except DuplicateKeyError:
    print('Duplicate')