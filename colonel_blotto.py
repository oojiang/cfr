import itertools
import random

def get_utility(my_action, opp_action):
    my_wins = 0
    opp_wins = 0
    for m, o in zip(my_action, opp_action):
        if m > o:
            my_wins += 1
        elif m < o:
            opp_wins += 1
    if my_wins > opp_wins:
        return 1
    elif my_wins < opp_wins:
        return -1
    else:
        return 0

class Blotto_Trainer:
    def __init__(self, S, N):
        self.actions = []
        for c in itertools.combinations(range(S+N-1), N-1): 
            self.actions.append(tuple(b-a-1 for a, b in zip((-1,)+c, c+(N+S-1,))))
        self.player1 = Player(self.actions)
        self.player2 = Player(self.actions)

    def train(self, iterations):
        for i in range(iterations):
            strat1 = self.player1.get_strategy()
            strat2 = self.player2.get_strategy()

            action1 = self.player1.get_action(strat1)
            action2 = self.player2.get_action(strat2)

            utility1 = get_utility(action1, action2)
            utility2 = get_utility(action2, action1)

            for action in self.actions:
                regret1 = get_utility(action, action2)
                regret2 = get_utility(action, action1)

                self.player1.regret_sum[action] += regret1
                self.player2.regret_sum[action] += regret2

class Player:
    def __init__(self, actions):
        self.actions = actions
        self.regret_sum = dict.fromkeys(self.actions, 0)
        self.strategy = dict.fromkeys(self.actions, 0)
        self.strategy_sum = dict.fromkeys(self.actions, 0)

    def get_strategy(self):
        normalizing_sum = 0
        for action in self.actions:
            self.strategy[action] = self.regret_sum[action] if self.regret_sum[action] > 0 else 0
            normalizing_sum += self.strategy[action]
        for action in self.actions:
            if normalizing_sum > 0:
                self.strategy[action] /= normalizing_sum
            else:
                self.strategy[action] = 1 / len(self.actions)
            self.strategy_sum[action] += self.strategy[action]
        return self.strategy

    def get_action(self, strategy):
        action = random.choices(list(strategy.keys()), weights=strategy.values(), k=1)[0]
        return action

    def get_average_strategy(self):
        average_strategy = dict.fromkeys(self.actions, 0)
        normalizing_sum = sum(self.strategy_sum.values())
        for action in self.actions:
            if normalizing_sum > 0:
                average_strategy[action] = self.strategy_sum[action] / normalizing_sum
            else:
                average_strategy = 1 / len(self.actions)
        return average_strategy

def pretty_print(strategy):
    for action in strategy.keys():
        print(action, round(strategy[action], 3))
    print()

def print_winrate(num_games, player1, player2, strat1, strat2):
    p1_wins = 0
    p2_wins = 0
    ties = 0
    for _ in range(num_games):
        action1 = player1.get_action(strat1)
        action2 = player2.get_action(strat2)
        utility = get_utility(action1, action2)
        if utility == 0:
            ties += 1
        elif utility > 0:
            p1_wins += 1
        else:
            p2_wins += 1
    print(p1_wins, p2_wins, ties)
    print(round(p1_wins/num_games, 2), round(p2_wins/num_games, 2), round(ties/num_games, 2))



def main():
    blotto = Blotto_Trainer(5, 3)
    blotto.train(100000)
    strat1 = blotto.player1.get_average_strategy()
    strat2 = blotto.player2.get_average_strategy()
    pretty_print(strat1)
    pretty_print(strat2)
    print_winrate(10000, blotto.player1, blotto.player2, strat1, strat2)

if __name__ == '__main__':
    main()
