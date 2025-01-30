"""
Ponizszy kod zawiera implementację uczacego sie agenta w grze blackjack.
Wykonane przez: Michał Krokoszyński i Dawid Nowakowski

__
----INSTALACJA NIEZBĘDNYCH BIBLIOTEK----
__
W terminalu wykonaj:

1. Wykonaj: pip install gymnasium
2. Wykonaj: pip install ale-py
3. Wykonaj: pip install "gymnasium[toy-text]"
4. Wykonaj: pip install numpy
5. Wykonaj: python z4.py *

* main.py = nazwa TEGO pliku

Uzyte srodowisko: https://ale.farama.org/environments/blackjack/
"""

import gymnasium as gym
import numpy as np
import random
from collections import defaultdict

# Tworzenie środowiska
env_test = gym.make("Blackjack-v1", render_mode=None)
env_final = gym.make("Blackjack-v1", render_mode='human')


def epsilon_greedy_policy(Q, state, nA, epsilon=0.1):
    if random.uniform(0, 1) < epsilon:
        return random.choice(range(nA))
    else:
        return np.argmax(Q[state])


def q_learning(env, num_episodes=1000, alpha=0.1, gamma=0.99, epsilon=0.1):
    """
        Funkcja uczaca agenta. Jest to implementacja algorytmu Q-learning.
    """
    Q = defaultdict(lambda: np.zeros(env.action_space.n))

    for episode in range(num_episodes):
        state, _ = env.reset()
        done = False

        while not done:
            action = epsilon_greedy_policy(Q, state, env.action_space.n, epsilon)
            next_state, reward, done, _, _ = env.step(action)

            # Q-learning update
            best_next_action = np.argmax(Q[next_state])
            Q[state][action] += alpha * (reward + gamma * Q[next_state][best_next_action] - Q[state][action])

            state = next_state

    return Q


Q_table = q_learning(env_test)


def test_agent(env, Q, num_episodes=30):
    """
        Funkcja testujaca agenta.
    """
    total_rewards = 0

    for _ in range(num_episodes):
        state, _ = env.reset()
        done = False
        while not done:
            action = np.argmax(Q[state])
            state, reward, done, _, _ = env.step(action)
        total_rewards += reward

    print(f"Średnia nagroda po {num_episodes} grach: {total_rewards / num_episodes}")


test_agent(env_final, Q_table)
