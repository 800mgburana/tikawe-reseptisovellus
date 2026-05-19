import sqlite3
from flask import *
from werkzeug.security import generate_password_hash
import db
import config

app = Flask(__name__)

# main page

@app.route("/")
def mainapge():
    db.execute("INSERT INTO visits (visited_at) VALUES (datetime('now'))")

    visit_ammount = (db.query("SELECT COUNT(*) FROM visits"))[0][0]
    last_visit = db.query("SELECT visited_at FROM visits ORDER BY visited_at DESC LIMIT 1")[0][0]
    return render_template("mainpage.html", visits = visit_ammount, date = last_visit)

# user

# could add password checking feature 
# ie password has to be at least n chracters long...

@app.route("/register", methods=["GET", "POST"])
def register():  # вроде работает
    if request.method == "GET":
        return render_template("register.html", filled={})

    if request.method == "POST":
        username = request.form["username"]
        if len(username) > 16:
            abort(403)
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            flash("VIRHE: Antamasi salasanat eivät ole samat")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

        try:
            password_hash = generate_password_hash(password1)
            db.execute("INSERT INTO users(username, password_hash) VALUES(?, ?)", 
                       (username, password_hash))
            flash("Tunnuksen luominen onnistui, voit nyt kirjautua sisään")
            return redirect("/")

        except sqlite3.IntegrityError:
            flash("VIRHE: Valitsemasi tunnus on jo varattu")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

@app.route("/login")
def login():
    pass



