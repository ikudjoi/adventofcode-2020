content = """14082811
5249543"""
train_content = """5764801
17807724"""
#content = train_content

card_pub, door_pub = [int(v) for v in content.splitlines()]


def transform(current_val, subject_num, loop_size=1):
    v = current_val
    for _ in range(loop_size):
        v *= subject_num
        v %= 20201227
    return v


def find_loop_size(subject_num, pub_key):
    current_val = 1
    loop_size = 1
    while True:
        current_val = transform(current_val, subject_num)
        if current_val == pub_key:
            break
        loop_size += 1
    return loop_size


#card_loop_size = find_loop_size(7, card_pub)
door_loop_size = find_loop_size(7, door_pub)
enc_key = transform(1, card_pub, door_loop_size)
print(enc_key)