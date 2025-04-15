from flask import Flask, render_template, request, redirect
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Connect to PostgreSQL database
DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Create table if not exists
cur.execute("CREATE TABLE IF NOT EXISTS entries (id SERIAL PRIMARY KEY, content TEXT)")
conn.commit()

@app.route("/", methods=["GET"])
def index():
    cur.execute("SELECT content FROM entries")
    data = [row[0] for row in cur.fetchall()]
    return render_template("index.html", data_list=data)

@app.route("/submit", methods=["POST"])
def submit():
    content = request.form["data"]
    if content:
        cur.execute("INSERT INTO entries (content) VALUES (%s)", (content,))
        conn.commit()
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

