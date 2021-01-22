from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results", methods = ["POST"])
def results():
    query = request.form["query"]
    return render_template("results.html", query = query)


@app.route("/settings")
def settings():
    return render_template("settings.html")

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['DEBUG'] = True
    app.config['SERVER_NAME'] = "127.0.0.1:5000"
    app.run()
