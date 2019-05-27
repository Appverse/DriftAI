
from optapp import RunnableApproach
from optapp.run import single_run
from optapp.parameters import FloatParameter, BoolParameter

from sklearn.linear_model import LogisticRegression

@single_run
class LogisticRegressionApproach(RunnableApproach):

    @property
    def parameters(self):
        """
        Declare your parameters here
        """
        pars = [
            FloatParameter("tol", 1e-4, 1, 10),
            FloatParameter("C", 1, 3, 10),
            BoolParameter("fit_intercept")
        ]

        return pars

    def learn(self, data, parameters):
        """
        Define, train and return your model here
        """
        lr_parameters = {
            "random_state" : 0, 
            "solver" : 'lbfgs', 
            "multi_class" : 'multinomial',
            **parameters
        }
        return LogisticRegression(**lr_parameters).fit(data["X"], data["y"])

    def inference(self, model, data):
        """
        Use the injected model to make predictions with the data
        """
        return model.predict(data['X'])  # Return the prediction
