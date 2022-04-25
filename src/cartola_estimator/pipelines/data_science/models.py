from sklearn.base import BaseEstimator
import pandas as pd

class CartolaEstimator(BaseEstimator):
    """Class responsible for agrup estimators of diferent Cartola statistics."""

    def __init__(self, **estimators):
        self._estimators = estimators

    def predict(self, X):
        y = pd.DataFrame(index=X.index)
        for statistic, estimator in self._estimators.items():
            y[statistic] = estimator.predict(X)
        return y
