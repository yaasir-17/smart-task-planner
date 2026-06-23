from flask import Flask, render_template, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
import sqlite3

app = Flask(__name__)
app.secret_key = "some-random-secret-key"
today = date.today()
today_display = today.strftime("%d/%m/%Y")

def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")
    
    search = request.args.get("search", "").strip()
    sort = request.args.get("sort", "default")

    conn = get_db()

    if search and sort == "priority":
        tasks = conn.execute(
            """
            SELECT *
            FROM tasks
            WHERE user_id = ?
            AND LOWER(title) LIKE LOWER(?)
            ORDER BY completed, priority DESC
            """,
            (
                session["user_id"],
                f"%{search}%"
            )
        ).fetchall()
    elif search and sort == "due_date":
        tasks = conn.execute(
            """
            SELECT *
            FROM tasks
            WHERE user_id = ?
            AND LOWER(title) LIKE LOWER(?)
            ORDER BY completed, due_date
            """,
            (
                session["user_id"],
                f"%{search}%"
            )
        ).fetchall()
    elif search:
        tasks = conn.execute(
            """
            SELECT *
            FROM tasks
            WHERE user_id = ?
            AND LOWER(title) LIKE LOWER(?)
            ORDER BY completed, priority DESC, due_date
            """,
            (
                session["user_id"],
                f"%{search}%"
            )
        ).fetchall()
    elif sort == "priority":
        tasks = conn.execute(
            """
            SELECT *
            FROM tasks
            WHERE user_id = ?
            ORDER BY completed, priority DESC
            """,
            (session["user_id"],)
        ).fetchall()
    elif sort == "due_date":
        tasks = conn.execute(
            """
            SELECT *
            FROM tasks
            WHERE user_id = ?
            ORDER BY completed, due_date
            """,
            (session["user_id"],)
        ).fetchall()
    else:
        tasks = conn.execute(
            """
            SELECT *
            FROM tasks
            WHERE user_id = ?
            ORDER BY completed, priority DESC, due_date
            """,
            (session["user_id"],)
        ).fetchall()
        
    total = conn.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ?", (session["user_id"],)).fetchone()[0]
    pending = conn.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND completed = 0", (session["user_id"],)).fetchone()[0]
    completed = conn.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND completed = 1", (session["user_id"],)).fetchone()[0]
    overdue = conn.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND completed = 0 AND due_date < ?", 
                           (session["user_id"], today)).fetchone()[0]
    recommended = conn.execute("SELECT * FROM tasks WHERE user_id = ? AND completed = 0 ORDER BY priority DESC, due_date LIMIT 1", 
                               (session["user_id"],)).fetchone()

    conn.close()

    due_text = None
    if recommended and recommended["due_date"]:
        due_date = date.fromisoformat(recommended["due_date"])
        days_left = (due_date - today).days
        if days_left < 0:
            due_text = f"Overdue by {-days_left} day(s)"

        elif days_left == 0:
            due_text = "Due Today"

        elif days_left == 1:
            due_text = "Due Tomorrow"

        else:
            due_text = f"Due in {days_left} days"

    return render_template("dashboard.html", tasks=tasks, total=total, pending=pending, completed=completed, overdue=overdue, 
                           today=today.isoformat(), search=search, sort=sort, recommended=recommended, due_text=due_text, 
                           today_display=today_display)

@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect("/")
    
    if request.method == "POST":

        username = request.form.get("username").strip()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return render_template("register.html", error="Username required")
        
        conn = get_db()
        
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user:
            conn.close()
            return render_template("register.html", error="Username already exists")
        if not password:
            conn.close()
            return render_template("register.html", error="Password required")
        if confirmation != password:
            conn.close()
            return render_template("register.html", error="Passwords do not match")
        
        conn.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, generate_password_hash(password)))
        conn.commit()
        conn.close()
        
        return redirect("/")
    
    else:
        return render_template("register.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect("/")
    
    if request.method == "POST":

        username = request.form.get("username").strip()
        password = request.form.get("password")

        if not username:
            return render_template("login.html", error="Username required")
        if not password:
            return render_template("login.html", error="Password requrired")
        
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if not user:
            return render_template("login.html", error="Invalid username and/or password")
        if not check_password_hash(user["hash"], password):
            return render_template("login.html", error="Invalid username and/or password")
        
        session["user_id"] = user["id"]

        return redirect("/")
    
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/add", methods=["POST"])
def add():
    if "user_id" not in session:
        return redirect("/login")
    
    title = request.form.get("title")
    due_date = request.form.get("due_date")
    priority = request.form.get("priority")

    if not title:
        return render_template("dashboard.html", error="Title required")
    
    conn = get_db()
    conn.execute("INSERT INTO tasks (user_id, title, due_date, priority) VALUES (?, ?, ?, ?)", 
                 (session["user_id"], title, due_date, priority))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/complete", methods=["POST"])
def complete():
    if "user_id" not in session:
        return redirect("/login")
    
    id = request.form.get("id")

    conn = get_db()
    conn.execute("UPDATE tasks SET completed = 1 WHERE id = ? AND user_id = ?", (id, session["user_id"]))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    if "user_id" not in session:
        return redirect("/login")
    
    id = request.form.get("id")

    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (id, session["user_id"]))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if "user_id" not in session:
        return redirect("/login")
    
    if request.method == "POST":

        id = request.form.get("id")
        title = request.form.get("title")
        due_date = request.form.get("due_date")
        priority = request.form.get("priority")

        if not title:
            return render_template("edit.html", error="Title required")
        
        conn = get_db() 
        conn.execute("UPDATE tasks SET title = ?, due_date = ?, priority = ? WHERE id = ? AND user_id = ?", 
                     (title, due_date, priority, id, session["user_id"]))
        conn.commit()
        conn.close()
        
        return redirect("/")
    
    else:
        id = request.args.get("id")
        conn = get_db()
        task = conn.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?", (id, session["user_id"])).fetchone()
        conn.close()

        if not task:
            return redirect("/")

        return render_template("edit.html", task=task)

if __name__ == "__main__":
    app.run(debug=True)