import logging
import time
import json
import os

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class SQLAlchemy:
    def __init__(self, app: FastAPI = None, **kwargs):
        self._engine = None
        self._session = None
        if app is not None:
            self.init_app(app=app, **kwargs)

    def init_app(self, app: FastAPI, **kwargs):
        """
        connect db
        """
        database_url = kwargs.get("DB_URL")
        pool_recycle = kwargs.get("DB_POOL_RECYCLE", 900)
        echo = kwargs.get("DB_ECHO", False)
        self._engine = create_engine(database_url, echo=echo, pool_recycle=pool_recycle, pool_pre_ping=True)
        self._session = sessionmaker(autocommit=False, bind=self._engine)

        @app.on_event("startup")
        def startup():
            for re_try in range(3):
                try:
                    self._engine.connect()
                    break
                except:
                    logging.error("DB connect failed.")
                    time.sleep(15)
                    continue
            else:
                raise Exception("DB not connected")

        @app.on_event("shutdown")
        def shutdown():
            self._session.close_all()
            self._engine.dispose()

    def get_db(self):
        """
        요청마다 db 세션을 가져오는 함수입니다.
        """
        if self._session is None:
            raise Exception("must init_db")
        db_session = None
        try:
            db_session = self._session()
            yield db_session
        finally:
            db_session.close()

    @property
    def session(self):
        return self.get_db

    @property
    def engine(self):
        return self._engine


db = SQLAlchemy()
Base = declarative_base()


