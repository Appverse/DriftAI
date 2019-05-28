from sklearn.linear_model import LogisticRegression

from driftai import RunnableApproach, Approach
from driftai.run import single_run
from driftai.parameters import FloatParameter, BoolParameter, CategoricalParameter

@single_run
class LogisticRegressionApproach(RunnableApproach):

    @property
    def parameters(self):
        """
        Declare your parameters here
        """
        return [
            FloatParameter("tol", 1e-4, 1, 2),
            FloatParameter("C", 1, 3, 2),
            BoolParameter("fit_intercept"),
            CategoricalParameter("solver", ["lbfgs"])
        ]

    def learn(self, data, parameters):
        """
        Define, train and return your model here
        """
        return LogisticRegression(**parameters).fit(**data)

    def inference(self, model, data):
        """
        Use the injected model to make predictions with the data
        """
        return model.predict(data["X"]) # Return the prediction
