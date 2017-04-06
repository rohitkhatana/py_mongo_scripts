import requests
import os
from config import Config
from mongo import client


class PolicyFileService(object):

    def __init__(self, db, bucketName):
        self.db = db
        self.bucketName = bucketName

    def __download_file(self, policy_s3):
        req = requests.get(policy_s3.get('policyUrl'), stream=True)
        with open(policy_s3.get('_id'), 'wb') as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    def __policy_doc(self, response):
        return {
                'document_id': response.get('data').get('id')
            }

    def __insert_into_policy_file(self, policy_doc):
        print self.db['PolicyFile'].insert_one(policy_doc)

    def __upload_and_migrate(self, policy_s3):
        file_info = {'file': open(policy_s3.get("_id"), 'rb')}
        values = {'host': 'localhost', 'bucketName': self.bucketName}
        res = requests.post('http://localhost:9011/v1/file/upload', files=file_info, data=values)
        if res.status_code == 200:
            policy_doc = self.__policy_doc(res.json())
            self.__insert_into_policy_file(policy_doc)

    def __remove_downloaded_file(self, policy_s3):
        os.remove(policy_s3.get('_id'))

    def migrate(self):
        policy_s3 = self.db['PolicyS3'].find_one()
        self.__download_file(policy_s3)
        self.__upload_and_migrate(policy_s3)
        self.__remove_downloaded_file(policy_s3)


if __name__ == '__main__':
    config = Config()
    db_obj = client(config.username, config.password, config.database)
    policyFileService = PolicyFileService(db_obj[config.database], config.bucketName)
    policyFileService.migrate()
