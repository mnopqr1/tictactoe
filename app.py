from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

#app.config["SESSION_FILE_DIR"] = mkdtemp()  # store temporary session info
#app.config["SESSION_PERMANENT"] = False     # you can set expiry time in a different way
#app.config["SESSION_TYPE"] = "filesystem"   # how to store the session


# Session(app)
app.secret_key = b'\xda\x98c\xc1J\x05\x9d\xc3\xdc\xcb\xce0g\x1d\xd9-'

OTHER = {"X" : "O", "O" : "X" }

def restart_game():
    session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
    session["turn"] = "X"
    session["active"] = True
    session["nmoves"] = 0
    session["draw"] = False

@app.route("/")
def index():
    if "board" not in session:
        restart_game()
    return render_template("game.html", 
        game=session["board"],
        turn=session["turn"],
        active=session["active"],
        draw=session["draw"],
        n=session["nmoves"])

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
    session["nmoves"] += 1
    
    if has_won(session["turn"]):
        session["status"] = "Player " + session["turn"] + " has won! Game over."
        session["active"] = False
    else:
        if session["nmoves"] == 9:
            session["draw"] = True
            session["active"] = False
        else:
            session["turn"] = OTHER[session["turn"]]
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    restart_game()
    return redirect(url_for("index"))