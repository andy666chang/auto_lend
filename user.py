
import os, json


def load_user(file):
    data = ""
    with open(file) as f:
        data = json.load(f)

    data = data['user']
    return data


if __name__ == '__main__':
    data = load_user("database.json")

    print(type(data))
    for i in data:
        print(i)
