import sqlite3
from flask import *
from werkzeug.security import generate_password_hash, check_password_hash
import db
import secrets
import users

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# main page

@app.route("/")
def mainapge():
    db.execute("INSERT INTO visits (visited_at) VALUES (datetime('now'))")

    visit_ammount = (db.query("SELECT COUNT(*) FROM visits"))[0][0]
    last_visit = db.query("SELECT visited_at FROM visits ORDER BY visited_at DESC LIMIT 1")[0][0]

    recipes = db.query("SELECT title, ingredients, instructions FROM recipes")

    return render_template("mainpage.html", visits = visit_ammount, date = last_visit,
                           recipes = recipes, n = len(recipes))

# user

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

    if request.method == "POST":
        username = request.form["username"]
        if len(username) > 16:
            abort(403)
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        # could add password checking feature 
        # ie password has to be at least n chracters long...

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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", next_page=request.referrer)

    if request.method == "POST":
        global username
        username = request.form["username"]
        password = request.form["password"]
        #next_page = request.form["next_page"] # doesnt work???
        next_page = "/"

        user_id = users.check_login(username, password)

        if user_id:
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
            return redirect(next_page)
        
        else:
            flash("VIRHE: Väärä tunnus tai salasana")
            return render_template("login.html", next_page=next_page)

@app.route("/logout")
def logout():
    del session["user_id"]
    flash("Olet kirjautunut ulos.")
    return redirect("/")

# posts

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    title = request.form["title"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]

    db.execute("INSERT INTO recipes(title, ingredients, instructions) VALUES(?, ?, ?)",
               [title, ingredients, instructions])
    return redirect("/")