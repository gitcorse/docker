import os
import time
import mysql.connector
from flask import Flask, render_template_string, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "super_secret_python_key"

# Database Connection Helper
def get_db_connection():
    return mysql.connector.connect(
        host="mysql-server",      # Container name from docker-compose
        user="root",
        password="password",
        database="mydb"
    )

# Wait for MySQL to start and initialize the database table
def init_db():
    db_connected = False
    while not db_connected:
        try:
            print("Python App: Connecting to MySQL database...")
            db = get_db_connection()
            cursor = db.cursor()
            
            # Create uploads table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS image_uploads (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    image_name VARCHAR(255) NOT NULL,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            db.commit()
            cursor.close()
            db.close()
            db_connected = True
            print("Python App: Database initialized successfully!")
        except mysql.connector.Error as err:
            print(f"Database waiting... ({err})")
            time.sleep(3)

# HTML Template Embedded Directly
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Web1 - Python Image Uploader</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f2f5; }
        .container { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h2 { color: #333; margin-top: 0; }
        .form-group { margin-bottom: 15px; }
        input[type="text"] { width: 100%; padding: 10px; box-sizing: border-box; margin-top: 5px; }
        button { background-color: #007bff; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .alert { padding: 10px; background-color: #d4edda; color: #155724; border-radius: 4px; margin-bottom: 15px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f8f9fa; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🐍 Python Image Uploader (Web 1)</h2>
        
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for message in messages %}
              <div class="alert">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        <form method="POST" action="/upload">
            <div class="form-group">
                <label for="image_name"><strong>Enter Image Name / URL to Upload to Database:</strong></label>
                <input type="text" id="image_name" name="image_name" placeholder="e.g. my_photo.png" required>
            </div>
            <button type="submit">Upload Image Record</button>
        </form>

        <hr style="margin: 25px 0;">

        <h3>Uploaded Images in Database</h3>
        <table>
            <tr>
                <th>ID</th>
                <th>Image Name</th>
                <th>Uploaded At</th>
            </tr>
            {% for image in images %}
            <tr>
                <td>{{ image[0] }}</td>
                <td>{{ image[1] }}</td>
                <td>{{ image[2] }}</td>
            </tr>
            {% else %}
            <tr>
                <td colspan="3">No images uploaded yet.</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT id, image_name, uploaded_at FROM image_uploads ORDER BY id DESC")
    images = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template_string(HTML_TEMPLATE, images=images)

@app.route('/upload', methods=['POST'])
def upload_image():
    image_name = request.form.get('image_name')
    if image_name:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO image_uploads (image_name) VALUES (%s)", (image_name,))
        db.commit()
        cursor.close()
        db.close()
        flash(f"Successfully uploaded '{image_name}' to Database!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    # Runs the web app on port 5000 inside the container
    app.run(host='0.0.0.0', port=5000)