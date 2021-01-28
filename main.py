from flask import Flask, render_template, request
from textprocessor import Textprocessor
import os
import pandas as pd
import query_functions as query_funcs

tp = Textprocessor()
app = Flask(__name__)


@app.route("/")
def index():
    # Startpage of the GUI.
    return render_template("index.html")


@app.route("/results", methods=["POST"])
def results():
    # Takes a given query, calculates the vectors and prints results.
    search_terms = request.form["search_terms"]
    query = search_terms.split()
    query = tp.clean_words(query)
    if query == []:
        msg = "Your query was too generic. Try to be more precise or enable \"keep stopwords\" in the settings."
        return render_template("results.html", search_terms=search_terms, message=msg)
    sum_of_weights = query_funcs.calc_sum_of_weights(tp.term_weight_matrix, query)
    if sum_of_weights is None:
        msg = "There were no matches for your search criteria."
        return render_template("results.html", search_terms=search_terms, message=msg)
    doc_vectors = query_funcs.calc_doc_vectors(tp.term_weight_matrix)
    final_output = query_funcs.calc_cosine_similarity(query, sum_of_weights, doc_vectors)
    return render_template("results.html", search_terms=search_terms, results=final_output)  # , results=Query.results


@app.route("/settings")
def settings(msg=""):
    # Page to adjust the settings of the application.
    if tp.language == "english":
        # create a boolean to set language in settings menu with Jinja.
        isenglish = True
    else:
        isenglish = False
    return render_template("settings.html",
                           message=msg,
                           directory=tp.documents_folder,
                           isenglish=isenglish,
                           unwanted_chars=tp.unwanted_chars,
                           enable_stopwords=tp.enable_stopwords,
                           enable_stemmer=tp.enable_stemmer,
                           enable_lemmatizer=tp.enable_lemmatizer)


@app.route("/savedsettings", methods=["GET", "POST"])
def savedsettings():
    # Gets all settings from form on /settings.
    # Then changes settings and creates new matrix accordingly.
    if request.method == "POST":
        if request.form["submit_button"] == "Reset to defaults":
            tp.reset_default_settings()
            message = "Default settings have been reset."
            return settings(message)
        chosen_folder = request.form["folder"]
        if chosen_folder == "":
            chosen_folder = tp.documents_folder
        if not os.path.exists(chosen_folder):
            errormsg = f"folder: {chosen_folder} does not exist!"
            # Reloads settings page with warning if wrong dir name is given.
            return settings(errormsg)
        tp.documents_folder = chosen_folder
        tp.language = request.form["language"]
        tp.unwanted_chars = request.form["unwanted_chars"]
        # empty checkboxes do not return a False boolean so we set
        # values to True/False based on appearance in the form.
        if "enable_stopwords" in request.form:
            print("nu ben ik True")
            tp.enable_stopwords = True
            print(tp.enable_stopwords)
        else:
            print("nu ben ik False")
            tp.enable_stopwords = False
            print(tp.enable_stopwords)
        if "enable_lemmatizer" in request.form:
            tp.enable_lemmatizer = True
        else:
            tp.enable_lemmatizer = False
        if "enable_stemmer" in request.form:
            tp.enable_stemmer = True
        else:
            tp.enable_stemmer = False
        tp.create_term_weight_matrix()
    return render_template("index.html")


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['DEBUG'] = True
    app.config['SERVER_NAME'] = "127.0.0.1:5000"
    app.run(use_reloader=False)
