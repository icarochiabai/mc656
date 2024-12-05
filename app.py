from flask import Flask, render_template, request, redirect, url_for
from scripts.game_logic import GameLogic
import random

app = Flask(__name__)
guesses = []
has_won = False
has_lost = False
seed = "engenharia de software melhor materia <3"

@app.route("/", methods=['GET', 'POST'])
def home():
    global game_logic
    global country
    global guesses
    global has_won
    global has_lost
    game_logic = GameLogic(5, seed)
    country = game_logic.daily_country()

    if len(guesses) != 0:
            guess_pos = game_logic.get_country(country_name=guesses[-1][0])["position"]
            target_pos = country["position"]
            dist = game_logic.distance_calculator.calculate_distance(guess_pos, target_pos)
            guesses[-1].append(dist)
            guesses[-1].append(5 - len(guesses))

            if guesses[-1][0] == country["name"]:
                has_won = True
            elif len(guesses) == 5:
                has_lost=True
                guesses=[]

    blur = game_logic.get_blur()
    blur_dec = blur / 5
    return render_template("index.html",
                            code=country["code"],
                            name=country["name"],
                            co2_emission=country["co2_emission"],
                            population=country["population"],
                            consume=country["consume"],
                            deflorest=country["deflorest"],
                            blur=blur - (len(guesses) + 1) * blur_dec,
                            countries=game_logic.get_guess_options(),
                            guesses=guesses,
                            has_won=has_won,
                            has_lost=has_lost
                            )

@app.route('/guess', methods=['POST'])
def guess_country():
    global game_logic
    global country
    global guesses
    guess = request.form.get('country')
    case = game_logic.try_guess(guess, country["name"])
    if case != "invalid":
        guesses.append([guess])
    
    return redirect(url_for('home'))

@app.route('/reset', methods=['POST'])
def reset():
    global guesses
    global has_won
    global seed
    global has_lost
    guesses = []
    if has_won:
        seed = ''.join(random.choices('0123456789', k=8))
        print(seed)
        has_won = False
    has_lost = False

    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
