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

Most core functionality is now working, including registration, login, quoting, buying, and selling of stocks.  
- The `sell` and `index` routes are implemented and functional.  
- However, the **logic still needs slight adjustments** to ensure stock share totals and portfolio values are fully accurate after a sell — particularly in the `index` view.  
- The `history` route has not yet been completed.

## 🧭 Next Steps

- [ ] Finalize adjustments to `sell` and `index` logic to accurately reflect current portfolio state after sales  
- [ ] Complete the `history` page to show all user transactions with timestamps  
- [ ] Enhance UI with better JavaScript interactivity and input validation  
- [ ] Improve error messaging and form feedback  
- [ ] Finalize README and clean up code for public release

### ⚙️ Prerequisites

- Python 3 installed  
- Flask and CS50 library installed  
- Internet connection (for stock price lookups)

## 📎 Repository Link

[https://github.com/Adamb0lt/CS50-Finance-App](https://github.com/Adamb0lt/CS50-Finance-App)

---

_This project is part of the Harvard CS50x curriculum. It demonstrates practical application of web development, API integration, and database management with Flask._
