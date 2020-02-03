from app.modules.mod_db.db import DB
import csv, time, logging, os
from app.modules.mod_ex.interrupt import InterruptException

class Export:
    def __init__(self, user_id):
        self.table_name = user_id
        self.row = 1
        self.paused = False
        self.terminated = False
        self.completed = False

    def export(self):
        self.paused = False
        self.terminated = False

        db = DB()
        db.create_connection()

        data = []
        query = f"SELECT * FROM {self.table_name} WHERE SNo={self.row}"
        logging.info(f"Getting row: {self.row}")
        data = db.run(query)

        if len(data[0]) == 0:
            logging.info("Nothing to export")
            return

        f = open(f"./{self.table_name}.csv", 'w')
        my_file = csv.writer(f)

        while len(data):
            try:
                my_file.writerow(data[0])
                self.row += 1
                self.stop()
                time.sleep(2)
                query = f"SELECT * FROM {self.table_name} WHERE SNo={self.row}"
                logging.info(f"Getting row: {self.row}")
                data = db.run(query)
            except InterruptException:
                db.close_connection()
                f.close()
                return
        
        self.completed = True

    def roll_back(self):
        try:
            logging.info("Rolling back")
            os.remove(f"./{self.table_name}.csv")
        except FileNotFoundError:
            logging.error("File not found")

    def stop(self):
        if self.paused or self.terminated:
            raise InterruptException
    
    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

        if self.terminated:
            logging.info("Cannot resume, the process was terminated")
            return False
        
        logging.info("Resuming")
        self.export()

    def terminate(self):
        self.terminated = True
        self.completed = False
        logging.info("Terminating")
        self.roll_back()

    def get_status(self):
        return self.completed