from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()  # store temporary session info
app.config["SESSION_PERMANENT"] = False     # you can set expiry time in a different way
app.config["SESSION_TYPE"] = "filesystem"   # how to store the session
Session(app)

OTHER = {"X" : "O", "O" : "X" }

@app.route("/")
def index():
    if "board" not in session or session["reset"]:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
        session["status"] = "It's X's turn."
        session["active"] = True
        session["reset"] = False
    return render_template("game.html", 
        game=session["board"],
        turn=session["turn"], 
        status=session["status"],
        active=session["active"])

def has_won(player):
    board = session["board"]
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
    for j in range(3):
        if all(board[i][j] == player for i in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2-i] == player for i in range(3)):
        return True
    return False

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["turn"]
    
    if has_won(session["turn"]):
        session["status"] = "Player " + session["turn"] + " has won! Game over."
        session["active"] = False
    else:
        session["turn"] = OTHER[session["turn"]]
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    session["reset"] = True
    return redirect(url_for("index"))