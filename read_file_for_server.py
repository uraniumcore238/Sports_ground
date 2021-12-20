import json
from local_settings import DEFAULT_JSON_FILE_PATH


def read_json_file():

    file = DEFAULT_JSON_FILE_PATH

    with open(file) as json_file:

        data = json.load(json_file)
        for line in data:
            print(f"id Площадки {line['global_id']}  и тип {line['NameSummer']}")
        print(data)


if __name__ == "__main__":
    read_json_file()
