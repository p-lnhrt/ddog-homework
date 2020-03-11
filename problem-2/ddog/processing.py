import itertools

import numpy as np


class TripleCounter:
    def __init__(self, min_player_count):
        self.min_player_count = min_player_count

    def compute(self, df):
        df = df.drop_duplicates()

        df['team-id'] = np.where(df.league.isna(), df.team, df.team + '-' + df.league)

        df_agg = df.groupby('player', as_index=False) \
            .agg(team_count=('team-id', 'count'), teams=('team-id', list))

        df_agg = df_agg[df_agg.team_count >= 3]

        team_triple_counter = dict()
        for player_teams in df_agg.teams:
            player_team_triples = itertools.combinations(player_teams, r=3)
            for team_triple in player_team_triples:
                key = frozenset(team_triple)
                current_triple_count = team_triple_counter.get(key, 0)
                team_triple_counter[key] = current_triple_count + 1

        return [(triple, count) for triple, count in team_triple_counter.items() if count >= self.min_player_count]
