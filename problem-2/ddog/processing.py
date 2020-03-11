import itertools

import numpy as np


class TripletCounter:
    def __init__(self, min_player_count):
        self.min_player_count = min_player_count

    def compute(self, df):
        df = df.drop_duplicates()

        df['team-id'] = np.where(df.league.isna(), df.team, df.team + '-' + df.league)

        df_agg = df.groupby('player', as_index=False) \
            .agg(team_count=('team-id', 'count'), teams=('team-id', list))

        df_agg = df_agg[df_agg.team_count >= 3]

        team_triplet_counter = dict()
        for player_teams in df_agg.teams:
            player_team_triplets = itertools.combinations(player_teams, r=3)
            for team_triplet in player_team_triplets:
                key = frozenset(team_triplet)
                current_triplet_count = team_triplet_counter.get(key, 0)
                team_triplet_counter[key] = current_triplet_count + 1

        return [(triplet, count) for triplet, count in team_triplet_counter.items() if count >= self.min_player_count]
