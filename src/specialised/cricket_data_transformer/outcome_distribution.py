import pandas as pd
from src.config import BALL_BY_BALL_FILE_PATH


class OutcomeDistribution:
    """
    Class to calculate outcome distributions from ball-by-ball data.
    It provides methods to calculate distributions based on key-value pairs and to compute conditional probabilities.

    Author: Jonathan Farrand
    Date: 2025-07-14
    """
    def __init__(self, ball_by_ball_data: pd.DataFrame):
        """
        Initializes the OutcomeDistribution class with ball-by-ball data.
        :param ball_by_ball_data: A DataFrame containing ball-by-ball data.
        """
        self.ball_by_ball = ball_by_ball_data
        pass

    def distribution(self, key_value_pairs: dict, distribution_key, ball_by_ball: pd.DataFrame = None):
        """
        Calculates the distribution of a specified key in the ball-by-ball data,
        filtered by the provided key-value pairs.
        :param key_value_pairs: A dictionary of key-value pairs to filter the DataFrame.
        :param distribution_key: The key for which the distribution is calculated.
        """
        if ball_by_ball == None:
            ball_by_ball = self.ball_by_ball
        
        adj_df = ball_by_ball.copy()
        for key, value in key_value_pairs.items():
            adj_df: pd.DataFrame = adj_df[(adj_df[key] == value)]
        
        return adj_df[distribution_key].value_counts().to_dict()
    
    def conditional_distribution_probability(
        self,
        key_value_pairs: dict,
        distribution_key: str,
        group_by_key: str,
        ball_by_ball: pd.DataFrame = None
    ):
        """
        Calculates the conditional distribution probability of a specified key in the ball-by-ball data,
        filtered by the provided key-value pairs and grouped by the specified group_by_key.
        :param key_value_pairs: A dictionary of key-value pairs to filter the DataFrame.
        :param distribution_key: The key for which the conditional distribution probability is calculated.
        :param group_by_key: The key by which the DataFrame is grouped.
        :param ball_by_ball: The DataFrame containing ball-by-ball data.
        :return: A dictionary with the conditional distribution probabilities.
        The keys are tuples of the group_by_key and the value of the distribution_key,
        and the values are the probabilities of the distribution_key given the group_by_key.
        """
        if ball_by_ball is None:
            ball_by_ball = self.ball_by_ball

        # Apply filters first
        adj_df = ball_by_ball.copy()
        for key, value in key_value_pairs.items():
            adj_df = adj_df[adj_df[key] == value]

        if adj_df.empty:
            return {}

        # Group by group_by_key (e.g. "over")
        group_sizes = adj_df.groupby(group_by_key).size()
        value_counts = adj_df.groupby(group_by_key)[distribution_key].value_counts()

        # Compute conditional probabilities: count / group total
        probs = (value_counts / group_sizes).to_dict()

        return probs
    
    def tidied_conditional_distribution_probability(self, key_value_pairs: dict, distribution_key: dict, group_by_key: str, ball_by_ball: pd.DataFrame = None):
        """
        Tidies the conditional distribution probability results by filtering based on a single key-value pair.
        :param key_value_pairs: A dictionary of key-value pairs to filter the DataFrame.
        :param distribution_key: A dictionary with a single key-value pair to filter the results.
        :param group_by_key: The key by which the DataFrame is grouped.
        :param ball_by_ball: The DataFrame containing ball-by-ball data.
        :return: A dictionary with the tidied conditional distribution probabilities.
        If the distribution_key has more than one key, returns None.
        """
        if len(distribution_key.keys()) > 1:
            return None
        temp_key = list(distribution_key.keys())[0]
        results = self.conditional_distribution_probability(key_value_pairs, temp_key, group_by_key, ball_by_ball)

        tidied_results = dict()
        tar_val = list(distribution_key.values())[0]
        for k, v in results.items():
            if (k[1] == tar_val):
                tidied_results[k[0]] = v
        return tidied_results



if __name__ == "__main__":
    ball_by_ball_data = pd.read_feather(f"{BALL_BY_BALL_FILE_PATH}t20.feather")
    outcome_distribution = OutcomeDistribution(ball_by_ball_data)
    pairs = dict()
    pairs["inn_num"] = 1
    results = outcome_distribution.distribution(pairs, "over_num")
    #print(results)

    from src.plotter import Plotter
    Plotter.plot_scatter_dict(results)

    result = outcome_distribution.tidied_conditional_distribution_probability(
    key_value_pairs=pairs, 
    distribution_key={'dismissal' : 1}, 
    group_by_key='over_num'
    )

        
    Plotter.plot_scatter_dict(result)