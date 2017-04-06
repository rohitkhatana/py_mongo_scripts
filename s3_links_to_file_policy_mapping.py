import requests
from config import Config
from mongo import client


class PolicyFileService(object):

    def __init__(self, db):
        self.db = db


    def migrate(self):
        print self.db
        print self.db['PolicyFile'].find_one()



if __name__ == '__main__':
    config = Config()
    db_obj = client(config.username, config.password, config.database)
    policyFileService = PolicyFileService(db_obj[config.database])
    policyFileService.migrate()
