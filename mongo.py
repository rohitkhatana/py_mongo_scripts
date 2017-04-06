from pymongo import MongoClient


def db(user_name, password, db_name):
     client = MongoClient("mongodb://{}:{}@localhost:27017/{}".format(user_name, password, db_name))
     return client[db_name]
