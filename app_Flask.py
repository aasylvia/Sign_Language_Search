from flask import Flask, render_template

appFlask = Flask(__name__)

# Route to display search results
@appFlask.route("/")
def show_results():
    global search_results_global
    return render_template("results.html", results=search_results_global)

if __name__ == "__main__":
    appFlask.run(debug=True)
