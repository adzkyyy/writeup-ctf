import os
import subprocess

from flask import Flask, request

app = Flask(__name__)

app.secret_key = os.urandom(32)


@app.route("/")
def index():

    return "Hello World !"


@app.route("/curl", methods=["POST"])
def curl():

    url = request.form.get("url")

    p = subprocess.Popen(
        ["curl", "--connect-timeout", "5", url], stdout=open("/dev/null")
    )

    return "ok"


if __name__ == "__main__":
    app.run()
