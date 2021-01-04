import os

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.readlines()

requested_bag = 'shiny gold bag'

simple_relations = []
full_relations = {}
for line in content:
    outer_bag, inner_bags_str = line.strip().split('s contain ')
    inner_bags = [bag.strip().rstrip('.s') for bag in inner_bags_str.split(',')]
    inner_bag_map = [bag.split(' ', 1) for bag in inner_bags]
    inner_bag_map = [[int(m[0].replace('no', '0')), m[1]] for m in inner_bag_map]
    inner_to_outer_relations = { inner_bag[1]: outer_bag for inner_bag in inner_bag_map }
    simple_relations.append(inner_to_outer_relations)
    full_relations[outer_bag] = inner_bag_map

# part 1
distinct_dags = set([item for sublist in simple_relations for item in sublist.items()])
# The requested bag can be sent as-is too.
bags_than_contain_requested_bag = set(['shiny gold bag'])
previous_length = 0
while len(bags_than_contain_requested_bag) > previous_length:
    previous_length = len(bags_than_contain_requested_bag)
    bags_that_can_contain_bags = set([dag[1] for dag in distinct_dags if dag[0] in bags_than_contain_requested_bag])
    bags_than_contain_requested_bag.update(bags_that_can_contain_bags)

print(len(bags_than_contain_requested_bag) - 1)


# part 2
parent_gen_bags = {'shiny gold bag': 1}
cumulative_bag_count = 0
while parent_gen_bags:
    next_gen_bags = {}
    for parent_gen_bag, parent_gen_bag_count in parent_gen_bags.items():
        if parent_gen_bag_count == 0:
            continue
        this_bag_contents = next(inner_bags for outer_bag, inner_bags in full_relations.items() if outer_bag == parent_gen_bag)
        for inner_bag_count, inner_bag in this_bag_contents:
            # Add placeholder
            if inner_bag not in next_gen_bags:
                next_gen_bags[inner_bag] = 0
            next_gen_bags[inner_bag] += inner_bag_count * parent_gen_bag_count
    cumulative_bag_count += sum(next_gen_bags.values())
    parent_gen_bags = next_gen_bags
print(cumulative_bag_count)