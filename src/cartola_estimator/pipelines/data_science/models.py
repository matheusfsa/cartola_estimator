from sklearn.base import BaseEstimator


class CartolaEstimator(BaseEstimator):
    """Class responsible for agrup estimators of diferent Cartola statistics."""

    def __init__(self, **estimators):
        self._estimators = estimators

    def predict(self, X, target):
        return self._estimators[target].predict(X)
