from app import app
from flask import render_template, request, redirect
import messages, users

@app.route("/")
def index():
    list_messages = messages.get_list()
    list_categories = messages.get_categories()
    return render_template("index.html", count_messages=len(list_messages), messages=list_messages,
                            count_categories=len(list_categories), categories=list_categories)

@app.route("/<name>")
def category_page(name):
    category = messages.check_categories(name)
    list_threads = messages.get_list_for_category(category[1])
    if category is None:
        return redirect("/")
    return render_template("category.html", category=category, count_threads=len(list_threads),
                            threads=list_threads)

@app.route("/<category_name>/<int:thread_id>")
def thread_page(category_name, thread_id):
    category = messages.check_categories(category_name)
    thread = messages.check_threads(thread_id)
    list_messages = messages.get_list_for_thread(thread_id)
    if category is None or thread is None:
        return redirect("/")
    return render_template("thread.html", category=category, thread=thread, messages=list_messages,
                            count_messages=len(list_messages))

@app.route("/<category_name>/<int:thread_id>/send", methods=["POST"])
def send(category_name, thread_id):
    category_id = request.form["category_id"]
    thread_id = request.form["thread_id"]
    content = request.form["content"]
    if messages.send(content, category_id, thread_id):
        return redirect(f"/{category_name}/{thread_id}")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")