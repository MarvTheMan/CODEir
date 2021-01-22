from flask import Flask, render_template, request
from textprocessor import Textprocessor
import os
import pandas as pd

tp = Textprocessor()
app = Flask(__name__)

@app.route("/")
def index():
    # Starts the gui.
    return render_template("index.html")


@app.route("/results", methods = ["POST"])
def results():
    # Takes a given query, calculates the vectors and prints results.
    query = request.form["query"]
    return render_template("results.html", query = query)


@app.route("/settings")
def settings():
    # Page to adjust the settings of the application.
    return render_template("settings.html",
        warning = "",
        directory = tp.documents_folder, 
        language = tp.language, # TODO: is not passed correctly. maybe add a placeholder option with value "Choose language..."
        unwanted_chars = tp.unwanted_chars,
        enable_stemmer = tp.enable_stemmer,
        enable_lemmatizer = tp.enable_lemmatizer
    )

@app.route("/savedsettings", methods = ["GET", "POST"])
def savedsettings():
    # Gets all settings from form on /settings. Then changes settings and creates new matrix accordingly.
    chosen_folder = request.form["folder"]
    if not os.path.exists(chosen_folder):
        return render_template("settings.html",
        warning = f"folder: {chosen_folder} does not exist!",
        directory = tp.documents_folder, 
        language = tp.language, # TODO: is not passed correctly. maybe add a placeholder option with value "Choose language..."
        unwanted_chars = tp.unwanted_chars,
        enable_stemmer = tp.enable_stemmer,
        enable_lemmatizer = tp.enable_lemmatizer
        )
    tp.documents_folder = request.form["folder"]
    tp.language = request.form["language"]
    tp.unwanted_chars = request.form["unwanted_chars"]
    # empty checkboxes do not send a False boolean so we have to set to True if its in the form.
    if "enabled_stemmer" in request.form:       
        tp.enable_stemmer == True
    else:
        tp.enable_stemmer == False
    if "enable_lemmatizer" in request.form:       
        tp.enable_lemmatizer == True
    else:
        tp.enable_lemmatizer == False
    tp.create_term_weight_matrix()
    return render_template("index.html")


if __name__ == "__main__":
    # if os.path.exists(os.path.join("config", "twmatrix.csv")):
    #     print("Found an existing term weight matrix!")
    #     term_weight_matrix = pd.read_csv(os.path.join("config", "twmatrix.csv"))
    # else:
    #     tp.create_term_weight_matrix()
    tp.create_term_weight_matrix()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['DEBUG'] = True
    app.config['SERVER_NAME'] = "127.0.0.1:5000"
    app.run(use_reloader=False)
