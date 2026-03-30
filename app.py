from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Création de la base si elle n'existe pas
def init_db():
    conn = sqlite3.connect("evenements.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS demandes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_demande TEXT,
        nom TEXT,
        prenom TEXT,
        email TEXT,
        telephone TEXT,
        service TEXT,
        evenement TEXT,
        date_souhaitee TEXT,
        lieu TEXT,
        participants TEXT,
        invites TEXT,
        centre_cout TEXT,
        budget TEXT,
        statut TEXT DEFAULT 'Nouveau',
        assignes TEXT DEFAULT ''
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        date_demande = datetime.now().strftime("%d/%m/%Y")

        conn = sqlite3.connect("evenements.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO demandes (
            date_demande,
            nom,
            prenom,
            email,
            telephone,
            service,
            evenement,
            date_souhaitee,
            lieu,
            participants,
            invites,
            centre_cout,
            budget
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            date_demande,
            request.form.get("nom"),
            request.form.get("prenom"),
            request.form.get("email"),
            request.form.get("telephone"),
            request.form.get("service"),
            request.form.get("evenement"),
            request.form.get("date_souhaitee"),
            request.form.get("lieu"),
            request.form.get("participants"),
            request.form.get("invites"),
            request.form.get("centre_cout"),
            request.form.get("budget")

        ))

        conn.commit()
        conn.close()

        return """
        <h2>Votre demande a bien été envoyée.</h2>

        <p>
        Le service Communication vous contactera prochainement.
        </p>

        <br>

        <a href="/">Faire une nouvelle demande</a>
        <br><br>
        <a href="/dashboard">Accéder au Dashboard</a>
        """

    return render_template("formulaire.html")


@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("evenements.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM demandes ORDER BY id DESC")

    demandes = cursor.fetchall()

    conn.close()

    return render_template("dashboard.html", demandes=demandes)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
