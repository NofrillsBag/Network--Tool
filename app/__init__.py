import os
from flask import Flask

template_path = os.path.join(os.path.dirname(__file__), "templates")
app = Flask(__name__, template_folder=template_path)

from app import routes

