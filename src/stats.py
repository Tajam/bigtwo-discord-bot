import os
import json
from collections import defaultdict


class Stats:
    def __init__(self):
        self.stats_file = "stats"
        self.point_system = {"0": 1, "1": 0.5, "2": -0.5, "3": -1}

    def read_stats_file(self):
        if os.path.exists(self.stats_file) and os.path.isfile(self.stats_file):
            try:
                stats = json.loads(open(self.stats_file, "r").readline())
            except:
                stats = {}
        else:
            open(self.stats_file, "w")
            stats = {}
        return defaultdict(lambda: {"0": 0, "1": 0, "2": 0, "3": 0}, stats)

    def update_stats(self, winners, players):
        current_stats = self.read_stats_file()
        for place, winner in enumerate(winners):
            current_stats[winner][place] += 1
        for loser in set(players) - set(winners):
            current_stats[loser][3] += 1
        with open(self.stats_file, "w") as sf:
            sf.write(json.dumps(current_stats))

    def get_stats(self, bot, player_id):
        stats = self.read_stats_file()
        places = stats[str(player_id)]
        message = "{:<12}⸾{:^7}⸾{:^5}⸾{:^5}⸾{:^5}⸾{:^7}\n".format(
            f"{bot.get_user(player_id).name}",
            "🧧: " + str(self.calculate_points(places)),
            "🥇: " + str(places["0"]),
            "🥈: " + str(places["1"]),
            "🥉: " + str(places["2"]),
            "🙃: " + str(places["3"]),
        )
        return message

    def calculate_points(self, places):
        total_points = 0
        for index, count in places.items():
            total_points += self.point_system[index] * count
        return total_points
