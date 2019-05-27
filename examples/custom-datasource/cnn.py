import optapp as opt
from optapp import RunnableApproach
from optapp.run import single_run

import keras
import numpy as np

@single_run
class CnnApproach(RunnableApproach):
    N_CLASSES = 10

    @property
    def parameters(self):
        """
        Declare your parameters here
        """
        return [
            opt.parameters.IntParameter('clf_neurons', 256, 512, 64),
            opt.parameters.CategoricalParameter('kernel_size', [3, 5])
        ]

    def learn(self, data, parameters):
        """
        Define, train and return your model here
        """
        X = np.array(data['X']).astype('float32') / 255.
        y = np.array(data['y']).astype(np.int)
        y = keras.utils.to_categorical(y)

        model = keras.models.Sequential([
            keras.layers.Conv2D(32, 
                                parameters['kernel_size'], 
                                input_shape=(32, 32, 3),
                                padding='same',
                                activation='relu'),
            keras.layers.MaxPool2D(pool_size=(2, 2)),
            keras.layers.Dropout(.3),

            keras.layers.Conv2D(64, 
                                parameters['kernel_size'], 
                                padding='same',
                                activation='relu'),
            keras.layers.MaxPool2D(pool_size=(2, 2)),
            keras.layers.Dropout(.3),
            
            keras.layers.Conv2D(64, 
                    parameters['kernel_size'], 
                    padding='same',
                    activation='relu'),
            keras.layers.MaxPool2D(pool_size=(2, 2)),
            keras.layers.Dropout(.3),

            keras.layers.Conv2D(128, 
                    parameters['kernel_size'], 
                    padding='same',
                    activation='relu'),
            keras.layers.MaxPool2D(pool_size=(2, 2)),
            keras.layers.Dropout(.3),

            keras.layers.Flatten(),
            keras.layers.Dense(parameters['clf_neurons'], 
                               activation='relu'),
            keras.layers.Dropout(.5),
            keras.layers.Dense(CnnApproach.N_CLASSES, activation='softmax')
        ])

        model.compile(loss="categorical_crossentropy", 
                      optimizer="adam",
                      metrics=['accuracy'])

        model.fit(X, y,
                  epochs=50,
                  validation_split=.2,
                  batch_size=32)
        return model

    def inference(self, model, data):
        """
        Use the injected model to make predictions with the data
        """
        X = np.array(data['X']) / 255.
        preds = model.predict(X)
        return [ int(np.argmax(p)) for p in preds ]  # Return the prediction

