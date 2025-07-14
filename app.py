from flask import Flask, render_template, request
from queue_model import mm1_model

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            lmbda = float(request.form["lambda"])
            mu = float(request.form["mu"])
            result = mm1_model(lmbda, mu)
        except ValueError:
            result = {"error": "Input harus berupa angka."}
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
