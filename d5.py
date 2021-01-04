import os

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.readlines()

ids = []
for line in content:
    row_coordinate_bin = line[:7].replace('F', '0').replace('B', '1')
    row_coordinate = int(row_coordinate_bin, 2)
    column_coordinate_bin = line[7:10].replace('L', '0').replace('R', '1')
    column_coordinate = int(column_coordinate_bin, 2)
    current_id = row_coordinate * 8 + column_coordinate
    ids.append(current_id)

print(max(ids))
ids = sorted(ids)
previous_id = None
for i in ids:
    if previous_id and i > previous_id + 1:
        print(i - 1)
    previous_id = i