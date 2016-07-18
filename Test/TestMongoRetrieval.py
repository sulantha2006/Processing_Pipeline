from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.ADNI_Database
XML_collection = db.Scan_XML_Collection


def getScannerType(processingItemObj):
    rid = processingItemObj['subject_rid']
    sid = processingItemObj['s_identifier']
    iid = processingItemObj['i_identifier']
    scan_info_dict = {}
    matched_doc = XML_collection.find_one({'_id': '{0}_{1}_{2}'.format(rid, sid, iid)})
    if matched_doc:
        for rec in matched_doc['idaxs']['project']['subject']['study']['series']['imagingProtocol']['protocolTerm'][
            'protocol']:
            try:
                scan_info_dict[rec['@term']] = rec['#text']
            except KeyError:
                scan_info_dict[rec['@term']] = None
    else:
        matched_doc = XML_collection.find_one({'idaxs.project.subject.study.series.seriesIdentifier': sid[1:],
                                                    'idaxs.project.subject.study.series.seriesLevelMeta.relatedImageDetail.originalRelatedImage.imageUID': iid[
                                                                                                                                                           1:]})
        for rec in matched_doc['idaxs']['project']['subject']['study']['series']['imagingProtocol']['protocolTerm'][
            'protocol']:
            try:
                scan_info_dict[rec['@term']] = rec['#text']
            except KeyError:
                scan_info_dict[rec['@term']] = None
matched_docs = XML_collection.find({'idaxs.project.subject.study.series.modality':'PET'})
allScanners = []
for doc in matched_docs:
    _id = doc['_id']
    rid = _id.split('_')[0]
    sid = _id.split('_')[1]
    iid = _id.split('_')[2]
    scannerType = getScannerType(dict(subject_rid = rid, s_identifier=sid, i_identifier=iid))
    allScanners.append(scannerType)


