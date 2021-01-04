input = '0,3,6'
input = '1,3,2'
input = '2,1,3'
input = '5,1,9,18,13,8,0'

turn_count = 2020
turn_count = 30000000

start_numbers = [int(i) for i in input.split(',')]
latest_turns = {}
prev_num = None
for turn in range(1, turn_count+1):
    if turn <= len(start_numbers):
        num = start_numbers[turn-1]
        if prev_num is not None:
            latest_turns[prev_num] = turn - 1
        prev_num = num
        continue

    if prev_num not in latest_turns:
        latest_turns[prev_num] = turn - 1
        num = 0
    else:
        prev_occur_turn = latest_turns[prev_num]
        latest_turns[prev_num] = turn - 1
        num = turn - 1 - prev_occur_turn
    prev_num = num
print(num)
