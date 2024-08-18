from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session,url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import image
app = Flask(__name__)
db = SQL("sqlite:///user.db")
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.secret_key = 'w1l2'



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")
        diet = request.form.get("dite")
        intolerance = []
        intolerance1=["Dairy","Egg","Gluten","Grain","Peanut","Seafood"]
        intolerance2=["Sesame","Shellfish","Soy","Sulfite","Tree Nut","Wheat"]
        for item in intolerance1 + intolerance2:
            if request.form.get(f"checkbox_{item}"):
                intolerance.append(item)   

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if password != confirm:
            flash("password and confirmation are not match")
            #return redirect(url_for("register"))
            return "passwoe"
            
        elif not password:
            flash("password is required")
            return redirect(url_for("register"))
        elif not username:
            flash("username required")
            return redirect(url_for("register"))
            
        elif rows:
            flash("user name already taken")
            return redirect(url_for("register"))
        else:
            diet= "".join(diet)
            intolerance=", ".join(intolerance)
            hash_password=generate_password_hash(password)
          
            
           
            values = [username, hash_password, diet, intolerance]

            sql = "INSERT INTO users (username, password, diet, intolerance) VALUES (?, ?, ?, ?)"

            db.execute(sql, *values)

            rows = db.execute(
                "SELECT * FROM users WHERE username = ?", request.form.get("username")
            )
            session["user_id"] = rows[0]["id"]
            return redirect("/")

    else:
        dite=["Gluten Free","Ketogenic","Vegetarian","Lacto-Vegetarian","Ovo-Vegetarian","Vegan","Pescetarian","Paleo","Primal","Low FODMAP","Whole30"]
        intolerance1=["Dairy","Egg","Gluten","Grain","Peanut","Seafood"]
        intolerance2=["Sesame","Shellfish","Soy","Sulfite","Tree Nut","Wheat"]
        return render_template("register.html",dite=dite,intolerance1=intolerance1,intolerance2=intolerance2)
#end of reigster
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""



    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("provide username")
            return redirect(url_for("login"))
           

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("provide password")
            return redirect(url_for("login"))
            
        # Forget any user_id
        session.clear()
        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("password")
        ):
            flash("invalid username and/or password")
            return redirect(url_for("login"))
           

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")
@app.route("/password", methods=["GET", "POST"])

def password():
    if request.method == "GET":
        return render_template("password.html")
    else:

        if not request.form.get("oldpassword") and not request.form.get("newpassword") and not request.form.get("username"):
            flash("provide username , oldpassword and newpassword")
            return redirect(url_for("password"))

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("oldpassword")
        ):
           flash("invalid username and/or old password")
           return redirect(url_for("password"))  
            
        
        else:
            new = generate_password_hash(request.form.get('newpassword'))
            db.execute(
                "UPDATE users SET password = ? WHERE username = ?",
                new, request.form.get('username')
            )

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

@app.route("/", methods=["GET", "POST"])
def home():
    user_id = session.get("user_id")
    from_users = db.execute("SELECT * FROM users WHERE id = :id", id=user_id)
    print(from_users)
    if request.method == "GET":
        if from_users:
            diet=from_users[0]['diet']
            intolerance=from_users[0]['intolerance']

            image_list=image(diet,intolerance)
            print(image_list)
            url=[]
            
            for urls in image_list:
                try:
                    url.append(urls['url'])
                except (TypeError, KeyError, IndexError, AttributeError) as e:
                    pass
            return render_template("home.html",image=url)
        else:
            
            return redirect("/register")

    else:

        if request.form.get('save'):  # Handle image saving
            if user_id:  # Ensure user is logged in
                save = request.form.get('save')
                values = [user_id,save]


                sql = "INSERT INTO save (user_id, url) VALUES (?, ?)"

                db.execute(sql, *values)
                
                return {"success": True}, 200  # Respond to AJAX with success
            
        return redirect("/")
     

    
@app.route("/search", methods=["GET", "POST"])
def search():
    user_id = session.get("user_id")
    from_users = db.execute("SELECT * FROM users WHERE id = :id", id=user_id)
    
    if request.method == "POST":
        if request.form.get("query"):  # Handle search query
            if from_users:
                diet = from_users[0]['diet']
                intolerance = from_users[0]['intolerance']
                query = request.form.get("query")

                image_list = image(diet, intolerance, query)
                images = []

                for img in image_list:                
                    try:
                        images.append(img['url'])
                    except (TypeError, KeyError, IndexError, AttributeError):
                        pass
                
                return render_template("search.html", image=images)
            else:
                return redirect("/register")
        
        elif request.form.get('save'):  # Handle image saving
            if user_id:  # Ensure user is logged in
                save = request.form.get('save')
                values = [user_id,save]


                sql = "INSERT INTO save (user_id, url) VALUES (?, ?)"

                db.execute(sql, *values)
                
                return {"success": True}, 200  # Respond to AJAX with success
            
    return render_template("search.html")  # Render the search page for GET requests
         



         
@app.route("/save")
def save(): 
    user_id = session.get("user_id")
    from_save = db.execute("SELECT url FROM save WHERE user_id = :id", id=user_id)
    saved=[]
    print(saved)
    for save in from_save:
       saved.append(save['url'])


    
    if from_save:
        return render_template("save.html",image=saved)
    else: 
        return render_template("save.html")

      

    
