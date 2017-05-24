import requests
import os
from config import Config
from mongo import client


class PolicyFileService(object):

    def __init__(self, db, file_db, bucketName):
        self.db = db
        self.file_db = file_db
        self.bucketName = bucketName

    def __insert_and_fetch_file_mapping(self, policy_detail):
        return self.file_db['fileMapping'].insert_one(self.__policy_mapping(policy_detail))

    def __policy_mapping(self, policy_detail):
        return {
            'key': policy_detail.get('policyUrl'),
            'bucketName': 'docs.turtlemint.com',
            'host': 'localhost'
        }

    def __update_policy_detail(self, policy_detail, policy_mapping):
        policy_detail['policyDocumentId'] = str(policy_mapping.inserted_id)
        self.db['PolicyDetail'].update({'_id': policy_detail.get('_id')}, {'$set': policy_detail}, upsert=False)

    def migrate(self):
        policy_detail = self.db['PolicyDetail'].find({'policyUrl': {'$exists': True, '$ne': None }})[0]
        if policy_detail.has_key('policyUrl'):
            print policy_detail.get('policyUrl')
            policy_mapping = self.__insert_and_fetch_file_mapping(policy_detail)
            self.__update_policy_detail(policy_detail, policy_mapping)
            print 'done'


if __name__ == '__main__':
    config = Config().turtlemint
    file_config = Config().file_mapping
    db_obj = client(config['username'], config['password'], config['database'])
    file_db = client(file_config['username'], file_config['password'], file_config['database'])
    policyFileService = PolicyFileService(db_obj[config['database']], file_db[config['database']], config['bucketName'])
    policyFileService.migrate()
