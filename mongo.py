from pymongo import MongoClient


def client(user_name, password, db_name):
     return MongoClient("mongodb://{}:{}@localhost:27017/{}".format(user_name, password, db_name))
