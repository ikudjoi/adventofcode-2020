import os
import re

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.readlines()

required_fields = set([line.split(' ')[0] for line in """byr (Birth Year)
iyr (Issue Year)
eyr (Expiration Year)
hgt (Height)
hcl (Hair Color)
ecl (Eye Color)
pid (Passport ID)""".splitlines()])


def field_valid_phase_1(field):
    return field[0] in required_fields


hair_color_matcher = re.compile(r"^#[\da-f]{6}$")
pid_matcher = re.compile(r"^\d{9}$")


def field_valid_phase_2(field):
    key, value = field
    value = value.strip('\n')
    if key == 'byr':
        return value.isdigit() and 1920 <= int(value) <= 2002

    if key == 'iyr':
        return value.isdigit() and 2010 <= int(value) <= 2020

    if key == 'eyr':
        return value.isdigit() and 2020 <= int(value) <= 2030

    if key == 'hgt':
        if value[-2:] == 'cm':
            value = value[:-2]
            return value.isdigit() and 150 <= int(value) <= 193
        if value[-2:] == 'in':
            value = value[:-2]
            return value.isdigit() and 59 <= int(value) <= 76
        return False

    if key == 'hcl':
        ok_hair = hair_color_matcher.match(value) is not None
        return ok_hair

    if key == 'ecl':
        return value in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

    if key == 'pid':
        pid_ok = pid_matcher.match(value) is not None
        return pid_ok

    return False


def valid_count(validator):
    fields_on_this_passport = list()
    valid_passport_count = 0
    this_password_invalidated = False
    for line in content:
        if line.strip() == '':
            if len(set(fields_on_this_passport)) == len(required_fields) and not this_password_invalidated:
                valid_passport_count += 1
            fields_on_this_passport.clear()
            this_password_invalidated = False
            continue

        fields_on_this_passport_line = [kvp.split(':') for kvp in line.split(' ')]
        valid_fields_on_this_passport_line = [field[0] for field in fields_on_this_passport_line if validator(field)]
        if len(valid_fields_on_this_passport_line) < len([i for i in fields_on_this_passport_line if i[0] != 'cid']):
            this_password_invalidated = True

        fields_on_this_passport.extend(valid_fields_on_this_passport_line)

    # Check last passport
    if len(set(fields_on_this_passport)) == len(required_fields) and not this_password_invalidated:
        valid_passport_count += 1

    print(valid_passport_count)


valid_count(field_valid_phase_1)
valid_count(field_valid_phase_2)
