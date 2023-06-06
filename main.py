from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from dotenv import load_dotenv
import os

db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_port = os.getenv("DB_PORT")

connection = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password, port=db_port)
cur = connection.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    book VARCHAR(255),
    author VARCHAR(255),
    rating INT
)""")

cur.execute("CREATE SEQUENCE IF NOT EXISTS books_id_seq")
connection.commit()

cur.execute("ALTER TABLE books ALTER COLUMN id SET DEFAULT nextval('books_id_seq')")
connection.commit()

app = Flask(__name__)

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
app.template_folder = template_dir

@app.route('/')
def home():
    cur.execute("SELECT * FROM books")
    rows = cur.fetchall()
    return render_template("index.html", rows=rows)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        cur.execute("INSERT INTO books (book, author, rating) VALUES (%s, %s, %s)",
                     (request.form["title"], request.form["author"], request.form["rating"]))
        connection.commit()
        return redirect(url_for("home"))
    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)

cur.close()
connection.close()