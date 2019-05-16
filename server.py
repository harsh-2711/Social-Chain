from flask import Flask

# Instantiates the node
app = Flask(__name__)


@app.route('/')
def index():
    return "App is deployed"

if __name__ == "__main__":
    app.run()