import json
import os
from flask import Flask, redirect, render_template, request
from attachment_checker import AttachmentChecker

application = Flask(__name__)
application.config["DEBUG"] = True
application_PATH = os.getcwd()

AC = AttachmentChecker()


@application.route("/")
def redirecter():
    return redirect("/index")


@application.route("/index")
def index():
    return render_template("main.html")


@application.route("/download", methods=['GET', 'POST'])
def download():
    username = request.form.get("username")
    password = request.form.get("password")
    AC.download(username, password)
    return index()


@application.route("/scan", methods=['GET', 'POST'])
def scan():
    return json.dumps(AC.scan())


if __name__ == "__main__":
    application.run()
