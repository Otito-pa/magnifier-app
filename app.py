from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'HEAD', 'POST'])from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(name)
app.secret_key = 'your_secret_key'

# Setup database
def setup_database():
    conn = sqlite3.connect("specimens.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS specimen_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            specimen_name TEXT NOT NULL,
            microscope_size REAL NOT NULL,
            magnification REAL NOT NULL,
            actual_size REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Home Route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            username = request.form["username"]
            specimen = request.form["specimen"]
            microscope_size = float(request.form["microscope_size"])
            magnification = float(request.form["magnification"])

            if magnification <= 0:
                flash("Magnification must be greater than 0.")
                return redirect("/")

            actual_size = microscope_size / magnification

            conn = sqlite3.connect("specimens.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO specimen_data (username, specimen_name, microscope_size, magnification, actual_size)
                VALUES (?, ?, ?, ?, ?)
            """, (username, specimen, microscope_size, magnification, actual_size))
            conn.commit()
            conn.close()

            flash(f"Saved successfully! Real-life size: {actual_size:.4f} μm")
            return redirect("/")
        except:
            flash("Error: Please enter valid data.")
            return redirect("/")

    return render_template("index.html")

if name == "main":
    setup_database()
    app.run(debug=True)
def calculate():
    result = None
    username = None
    error = None  # Initialize error variable
    
    if request.method == 'POST':
        try:
            # Retrieve form data
            username = request.form['username']
            microscope_size = float(request.form['microscope_size'])
            magnification = float(request.form['magnification'])
            
            # Validate magnification
            if magnification == 0:
                error = "Magnification cannot be zero"
            else:
                # Perform the calculation
                result = f"{microscope_size / magnification:.2f}"
                
        except ValueError:
            error = "Please enter valid numbers"
    
    # For 'HEAD' requests, you can just return a minimal response without rendering the template
    if request.method == 'HEAD':
        return '', 200  # Empty response with status code 200
    
    # For 'GET' and 'POST' requests, render the template with results or errors
    return render_template('microscope.html', 
                         result=result, 
                         username=username,
                         error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
