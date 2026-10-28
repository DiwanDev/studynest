from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
        <h1>Welcome to StudyNest</h1>
        <p>Your simple study task manager.</p>
    """