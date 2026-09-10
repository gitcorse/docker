from flask import Flask, render_template_string, request
import mysql.connector

app = Flask(__name__)

# MySQL connection settings
db_config = {
    'host': 'mysql-container',   # use container name if running with docker-compose
    'user': 'root',
    'password': 'password',
    'database': 'mydb'
}

# HTML templates
login_page = """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
  <h2>Login</h2>
  <form method="POST">
    Username: <input type="text" name="username"><br><br>
    Password: <input type="password" name="password"><br><br>
    <input type="submit" value="Login">
  </form>
  {% if error %}
    <p style="color:red;">{{ error }}</p>
  {% endif %}
</body>
</html>
"""

profile_page = """
<!DOCTYPE html>
<html>
<head><title>Profile</title></head>
<body>
  <h2>Welcome, {{ username }}!</h2>
  <p>This is your profile page.</p>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            return render_template_string(profile_page, username=user["username"])
        else:
            error = "Try again: invalid username or password."

    return render_template_string(login_page, error=error)

if __name__ == "__main__":
    # Explicitly define port 8080
    app.run(host="0.0.0.0", port=8080, debug=True)
