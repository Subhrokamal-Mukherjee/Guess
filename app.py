import os

from flask import Flask, request, render_template_string, session,redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "secret-key"

HTML = """
<!doctype html>
<title>Guessing Game</title>
<h2>Guess the number (1–100)</h2>

<p>{{ message }}</p>

{% if game_over %}
    <form method="post" action="/restart">
        <button type="submit">Restart Game</button>
    </form>
{% else %}
    <form method="post">
        <input name="guess" autofocus>
        <button type="submit">Submit</button>
    </form>
{% endif %}
"""

def compare_to_target(user_input, target):
    diff = abs(user_input - target)

    if user_input < target:
        if diff > 10:
            return "Too low."
        elif diff > 5:
            return "Close! Too low."
        elif diff > 1:
            return "Almost there! Too low."
        else:
            return "So close! Just a bit higher."

    elif user_input > target:
        if diff > 10:
            return "Too high."
        elif diff > 5:
            return "Close! Too high."
        elif diff > 1:
            return "Almost there! Too high."
        else:
            return "So close! Just a bit lower."

@app.route("/restart", methods=["POST"])
def restart():
    session.clear()
    return redirect(url_for("game"))

@app.route("/", methods=["GET", "POST"])
def game():
    # Initialize like your main()
    if "target" not in session:
        session["target"] = random.randint(1, 100)
        session["anger"] = 0
        session["game_over"] = False

    message = "Enter a number between 1 and 100"

    if request.method == "POST" and not session.get("game_over", False): # Only process if game isn't over
        user_input = request.form.get("guess", "")

        # Handle empty input first (before trying to convert to int)

        if user_input == "" and session["anger"] < 8:
            message = "You didn’t even type anything...\nBe Better"
            session["anger"] += 1

        elif user_input == "" and session["anger"] >= 8:
            message = "I’m done with you."
            session["game_over"] = True

        else:
            try:
                user_input = int(user_input)
            except ValueError:
                message = "Come on..........\nThat’s not even a number!"
                if session["anger"] < 8:
                    session["anger"] += 1
                return render_template_string(
                    HTML,
                    message=message,
                    game_over=session.get("game_over", False)
                )

            if user_input == session["target"]:
                message = "Finally... you got it."
                session["game_over"] = True
                return render_template_string(
                    HTML,
                    message=message,
                    game_over=True
                )

            session["anger"] += 1

            if session["anger"] > 8:
                message = "I’m done with you."
                session["game_over"] = True
                return render_template_string(
                    HTML,
                    message=message,
                    game_over=True
                )

            # anger messages 
            if session["anger"] <= 2:
                message = "Nope."
            elif session["anger"] <= 3:
                message = "Still wrong..."
            elif session["anger"] <= 4:
                message = "Are you even trying?"
            elif session["anger"] <= 5:
                message = "This is getting old."
            elif session["anger"] <= 6:
                message = "This is getting ridiculous."
            else:
                message = "You’re testing my patience."

            # compare_to_target feedback
            feedback = compare_to_target(user_input, session["target"])
            message += " " + feedback

    return render_template_string(
        HTML,
        message=message,
        game_over=session.get("game_over", False)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))