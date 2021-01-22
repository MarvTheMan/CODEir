from flask import Flask, render_template, request
from standard_functions import *
from matrix import *
from textprocessor import Textprocessor
import os

tp = Textprocessor()
app = Flask(__name__)
DOCUMENTS_FOLDER = os.path.join(os.getcwd(), "documents")

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
        directory = DOCUMENTS_FOLDER, 
        language = tp.language, # TODO: is not passed correctly. maybe add a placeholder option with value "Choose language..."
         unwanted_chars = tp.unwanted_chars
    )

@app.route("/savedsettings", methods = ["GET", "POST"])
def savedsettings():
    # Gets all settings from form on /settings. Then changes settings and shows mainpage.
    DOCUMENTS_FOLDER = request.form["folder"] # TODO: does not recieve folder correctly...
    print("folder is: " + request.form["folder"])
    tp.language = request.form["language"]
    tp.unwanted_chars = request.form["unwanted_chars"]

    # renders homepage after adjusting settings.
    return render_template("index.html")



if __name__ == "__main__":
    if os.path.exists(os.path.join("config", "twmatrix.csv")):
        print("Found an existing term weight matrix!")
        term_weight_matrix = get_twmatrix_from_csv()
    else:
        print("Term weight matrix was not found. Creating one for the provided documents...")
        wordcounts = {}
        for file in os.listdir(DOCUMENTS_FOLDER):
            if not file.endswith(".txt"):
                print(f"{file} is not a textfile! Skipping it!")
                continue
            wordlist = get_list_from_file(os.path.join("documents", file)) # TODO: this probably needs some adjustments when arbitrary folders can be searched.
            wordcounts[file] =tp.create_clean_wordcount(wordlist)
        freq_matrix = create_freq_matrix(wordcounts)
        term_weight_matrix = create_term_weight_matrix(freq_matrix)
        term_weight_matrix.to_csv(os.path.join("config", "twmatrix.csv"))
        print("Saved term weight matrix for next startup.")
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['DEBUG'] = True
    app.config['SERVER_NAME'] = "127.0.0.1:5000"
    app.run(use_reloader = False)
