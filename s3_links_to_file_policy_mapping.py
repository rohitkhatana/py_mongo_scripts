import requests
import os
from config import Config
from mongo import client


class PolicyFileService(object):

    def __init__(self, db, bucketName):
        self.db = db
        self.bucketName = bucketName

    def __insert_into_file_mapping(self, policy_detail):
        return self.db['fileMapping'].insert_one(self.__policy_mapping(policy_detail))

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
            policy_mapping = self.__insert_into_file_mapping(policy_detail)
            self.__update_policy_detail(policy_detail, policy_mapping)


if __name__ == '__main__':
    config = Config()
    db_obj = client(config.username, config.password, config.database)
    #db_obj = client('turt#Dev', 'hD=h7wb#', 'turtlemint')
    policyFileService = PolicyFileService(db_obj[config.database], config.bucketName)
    policyFileService.migrate()
