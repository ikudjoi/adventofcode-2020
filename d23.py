import os
from collections import deque


class Cup:
    def __init__(self, cup_num, previous_cup=None):
        self.cup_num = cup_num
        self.previous_cup = previous_cup
        self.next_cup = None


class CupGame:
    def __init__(self, cup_str, total_cups):
        self.total_cups = total_cups
        self.refs_to_cups = {}
        cups = list(cup_str)
        prev_cup = None
        first_cup = None
        for cup in cups:
            cup_num = int(cup)
            new_cup = Cup(cup_num, prev_cup)
            self.refs_to_cups[cup_num] = new_cup
            if prev_cup:
                prev_cup.next_cup = new_cup
            if not first_cup:
                first_cup = new_cup
            prev_cup = new_cup
        if total_cups > len(cups):
            for cup_num in range(len(cups) + 1, total_cups + 1):
                new_cup = Cup(cup_num, prev_cup)
                self.refs_to_cups[cup_num] = new_cup
                prev_cup.next_cup = new_cup
                prev_cup = new_cup
        # Close circle
        first_cup.previous_cup = prev_cup
        prev_cup.next_cup = first_cup
        self.current_cup = first_cup

    def minus_one(self, value):
        if value == 1:
            return self.total_cups
        return value - 1

    def destination_cup_num(self, pickup_cups):
        destination_cup_num = self.minus_one(self.current_cup.cup_num)
        while any([c for c in pickup_cups if c.cup_num == destination_cup_num]):
            destination_cup_num = self.minus_one(destination_cup_num)
        return destination_cup_num

    def lookup_cup(self, cup_num):
        return self.refs_to_cups[cup_num]

    def play_round(self):
        pickup_cups = []
        pickup_cup = None
        for _ in range(3):
            pickup_cup = self.current_cup.next_cup if pickup_cup is None else pickup_cup.next_cup
            pickup_cups.append(pickup_cup)
        destination_cup_num = self.destination_cup_num(pickup_cups)
        destination_cup = self.lookup_cup(destination_cup_num)

        destination_cup_current_next = destination_cup.next_cup
        last_pickup_cup_next = pickup_cups[-1].next_cup
        # Remove pickup cups from circle
        self.current_cup.next_cup = last_pickup_cup_next
        last_pickup_cup_next.previous_cup = self.current_cup
        # Add them back relative to destination cup
        destination_cup.next_cup = pickup_cups[0]
        pickup_cups[0].previous_cup = destination_cup
        pickup_cups[-1].next_cup = destination_cup_current_next
        destination_cup_current_next.previous_cup = pickup_cups[-1]
        # Move current cup
        self.current_cup = self.current_cup.next_cup

    def play(self, rounds):
        for _ in range(rounds):
            self.play_round()

    def part_1_result(self):
        cup = self.lookup_cup(1)
        res_str = ""
        for _ in range(self.total_cups - 1):
            cup = cup.next_cup
            res_str += str(cup.cup_num)
        return res_str

    def part_2_result(self):
        cup = self.lookup_cup(1)
        cup_a = cup.next_cup
        cup_b = cup_a.next_cup
        return cup_a.cup_num * cup_b.cup_num


input, rounds, total_cups = "962713854", 100, 9
g1 = CupGame(input, total_cups)
g1.play(rounds)
print(g1.part_1_result())

input, rounds, total_cups = "962713854", 10000000, 1000000
g2 = CupGame(input, total_cups)
g2.play(rounds)
print(g2.part_2_result())
