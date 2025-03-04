from flask import Flask, request, render_template, send_file
import spotifyapp
import os

app = Flask(__name__)

app.route("/")
def index():
    return "Nothing Here. This is the server for the Glove Project."


app.register_blueprint(spotifyapp.bp)

if __name__ == "__main__":
    app.run(debug="true", host="0.0.0.0", port=5000)