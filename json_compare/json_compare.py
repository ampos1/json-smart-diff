import json
import sys
import tabulate

file_1 = sys.argv[1]
file_2 = sys.argv[2]


def flatten_json(nested_json):
    flattened_json = {}

    def flatten(json_object, name=''):
        if type(json_object) is dict:
            for key in json_object:
                flatten(json_object[key], name + key + '_')
        elif type(json_object) is list:
            i = 0
            for key in json_object:
                flatten(key, name + str(i) + '_')
                i += 1
        else:
            flattened_json[name[:-1]] = json_object
    flatten(nested_json)
    return flattened_json


def process_input(file):
    with open(file, 'r') as file_bytes:
        file_strings = file_bytes.read()
        file_dictionary = json.loads(file_strings)
    return flatten_json(file_dictionary)


def compare_keys(dict_1, dict_2):
    key_tup = ([], [], [])
    for key in dict_1:
        if key in dict_2:
            key_tup[0].append(key)
            continue
        key_tup[1].append(key)

    for key in dict_2:
        if key not in dict_1:
            key_tup[2].append(key)

    return key_tup


def print_unique_keys(unique_keys):
    if len(unique_keys[0]) == 0 and len(unique_keys[1]) == 0:
        print('\n%s and %s have identical keys!' % (file_1, file_2))
        return
    print("\nTable of unique keys:\n")
    required_rows = max(len(unique_keys[0]), len(unique_keys[1]))
    all_rows = []

    for i in range(required_rows):
        row_of_unique_keys = [None]*2

        try:
            row_of_unique_keys[0] = unique_keys[0][i]
        except IndexError:
            row_of_unique_keys[0] = ""

        try:
            row_of_unique_keys[1] = unique_keys[1][i]
        except IndexError:
            row_of_unique_keys[1] = ""

        all_rows.append(row_of_unique_keys)

    print(tabulate.tabulate(all_rows, headers=[
          file_1, file_2], tablefmt="presto"))


def compare_values(dict_1, dict_2, shared_keys):
    if len(shared_keys) == 0:
        print("%s and %s have no common keys" % (file_1, file_2))
        return

    print("\nTable of inconsistent key value pairs:\n")
    all_rows = []
    for key in shared_keys:
        if dict_1[key] != dict_2[key]:
            row_of_shared_keys = []
            row_of_shared_keys.append(key)
            row_of_shared_keys.append(dict_1[key])
            row_of_shared_keys.append(dict_2[key])
            all_rows.append(row_of_shared_keys)

    print(tabulate.tabulate(all_rows, headers=[
          "key", file_1, file_2], tablefmt="fancy_grid"))


dict_1 = process_input(file_1)
dict_2 = process_input(file_2)
keys = compare_keys(dict_1, dict_2)
unique_keys = [keys[1], keys[2]]
print_unique_keys(unique_keys)
compare_values(dict_1, dict_2, keys[0])
