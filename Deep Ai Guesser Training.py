# deep_ai_guesser.py

# deep_ai_guesser.py

import numpy as np
import random
import matplotlib.pyplot as plt
from collections import deque
import torch
import torch.nn as nn
import torch.optim as optim

# Parameters
episodes = 500
max_steps = 10
reward_correct = 50
reward_wrong = -20
gamma = 0.95
epsilon = 1.0
epsilon_min = 0.01
epsilon_decay = 0.995
learning_rate = 0.001

# Environment settings
LOW = 1
HIGH = 100

class QNetwork(nn.Module):
    def _init_(self):
        super(QNetwork, self)._init_()
        self.fc1 = nn.Linear(3, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, (HIGH - LOW + 1))  # 100 actions

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class DeepAIGuesser:
    def _init_(self):
        self.model = QNetwork()
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.criterion = nn.MSELoss()
        self.memory = deque(maxlen=2000)
        self.epsilon = epsilon

    def get_state(self, low, high, current_guess):
        return np.array([low/100, high/100, current_guess/100], dtype=np.float32)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(LOW, HIGH)
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state)
            q_values = self.model(state_tensor)
            action = torch.argmax(q_values).item() + 1
            return action

    def store_experience(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size=32):
        if len(self.memory) < batch_size:
            return

        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            state_tensor = torch.FloatTensor(state)
            next_state_tensor = torch.FloatTensor(next_state)
            target = reward
            if not done:
                target += gamma * torch.max(self.model(next_state_tensor)).item()

            output = self.model(state_tensor)[action-1]
            loss = self.criterion(output, torch.tensor(target))

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        if self.epsilon > epsilon_min:
            self.epsilon *= epsilon_decay

# Training
agent = DeepAIGuesser()
scores = []

for e in range(episodes):
    secret_number = random.randint(LOW, HIGH)
    low = LOW
    high = HIGH
    score = 0
    
    for step in range(max_steps):
        current_guess = random.randint(low, high)
        state = agent.get_state(low, high, current_guess)
        action = agent.choose_action(state)

        # Environment feedback
        if action < secret_number:
            low = max(low, action + 1)
            reward = reward_wrong
        elif action > secret_number:
            high = min(high, action - 1)
            reward = reward_wrong
        else:
            reward = reward_correct

        next_state = agent.get_state(low, high, action)
        done = (action == secret_number)

        agent.store_experience(state, action, reward, next_state, done)

        score += reward

        if done:
            break

    agent.replay()
    scores.append(score)
    print(f"Episode {e+1}/{episodes} - Score: {score}")

# Plotting
plt.plot(scores)
plt.title("Training Progress")
plt.xlabel("Episode")
plt.ylabel("Score")
plt.savefig("training_scores.png")
plt.show()

# Save the model
torch.save(agent.model.state_dict(), "deep_ai_model.pth")

print("Training completed!")