from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        return """
        <h2>Votre demande a bien été envoyée.</h2>

        <p>
        Le service Communication vous contactera prochainement.
        </p>

        <br>

        <a href="/">Faire une nouvelle demande</a>
        """

    return render_template("formulaire.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
