from optapp import RunnableApproach
from optapp.run import single_run
from optapp.parameters import CategoricalParameter, IntParameter

from sklearn.ensemble import RandomForestClassifier

@single_run
class RandomForestApproach(RunnableApproach):

    @property
    def parameters(self):
        """
        Declare your parameters here
        """
        return [
            CategoricalParameter('criterion', ['gini', 'entropy']),
            IntParameter('n_estimators', initial=10, limit=100, step=10),
            IntParameter('max_depth', initial=5, limit=15, step=3)
        ]


    def learn(self, data, parameters):
        """
        Define, train and return your model here
        """
        return RandomForestClassifier(**parameters).fit(**data) # Return a trained model

    def inference(self, model, data):
        """
        Use the injected model to make predictions with the data
        """
        return model.predict(data["X"])  # Return the prediction
