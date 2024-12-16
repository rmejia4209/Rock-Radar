import math


class RankingModel:
    """TODO:"""
    _model: str

    def __init__(self, model: str = 'raw'):
        self._model = model

    @staticmethod
    def _raw_score(popularity: int, rating: float) -> float:
        """Return the popularity * score"""
        return round(popularity * rating, 2)

    @staticmethod
    def _logarithmic_score(popularity: int, rating: float) -> float:
        """
        Returns the product of the log of the popularity and the rating.
        """
        return round(math.log(popularity)*rating, 2)

    def _logistic_score(self, popularity: int, rating: float) -> float:
        """Returns a score based on a logistic function."""
        c = self._target_popularity / 2
        k = self._trust_parameter
        exponent = (-1 * k) * (popularity - c)
        score = (1 / (1 + math.exp(exponent))) * rating
        return round(score, 2)

    def get_score(self, popularity: int, rating: float) -> float:
        """Returns the score based on the current model"""
        print("Running...")
        if self._model == 'raw':
            return RankingModel._raw_score(popularity, rating)
        elif self._model == 'logarithmic':
            return RankingModel._logarithmic_score(popularity, rating)
        return self._logistic_score(popularity, rating)

    def set_model(self, model: str, popularity: int, trust: int) -> None:
        """
        Sets the model used. If Logistic is set, populartiy and trust
        parameters are set as well.
        """
        self._model = model
        if self._model == 'logistic':
            self._target_popularity = popularity
            self._trust_parameter = trust
