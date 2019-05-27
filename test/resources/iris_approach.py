from sklearn.tree import DecisionTreeClassifier

from optapp import RunnableApproach, Approach
from optapp.run import single_run
from optapp.parameters import IntParameter, BoolParameter, CategoricalParameter

@single_run
class DecisionTreeApproach(RunnableApproach):

    @property
    def parameters(self):
        """
        Declare your parameters here
        """
        return [
            IntParameter("max_depth", 10, 50, 10),
            CategoricalParameter("criterion", ["gini", "entropy"])
        ]

    def learn(self, data, parameters):
        """
        Define, train and return your model here
        """
        return DecisionTreeClassifier(**parameters).fit(**data)

    def inference(self, model, data):
        """
        Use the injected model to make predictions with the data
        """
        return model.predict(data["X"]) # Return the prediction
