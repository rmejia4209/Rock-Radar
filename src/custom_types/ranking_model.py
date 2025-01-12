import math


class RankingModel:
    """TODO:"""
    _model: str
    _options: list[str] = ['raw', 'logarithmic',]  # logistic removed

    def __init__(self, model: str = 'raw'):
        self._model = model

    @staticmethod
    def get_options():
        """TODO"""
        return RankingModel._options

    @staticmethod
    def get_logistic_coefficient_limits() -> tuple[int, int]:
        return (0.05, 0.5)

    @staticmethod
    def _raw_score(popularity: int, rating: float) -> float:
        """Return the popularity * score"""
        return round(popularity * rating, 2)

    @staticmethod
    def _logarithmic_score(popularity: int, rating: float) -> float:
        """
        Returns the product of the log of the popularity and the rating.
        """
        return round(math.log(popularity+1)*rating, 2)

    def _logistic_score(self, popularity: int, rating: float) -> float:
        """
        Currently not used due to the complexity of the model.
        Returns a score based on a logistic function.
        """
        c = self._target_popularity / 2
        k = self._trust_parameter
        exponent = (-1 * k) * (popularity - c)
        score = (1 / (1 + math.exp(exponent))) * rating
        return round(score, 2)

    def get_score(self, popularity: int, rating: float) -> float:
        """Returns the score based on the current model"""
        if self._model == 'raw':
            return RankingModel._raw_score(popularity, rating)
        elif self._model == 'logarithmic':
            return RankingModel._logarithmic_score(popularity, rating)
        return self._logistic_score(popularity, rating)

    def set_model(self, model: str) -> None:
        """
        Sets the model used. If Logistic is set, popularity and trust
        parameters are set as well.
        """
        self._model = model.lower()
