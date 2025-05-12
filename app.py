import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, init_db

# Configure application
app = Flask(__name__)
init_db() # initialize extra tables for db

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    user_id = session["user_id"]

    # Get user cash
    user_info = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    cash = user_info[0]["cash"]

    # Get user's transactions
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)

    # List to store portfolio entries
    portfolio = []

    # keep track of total stock price overall
    running_total = 0

    # TODO: Build out logic to differentiate totals for different companies
    # TODO: Update cash balance
    # Go through each unique stock the user has
    for row in transactions:
        symbol = row["symbol"]
        shares = row["shares"]
        stock_info = lookup(symbol)
        name = stock_info["name"]
        price = float(row["price"])
        total = price * shares
        running_total += total

        portfolio.append({
            "name": name,
            "symbol": symbol,
            "shares": shares,
            "price": usd(price),
            "total": usd(total),
            "running_total": usd(running_total)
        })

    return render_template("index.html", portfolio=portfolio, cash=usd(cash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # get the symbol that the user submits
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # authenticate that symbol is legit
        stock = lookup(symbol)
        if not stock or not symbol:
            return apology("Invalid or missing stock symbol", 400)
        # for fun, dont really need try except


        try:
            shares = float(shares)
            if shares <= 0:
                return apology("Number of shares isn't positive integer", 400)
        except (ValueError, TypeError):
            return apology("You didn't enter a number for the shares", 400)



        # perform SQL check to access how much cash the user has
        # this is the same as trying to get request.form.get("username") from the login page
        # session["user_id"] is global so not affected by scope
        user_id = session["user_id"]

        # store info on user that can be used later on to access variables to place in another table
        user_info = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        total_price = shares * float(stock["price"])

        if total_price > user_info[0]["cash"]:
            return apology("You don't have enough funds", 400)
        # I added in the three quotes so that the multi-line string is read for db statement
        # Create the table if it doesn't exist, if it does, add user date in
        # probably will need rules or store info in variables and then add in table

        # Try for a transaction that is found in other forms of SQL
        try:

            # start transaction
            db.execute("BEGIN")

            # add users within table( I could technically have them added every time a new account is successfully created)
            db.execute("""
                INSERT INTO transactions (user_id, symbol, shares, price, type, cash_balance)
                VALUES (?, ?, ?, ?, 'buy', ?)
            """, user_id, symbol, shares, total_price, user_info[0]["cash"] - total_price)

            # Update user total cash balance from user's after they buy or sell stock
            db.execute("""
                UPDATE users
                SET cash = cash - ?
                WHERE id = ?
            """, total_price, user_id)

            db.execute("COMMIT")

        except Exception as e:
            db.execute("ROLLBACK")
            return apology("Transaction failed", 400)


        # go back to home page once everything is done
        return redirect("/")



    else:
        # render page for when user clicks buy
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

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
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # get the value submitted for symbol
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Need a symbol", 400)
        # TODO: may also need something to ensure that a valid symbol is submitted
        stock = lookup(symbol)
        print(stock)

        if not stock:
            return apology("Not a valid stock")

        # check if the symbol the user sent is legitimate. If not
        # once quote submitted. redirect to quoted.html and supply the symbol from quote
        return redirect(f"/quoted?symbol={symbol}")
    else:
        return render_template("quote.html")

@app.route("/quoted", methods=["GET"])
@login_required
def quoted():

    # this searches for the symbol from the quote route
    # search for the symbol from quote
    symbol = request.args.get("symbol")
    stock = lookup(symbol)

    # present the Company name, symbol and price

    company = stock["name"]
    symbol = stock["symbol"]
    price = stock["price"]
    print(price, symbol, company)

    # also utilize the usd function from helper to convert price properly if needed

    return render_template("quoted.html", company=company, symbol=symbol, price=price)



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # TODO: build in functionality for ensuring password and confirmation of password are matches before register works
        # get username and password. also username not case sensitive for now
        username = request.form.get("username").lower()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # checks if username, password, or confirmation was given
        for value, label in [(username, "username"), (password, "password"), (confirmation,"confirmation")]:
            if not value:
                return apology(f"Must provide {label}", 400)

        # select all usernames that exist and if username registered is in there dubb the user
        rows = db.execute("SELECT * FROM users WHERE username = ?", username.lower())
        if len(rows) != 0:
            return apology("username already exists", 400)
        if password != confirmation:
            return apology("passwords don't match", 400)

        # create a hashed password for the user
        hash_password = generate_password_hash(password)

        # insert into db the hash password and username
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username.lower(), hash_password)

        # once done, send them back to login page to login
        return redirect("/login")

    else:
        # for users to visit the page as a get request which happens first
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # get the symbol that the user submits
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # authenticate that symbol is legit
        stock = lookup(symbol)
        if not stock or not symbol:
            return apology("Invalid or missing stock symbol", 400)
        # for fun, dont really need try except


        try:
            shares = float(shares)
            if shares <= 0:
                return apology("Number of shares isn't positive integer", 400)
        except (ValueError, TypeError):
            return apology("You didn't enter a number for the shares", 400)



        # perform SQL check to access how much cash the user has
        # this is the same as trying to get request.form.get("username") from the login page
        # session["user_id"] is global so not affected by scope
        user_id = session["user_id"]

        # store info on user that can be used later on to access variables to place in another table
        user_info = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        total_price = shares * float(stock["price"])

        if total_price > user_info[0]["cash"]:
            return apology("You don't have enough funds", 400)
        # I added in the three quotes so that the multi-line string is read for db statement
        # Create the table if it doesn't exist, if it does, add user date in
        # probably will need rules or store info in variables and then add in table

        # Try for a transaction that is found in other forms of SQL
        try:

            # start transaction
            db.execute("BEGIN")

            # add users within table( I could technically have them added every time a new account is successfully created)
            db.execute("""
                INSERT INTO transactions (user_id, symbol, shares, price, type, cash_balance)
                VALUES (?, ?, ?, ?, 'buy', ?)
            """, user_id, symbol, shares, total_price, user_info[0]["cash"] - total_price)

            # Update user total cash balance from user's after they buy or sell stock
            db.execute("""
                UPDATE users
                SET cash = cash - ?
                WHERE id = ?
            """, total_price, user_id)

            db.execute("COMMIT")

        except Exception as e:
            db.execute("ROLLBACK")
            return apology("Transaction failed", 400)


        # go back to home page once everything is done
        return redirect("/")



    else:
        # render page for when user clicks buy
        return render_template("buy.html")
