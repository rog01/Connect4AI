import random
import tensorflow as tf
import keras
import numpy as np

from keras.models import Sequential,  Model

from keras.layers import Dense, Dropout, Flatten, Conv2D, Input, MaxPooling2D, Reshape, BatchNormalization
from keras.optimizers import Adam

from collections import deque

class DQN:
    def __init__(self, env):
        self.env     = env
        self.memory  = deque(maxlen=20000) # initialement à 2000
        
        self.gamma = 0.85
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.005
        self.tau = .125

        self.model        = self.create_model()
        self.target_model = self.create_model()

    def create_model(self):
        model = Sequential()
        state_shape  = self.env.shape

        model.add(Dense(20, input_dim=state_shape[0]*state_shape[1], activation='relu'))
        model.add(Dense(100, activation='relu'))
        model.add(Dense(100, activation='relu'))
        model.add(Dense(state_shape[1], activation='linear'))

        model.compile(loss="mean_squared_error", optimizer=Adam(lr=self.learning_rate))

        return model

    """
    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()
        return np.argmax(self.model.predict(state)[0])
    """

    def  create_model_qui_fonctionne(self):
        model = Sequential()
        state_shape  = self.env.shape

        model.add(Dense(24, input_shape= state_shape, activation="relu")) # VOIR EVENTUELLEMENT SANS [0]
        model.add(Dense(state_shape[0] * state_shape[1], input_shape= state_shape, activation="relu"))

        model.add(Dense(7))

        model.compile(loss="mean_squared_error", optimizer=Adam(lr=self.learning_rate))

        return model


    def remember(self, state, action, reward, new_state, done):
        #print("Méthode remenber")
        self.memory.append([state, action, reward, new_state, done])

    def replay(self):
        batch_size = 32
        if len(self.memory) < batch_size: 
            #print(f"Méthode replay: self memory= {self.memory} < {batch_size}")
            return

        samples = random.sample(self.memory, batch_size)
        #print(f"Méthode replay: sampleshape= {len(samples)}")
        #print(f"Méthode replay: samples= {samples}")
        for sample in samples:
            state, action, reward, new_state, done = sample
            #state= state.reshape(6,7,1)
            #print(f"Méthode remenber, state shape: {state.shape} \ntarget=\n {state}")
            state = state.reshape(1, self.env.shape[0] * self.env.shape[1])
            target = self.target_model.predict(state)

            print(f"Méthode remenber, state shape: {target.shape} \ntarget=\n {target}")
            if done:
                target[0][action] = reward
            else:
                #Q_future = max(self.target_model.predict(new_state)[0])
                #new_state= new_state.reshape(6,7,1)
                new_state = new_state.reshape(1, self.env.shape[0] * self.env.shape[1])
                Q_future = max(self.target_model.predict(new_state)[0])
                #print(f"Méthode remenber, target future= {Q_future}")
                target[0][action] = reward + Q_future * self.gamma
                print(f"\nMéthode remenber, target[0][action]= {target[0][action]} action= {action}\n")
            self.model.fit(state, target, epochs=1, verbose=1)

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)
        #print(f"Méthode target train: target_weights\n{target_weights}")

    def save_model(self, fn):
        self.model.save(fn)

    
