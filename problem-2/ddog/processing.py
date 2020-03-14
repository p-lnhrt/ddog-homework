"""
This modules gathers all the classes and functions dedicated to the processing of metrics on baseball data.
"""
import itertools

import numpy as np


class TripleCounter:
    """ This class encapsulates the logic dedicated tho the computation of baseball team triples consisting of a 
    minimum number of players.
    
    Attributes: 
        min_player_count (int): Minimum player count a given team triple must have in order to be returned.    
    """
    def __init__(self, min_player_count):
        """ Initializes the `TripleCounter` object.
        
        Args:
            min_player_count (int): Cf. class docstring. 
        """
        self.min_player_count = min_player_count

    def compute(self, df):
        """ List baseball team triples with the required minimum number of players based on the data available in the
        input DataFrame `df`.
        
        Args: 
            df (pandas.DataFrame): DataFrame that gathers the raw data of all input baseball statistics files.

        Returns: 
            list[(frozenset, int)]: List of (team triple, player count) where each player count is greater or equal to
            the value of the `min_player_count` attribute.
        """
        df = df.drop_duplicates()

        df['team-id'] = np.where(df.league.isna(), df.team, df.team + '-' + df.league)

        df = df.groupby('player', as_index=False) \
            .agg(team_count=('team-id', 'count'), teams=('team-id', list))

        df = df[df.team_count >= 3]

        team_triple_counter = dict()
        for player_teams in df.teams:
            player_team_triples = itertools.combinations(player_teams, r=3)
            for team_triple in player_team_triples:
                key = frozenset(team_triple)
                current_triple_count = team_triple_counter.get(key, 0)
                team_triple_counter[key] = current_triple_count + 1

        return [(triple, count) for triple, count in team_triple_counter.items() if count >= self.min_player_count]
