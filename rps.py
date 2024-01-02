import numpy as np
from enum import IntEnum

class Actions(IntEnum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    def utility(my_action, opp_action):
        payoffs = [
            [0, -1, 1],
            [1, 0, -1],
            [-1, 1, 0],
        ]
        return payoffs[my_action][opp_action]

class RPS_Trainer:
    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()

    def get_action(self, strategy):
        action = np.random.choice(list(Actions), p=strategy)
        return action

    def train(self, iterations):
        for i in range(iterations):
            action1 = self.get_action( self.player1.get_strategy() )
            action2 = self.get_action( self.player2.get_strategy() )

            utility1 = Actions.utility(action1, action2)
            utility2 = Actions.utility(action2, action1)

            utility_vec1 = self.player1.get_utility_vector(action2)
            utility_vec2 = self.player2.get_utility_vector(action1)

            regret1 = utility_vec1 - utility1
            regret2 = utility_vec2 - utility2

            self.player1.regret_sum += regret1
            self.player2.regret_sum += regret2

class Player:
    def __init__(self):
        self.regret_sum = np.zeros( len(Actions) )
        self.strategy = np.zeros( len(Actions) )
        self.strategy_sum = np.zeros( len(Actions) )

    def get_strategy(self):
        normalizing_sum = 0
        for action in Actions:
            self.strategy[action] = self.regret_sum[action] if self.regret_sum[action] > 0 else 0
            normalizing_sum += self.strategy[action]
        for action in Actions:
            if normalizing_sum > 0:
                self.strategy[action] /= normalizing_sum
            else:
                self.strategy[action] = 1 / len(Actions)
            self.strategy_sum[action] += self.strategy[action]
        return self.strategy

    def get_utility_vector(self, opp_action):
        return np.array([
            Actions.utility(Actions.ROCK, opp_action),
            Actions.utility(Actions.PAPER, opp_action),
            Actions.utility(Actions.SCISSORS, opp_action),
        ])

    def get_average_strategy(self):
        average_strategy = np.zeros( len(Actions) )
        normalizing_sum = sum(self.strategy_sum)
        for action in Actions:
            if normalizing_sum > 0:
                average_strategy[action] = self.strategy_sum[action] / normalizing_sum
            else:
                average_strategy = 1 / len(Actions)
        return average_strategy
            

def main():
    rps = RPS_Trainer()
    rps.train(10000)
    print(rps.player1.get_average_strategy())
    print(rps.player2.get_average_strategy())

if __name__ == '__main__':
    main()
