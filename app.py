from flask import Flask, render_template, request, redirect, url_for
from scripts.game_logic import GameLogic

app = Flask(__name__)
guesses = []
has_won = False

@app.route("/", methods=['GET', 'POST'])
def home():
    global game_logic
    global country
    global guesses
    global has_won
    game_logic = GameLogic(5)
    country = game_logic.daily_country()
    if len(guesses) != 0:
            guess_pos = game_logic.get_country(country_name=guesses[-1][0])["position"]
            target_pos = country["position"]
            dist = game_logic.distance_calculator.calculate_distance(guess_pos, target_pos)
            guesses[-1].append(dist)
            guesses[-1].append(5 - len(guesses))
            print(guesses)
            if guesses[-1][0] == country["name"]:
                has_won = True
                print("OASIKDOIAS")
            if len(guesses) == 5 and not has_won:
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
                            blur=blur - len(guesses) * blur_dec,
                            countries=game_logic.get_guess_options(),
                            guesses=guesses,
                            has_won=has_won
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

if __name__ == "__main__":
    app.run(debug=True)
