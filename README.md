# CS50 Finance App

A full-stack stock trading web application built as part of [CS50x](https://cs50.harvard.edu/x/)'s Week 9 "Finance" project. The app allows users to register, log in, look up real-time stock prices, buy and sell stocks, and view their portfolio and transaction history.

## 🚀 Features

- ✅ User registration and login with secure password hashing  
- ✅ Real-time stock lookup using CS50’s stock quote API (a wrapper over IEX Cloud’s free tier)  
- ✅ Ability to buy and sell shares based on live pricing  
- ✅ Portfolio overview showing current holdings and remaining cash  
- ✅ Transaction history logging all buy/sell actions  
- ✅ Responsive UI built with HTML, CSS, and JavaScript  
- ✅ Server-side validation and error handling with Flask and Jinja templates  
- ✅ SQLite database integration using CS50’s `SQL` helper  

## 🛠️ Technologies Used

- Python (Flask)  
- SQLite (SQL)  
- HTML, CSS, JavaScript  
- CS50 Finance API (wrapper over IEX Cloud)  
- Jinja templating  
- Bootstrap (for styling)  

## 📁 Project Structure

- `app.py` – Main Flask application containing routes and app logic  
- `helpers.py` – Utility functions: apology messages, login decorators, API lookup, USD formatting  
- `templates/` – Jinja2 HTML templates (e.g., layout.html, quote.html, register.html)  
- `static/` – Static assets like custom CSS or JavaScript files (optional)  
- `finance.db` – SQLite database file storing user info, transactions, and user portfolio data  
- `README.md` – This file (project overview, instructions, structure, & next steps)  

## 📍 Current Status

All core routes are fully implemented and functional:  
- `register`, `login`, `logout`, `quote`, `buy`, `sell`, and the `index` page all work as expected  
- Share quantities and portfolio values update correctly after selling  
- Only the `history` route remains to be completed

## ▶️ How to Run the App

1. **Ensure prerequisites are installed**:
    - Python 3  
    - Flask  
    - CS50 library  
2. **Navigate to the project folder** in your terminal  
3. **Run the Flask app**:
    ```bash
    flask run
    ```
4. **Visit the provided URL** (e.g., `http://127.0.0.1:5000`) in your browser to access the app

> Note: You must be connected to the internet for stock price lookups to work via the CS50 Finance API.

## 🧭 Next Steps

- [ ] Build out the `history` page to show all user transactions with timestamps  
- [ ] Enhance UI with JavaScript interactivity and input validation  
- [ ] Improve error messaging and form feedback  
- [ ] Final polish and code cleanup for public release  

### ⚙️ Prerequisites

- Python 3  
- Flask and CS50 library installed  
- Internet connection (for real-time stock data)

## 📎 Repository Link

[https://github.com/Adamb0lt/CS50-Finance-App](https://github.com/Adamb0lt/CS50-Finance-App)

---

_This project is part of the Harvard CS50x curriculum. It demonstrates practical application of web development, API integration, and database management with Flask._
