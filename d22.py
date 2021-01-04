import os
from collections import deque

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.read()

train_content = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""
#content = train_content

p1, p2 = content.split('\n\n')
p1, p2 = p1.splitlines()[1:], p2.splitlines()[1:]
p1, p2 = [int(i) for i in p1], [int(i) for i in p2]


class GameError(Exception):
    pass


class SimpleGame:
    def __init__(self, p1_cards, p2_cards):
        self.q1 = deque(p1_cards)
        self.q2 = deque(p2_cards)
        self.winner = None
        self.winner_q = None
        self.score = 0

    def play_round(self):
        p1_wins, p1_card, p2_card = self.determine_round_winner()
        if p1_wins:
            self.q1.append(p1_card)
            self.q1.append(p2_card)
        else:
            self.q2.append(p2_card)
            self.q2.append(p1_card)
        return p1_wins

    def game_end_condition(self, p1_wins_prev_round):
        return not bool(self.q1 and self.q2), p1_wins_prev_round

    def determine_round_winner(self):
        """
        Will return True if player 1 wins
        """
        p1_card = self.q1.popleft()
        p2_card = self.q2.popleft()
        return p1_card > p2_card, p1_card, p2_card

    def play(self):
        p1_wins = None
        while True:
            res, p1_wins = self.game_end_condition(p1_wins)
            if res:
                break
            p1_wins = self.play_round()
        self.score_game(p1_wins)
        return self.winner, self.score

    def score_game(self, p1_wins):
        if p1_wins:
            self.winner = True
            self.winner_q = self.q1
        else:
            self.winner = False
            self.winner_q = self.q2

        scr = 0
        self.winner_q.reverse()
        for i, card in enumerate(self.winner_q):
            scr += (i+1) * card

        self.score = scr


g = SimpleGame(p1, p2)
_, score = g.play()
print(score)


class RecursiveCombat(SimpleGame):
    def __init__(self, p1_cards, p2_cards):
        super().__init__(p1_cards, p2_cards)
        self.prev_states = set()

    def determine_round_winner(self):
        """
        Will return True if player 1 wins
        """
        p1_wins, p1_card, p2_card = super().determine_round_winner()
        if p1_card <= len(self.q1) and p2_card <= len(self.q2):
            p1_subgame_cards = list(self.q1)[:p1_card]
            p2_subgame_cards = list(self.q2)[:p2_card]
            subgame = RecursiveCombat(p1_subgame_cards, p2_subgame_cards)
            p1_wins, _ = subgame.play()

        return p1_wins, p1_card, p2_card

    def game_end_condition(self, p1_wins_prev_round):
        res, p1_wins = super().game_end_condition(p1_wins_prev_round)
        if res:
            return True, p1_wins
        cs = self.current_state()
        if cs in self.prev_states:
            return True, True

        self.prev_states.add(cs)
        return False, p1_wins_prev_round

    def current_state(self):
        p1h = hash(tuple(self.q1))
        p2h = hash(tuple(self.q2))
        return hash((p1h, p2h))

rc = RecursiveCombat(p1, p2)
_, score = rc.play()
print(score)
