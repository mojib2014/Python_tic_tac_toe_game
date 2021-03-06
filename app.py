from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session 
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

BOARD = [[None, None, None], [None, None, None], [None, None, None]]

@app.route("/")
def index():
    if "board" not in session:
        session["board"] = BOARD
        session["turn"] = "X"
    winner = check_winner(session["board"])
    if winner is not None:
        return render_template("game.html", game=session["board"], turn=session["turn"], winner=winner)
    else:
        return render_template("game.html", game=session["board"], turn=session["turn"])       

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["turn"]
    if session["turn"] == "X":
        session["turn"] = "O"
    else: 
        session["turn"] = "X"
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    session["board"] = BOARD
    session["turn"] = "X"
    return redirect(url_for("index"))


# Check for winner
def check_winner(board):
    # Checking rows
    for row in range(3):
        for col in range(3):
            if board[row][0] is None:
                break
            if board[row][0] == board[row][1] and board[row][1] == board[row][2]:
                return board[row][0]


    # Checking columns
    for row in range(3):
        for col in range(3):
            if board[0][row] is None:
                break
            if board[0][row] == board[1][row] and board[1][row] == board[2][row]:
                return board[0][row]

    # Checking diagonal
    for row in range(3):
        for col in range(3):
            if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
                if board[0][0] is not None:
                    return board[0][0]

    # Checking the oposite diagonal
    for row in range(3):
        for col in range(3):
            if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
                if board[1][1] is not None:
                    return board[1][1]


    return None  