import os

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.readlines()

content_train = """939
7,13,x,x,59,x,31,19""".splitlines()
#content = content_train


earliest_dep_time, buses = content
earliest_dep_time = int(earliest_dep_time)
earliest_avail_dep_time = None
corresponding_bus = None

for bus in buses.strip().split(','):
    if bus == 'x':
        continue
    bus = int(bus)
    next_dep = bus - (earliest_dep_time % bus)
    if earliest_avail_dep_time is None or next_dep < earliest_avail_dep_time:
        earliest_avail_dep_time = next_dep
        corresponding_bus = bus

print(earliest_avail_dep_time * corresponding_bus)

# part 2
# training values
#buses = '17,x,13,19'
#buses = '67,7,59,61'
#buses = '67,x,7,59,61'
#buses = '67,7,x,59,61'
#buses = '1789,37,47,1889'

desired_bus_times = [(t, bus) for t, bus in enumerate(buses.strip().split(','))]
desired_bus_times = [(int(bus), t) for t, bus in desired_bus_times if bus != 'x']

print(";".join([f"t + {t} mod {bus} == 0" for bus, t in desired_bus_times]))
# -> result from Wolfram Alpha :smirk: