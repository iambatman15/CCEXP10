from flask import Flask, render_template, request, redirect
import os
import psycopg2
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

# Load environment variables
load_dotenv()

app = Flask(__name__)

# PostgreSQL configuration
DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS entries (id SERIAL PRIMARY KEY, content TEXT)")
conn.commit()

# Cloudinary configuration
cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET')
)

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

@app.route("/upload", methods=["POST"])
def upload():
    file_to_upload = request.files['file']
    if file_to_upload:
        upload_result = cloudinary.uploader.upload(file_to_upload)
        url = upload_result['secure_url']
        return f"✅ File uploaded: <a href='{url}' target='_blank'>{url}</a>"
    return "❌ No file uploaded."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
