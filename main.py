from flask import Flask, render_template, request
from standard_functions import *
from matrix import *
from textprocessor import Textprocessor
import os


documents = os.listdir("documents")
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
    return render_template("settings.html")


documents = os.listdir("documents") #this variable can be set to other folders on the machine to search them.

if __name__ == "__main__":
    if os.path.exists(os.path.join("config", "twmatrix.csv")):
        print("Found an existing term weight matrix!")
        term_weight_matrix = get_twmatrix_from_csv()
    else:
        print("Term weight matrix was not found. Creating one for the provided documents...")
        wordcounts = {}
        tp = Textprocessor()
        for file in documents:
            if not file.endswith(".txt"):
                print(f"{file} is not a textfile! Skipping it!")
                continue
            wordlist = get_list_from_file(os.path.join("documents", file))
            wordcounts[file] =tp.create_clean_wordcount(wordlist)
        freq_matrix = create_freq_matrix(wordcounts)
        term_weight_matrix = create_term_weight_matrix(freq_matrix)
        term_weight_matrix.to_csv(os.path.join("config", "twmatrix.csv"))
        print("Saved term weight matrix for next startup.")
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['DEBUG'] = True
    app.config['SERVER_NAME'] = "127.0.0.1:5000"
    app.run(use_reloader = False)
