from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, declarative_base
import json


class sqlService:
    
    engine = None
    session = None

    def init():
        jsonfile = "dbConnection.json"
        with open(jsonfile, 'r') as file:
            dbCreds = json.loads(file.read())
        #mysql+pymysql://username:password@host:port/database_name
        dbUri = f"mysql+pymysql://{dbCreds['data']['user']}:{dbCreds['data']['password']}@{dbCreds['data']['host']}:{dbCreds['data']['port']}/{dbCreds['data']['dbName']}"
        
        sqlService.engine = create_engine(dbUri)
        declarative_base().metadata.create_all(sqlService.engine)
        sqlService.session = sessionmaker(bind=sqlService.engine)

    @staticmethod
    def create(model_instance):
        with sqlService.session() as session:
            session.add(model_instance)
            session.commit()

    @staticmethod
    def read(model, primary_key):
        with sqlService.session() as session:
            return session.query(model).get(primary_key)
    
    @staticmethod
    def update(model_instance):
        with sqlService.session() as session:
            session.merge(model_instance)
            session.commit()
    
    @staticmethod
    def delete(model, primary_key):
        with sqlService.session() as session:
            instance = session.query(model).get(primary_key)
            if instance:
                session.delete(instance)
                session.commit()