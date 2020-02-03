import pandas as pd
from app.modules.mod_db.db import  DB
from app.modules.mod_ex.interrupt import InterruptException
import dill
import logging
import time


class Insert:

    def __init__(self, user_id, file_name="dummy.csv"):
        self.user_id = user_id
        self.file_name = file_name
        self.lines = 0
        self.table_name = user_id
        self.paused = False
        self.terminated = False
        self.progress = 0
    
    def create_table(self):
        db = DB()
        db.create_connection()
        query = f"CREATE TABLE {self.user_id} (\
            PM10 FLOAT, \
            PM25 FLOAT, \
            PM1 FLOAT, \
            sationName varchar(255), \
            time varchar(255), \
            latitude FLOAT, \
            averaging FLOAT, \
            cityName varchar(255), \
            id FLOAT, \
            longitude FLOAT\
            );"
        db.run(query)
        db.close_connection()

    def get_checkpoint(self):
        query = f"SELECT MAX(SNo) from {self.table_name}"
        db = DB()
        db.create_connection()
        logging.info("Getting checkpoint from roll back purpose")
        roll_back_checkpoint = db.run(query)[0][0]
        db.close_connection()
        return roll_back_checkpoint

    def start(self):
        self.paused = False
        self.terminated = False

        db = DB()
        db.create_connection()

        csv = pd.read_csv(self.file_name, skiprows = self.lines)
        df = pd.DataFrame(csv)
        
        total_rows = len(df)

        for i in range(total_rows):
            try:
                logging.info(f"Inserting Row {self.lines + 1}")
                col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = df.iloc[i]
                query = f"INSERT INTO {self.table_name} VALUES({col1}, {col2}, {col3}, '{col4}', '{col5}', {col6}, {col7}, '{col8}', {col9}, {col10}, DEFAULT)"
                db.run(query)
                self.lines += 1
                self.progress = (self.lines/total_rows) * 100
                self.stop()
                time.sleep(1.5)
            except InterruptException:
                db.close_connection()
                break
    
    def roll_back(self, roll_back_checkpoint):
        query = f"DELETE FROM {self.table_name} WHERE SNo > {roll_back_checkpoint}"
        db = DB()
        db.create_connection()
        logging.info("Rolling back")
        db.run(query)
        db.close_connection()

    def stop(self):
        if self.paused or self.terminated:
            raise InterruptException

    def pause(self):
        self.paused = True
        logging.info("Pausing")
    
    def resume(self):
        self.paused = False

        if self.terminated:
            logging.info("Cannot resume, the process was terminated")
            return False

        logging.info("Resuming")
        self.start()

    def terminate(self, roll_back_checkpoint):
        self.terminated = True
        logging.info("Terminating")
        self.progress = 0
        self.roll_back(roll_back_checkpoint)
    
    def get_progress(self):
        return self.progress
