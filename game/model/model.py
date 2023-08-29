import os
import random as rd
import numpy as np

import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense, Flatten, Input


class Population():
    
    def __init__(self):
        
        self.generation = 0
        self.n_individuals = 50

        self.all_individuals = []
    
    def create_population(self, input_shape : tuple):
        
        if self.generation == 0:
            for i in range(self.n_individuals):
                self.all_individuals.append(Individual(
                    input_shape=input_shape,
                    n_classes=6,
                    generation=self.generation,
                    n_layer=rd.randint(2, 4)
                ))
            self.generation += 1


class Individual():
    
    def __init__(self, input_shape : tuple, n_classes : int, generation : int, n_layer : int):
        
        self.generation = generation
        self.score = 0
        
        self.model = self.build_model(input_shape, n_classes, n_layer)

    def build_model(self, input_shape, n_classes, n_layer):
        
        # tf.random.set_seed(42)
        
        n_dense = 16
        
        input_layer = Input(shape=input_shape)
        
        x = Dense(n_dense, activation='relu')(input_layer)
        
        for i in range(1, n_layer):
            x = Dense(n_dense, activation='relu')(x)
            
        flatten_layer = Flatten()(x)
        output_layer = Dense(n_classes, activation='softmax')(flatten_layer)
        
        model = Model(inputs=input_layer, outputs=output_layer)
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        return model
    
    def make_prediction(self, x):
        
        prediction = self.model.predict(x, verbose=0)
        
        return prediction[0]


# joe = Individual(input_shape=(34,), n_classes=5, generation=0, n_layer=rd.randint(1, 3))
# print(joe.model.summary())
# print(np.argmax(joe.make_prediction(np.array([[4,1,5,1,3,4,5,8,2,4,4,1,5,1,3,5,8,2,4,3,9,0,4,1,5,1,3,4,5,8,2,4,2,1]]).reshape(1, -1))))