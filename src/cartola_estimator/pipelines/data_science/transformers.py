from sklearn.base import BaseEstimator

__all__ = [
    "DropColumns"
]

class DropColumns(BaseEstimator):

    def __init__(self, columns):
        self.columns = columns

    def fit(self, X):
        return self

    def transform(self, X, y=None):
        return X.drop(columns=self.columns)

    def fit_transform(self, X, y, **fit_params):
        return self.fit(X).transform(X, y)