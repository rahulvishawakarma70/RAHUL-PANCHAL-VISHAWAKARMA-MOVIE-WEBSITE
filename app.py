from flask import Flask, render_template, request, redirect, send_from_directory
import os
import sqlite3

app = Flask(__name__)

UPLOAD_FOLDER="static/uploads"
app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER,exist_ok=True)


def db():
    con=sqlite3.connect("movies.db")
    con.execute("""
    CREATE TABLE IF NOT EXISTS movies(
    id INTEGER PRIMARY KEY,
    title TEXT,
    file TEXT
    )
    """)
    return con


@app.route("/")
def home():

    con=db()
    movies=con.execute("select * from movies").fetchall()

    return render_template(
        "index.html",
        movies=movies
    )


@app.route("/upload",methods=["GET","POST"])
def upload():

    if request.method=="POST":

        title=request.form["title"]
        file=request.files["movie"]

        filename=file.filename

        file.save(
        os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
        ))

        con=db()

        con.execute(
        "insert into movies(title,file) values(?,?)",
        (title,filename)
        )

        con.commit()

        return redirect("/")


    return render_template("upload.html")



@app.route("/watch/<int:id>")
def watch(id):

    con=db()

    movie=con.execute(
    "select * from movies where id=?",
    (id,)
    ).fetchone()

    return render_template(
    "watch.html",
    movie=movie
    )



@app.route("/download/<file>")
def download(file):

    return send_from_directory(
    UPLOAD_FOLDER,
    file,
    as_attachment=True
    )


app.run(
host="0.0.0.0",
port=5000
)
