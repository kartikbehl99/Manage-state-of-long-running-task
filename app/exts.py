from flask import Flask
import logging

app = Flask(__name__)
app.config.from_object("config")

logging.basicConfig(level=app.config["LOGGING_LEVEL"],
                    format='%(asctime)s %(levelname)-8s %(message)s')