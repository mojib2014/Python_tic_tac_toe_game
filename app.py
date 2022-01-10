from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session 
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    board_not_empty = False
    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
    winner = check_winner(session["board"])
    if winner is not None:
        return render_template("game.html", game=session["board"], turn=session["turn"], winner=winner)
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
    session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
    session["turn"] = "X"
    return redirect(url_for("index"))


# Check for winner
def check_winner(board):
    # Checking rows
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][0] == None:
                break
            if board[row][0] == board[row][1] and board[row][1] == board[row][2]:
                return board[row][0]


    # Checking columns
    for row in range(len(board)):
        for col in range(len(board)):
            if board[0][col] == None:
                break
            if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
                return board[0][col]

    # Checking diagonal
    for row in range(len(board)):
        for col in range(len(board)):
            if board[0][0] == None:
                break
            if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
                return board[0][0]

    # Checking the oposite diagonal
    for row in range(len(board)):
        for col in range(len(board)):
            if board[0][2] == None:
                break
            if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
                return board[0][2]


    return None