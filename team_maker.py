import random
from typing import List


class TeamMaker:
    def __init__(self, players: List, teams_num=3, distinct_players=["huhu", "lala"], players_match=None) -> None:
        self.players = players
        self.teams_num = teams_num
        self.player_stats = [[player, {"GK_count": 0, "play_count": 0}] for player in self.players]
        self.distinct_players = distinct_players
        self.players_match = players_match

    def choice_team(self):
        while True:
            teams = self._distribute_players(self.players, self.teams_num)
            retry = 0
            for team in teams:
                if (self.distinct_players[0] in team) & (self.distinct_players[1] in team):
                    retry = 1
            if not retry:
                break
        return teams

    def _distribute_players(self, players, num_teams=3):
        random.shuffle(players)

        teams = [[] for _ in range(num_teams)]
        for i, player in enumerate(players):
            team_index = i % num_teams
            teams[team_index].append(player)
        return teams

    def _where_man(self, num, data):
        for i, sublist in enumerate(data):
            if sublist[0] == num:
                return i

    def allocate_position_per_game(self, team):
        players = team
        players = sorted(players)

        positions = ["LW", "FW", "RW", "LM", "CM", "RM", "LB", "LCB", "RCB", "RB", "GK"]
        players_per_game = 11
        num_games = 4

        game = {}
        for i in range(1, num_games + 1):
            random.shuffle(self.player_stats)
            self.player_stats = sorted(self.player_stats, key=lambda x: x[1]["play_count"])
            this_game_player = self.player_stats[:players_per_game]

            while True:
                this_game_position = {}
                for ps, man in zip(positions, this_game_player):
                    this_game_position[ps] = self.players_match[man[0]]
                    # 골키퍼되면 GK count 증가
                    if ps == "GK":
                        where_is_gk = self._where_man(man[0], self.player_stats)
                        self.player_stats[where_is_gk][1]["GK_count"] += 1

                # 이미 골키퍼 한적 있으면 다시!
                try:
                    if self.player_stats[where_is_gk][1]["GK_count"] > 1:
                        self.player_stats[where_is_gk][1]["GK_count"] -= 1
                        random.shuffle(this_game_player)
                    else:
                        # 제대로 골키퍼 선정되었으면, 이번 게임참가자들 play count 증가
                        for man in this_game_player:
                            where_is_man = self._where_man(man[0], self.player_stats)
                            self.player_stats[where_is_man][1]["play_count"] += 1
                        break
                except UnboundLocalError as e:
                    print(self.players)
                    print("------------------------")
                    print(self.players_match)
                    break

            game[i] = this_game_position
        return game
