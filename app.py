from textwrap import dedent
from uuid import uuid4
import json

from flask import Flask, jsonify, request

from Blockchain import Blockchain

# Instantiates the node
app = Flask(__name__)


@app.route('/')
def index():
    return "App is deployed and Imports are ready"

if __name__ == "__main__":
    app.run()