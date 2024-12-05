from scripts.country_chooser import CountryChooser
from scripts.country_data_manager import DatabaseHandler
from scripts.distance_calculator import DistanceCalculator


class GameLogic:
    def __init__(self, tries, seed):
        self.tries = tries
        self.country_chooser = CountryChooser(seed)
        self.country_data_manager = DatabaseHandler()
        self.distance_calculator = DistanceCalculator()
        self.blur = 50
        self.blur_dec = self.blur / self.tries
        self.guess_options = self.get_guess_options()
        self.num_country = self.country_data_manager.get_row_count()

    def get_guess_options(self):
        return self.country_data_manager.get_countries_names()

    def get_country(self, country_name=None, country_id=None):
        if country_name:
            params = {"country_name": country_name}
        else:
            params = {"index": country_id}
        details = self.country_data_manager.get_country_details(**params)
        country_details = {
            "index": details[0],
            "code": details[1],
            "position": (details[2], details[3]),
            "name": details[4],
            "co2_emission": details[5],
            "population": details[6],
            "deflorest": details[7],
            "consume": details[8],
        }

        return country_details

    def daily_country(self):
        country_id = self.country_chooser.choose(self.num_country)
        return self.get_country(country_id=country_id)

    def guess_distance(self, guess, target):
        return self.distance_calculator.calculate_distance(guess, target)

    def get_blur(self):
        if self.blur < 0:
            self.blur = 0
        else:
            self.blur -= self.blur_dec
        return self.blur

    def try_guess(self, guess, target):
        if guess != "" and guess in self.guess_options:
            if guess.lower() == target.lower():
                return "won"
            else:
                self.tries -= 1
                return "missed"
        return "invalid"
