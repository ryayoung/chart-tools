import pandas as pd
import requests
import json
from locations import locations

other_names = 'https://api.github.com/repos/ryayoung/datasets/git/trees/main?recursive=1'

def build_source(key, name):
    s = locations[key]
    return "https://raw.githubusercontent.com/{s['u']}/{s['r']}/{s['b']}/{s['l']}{name}.csv"


def build_request(key):
    s = locations[key]
    return "https://api.github.com/repos/{s['u']}/{s['r']}/git/trees/{s['b']}?recursive=1"


def load_data(name, source='ryayoung', **kwargs):
    url = build_source(source, name)


    try:
        df = pd.read_csv(url, **kwargs)
    except Exception as e:
        s = locations.get(source, None)
        if s == None:
            print("Unknown source. The following are available:")
            print(*locations.keys(), sep=", ")
            return None
        else:
            url = build_request(source)
            r = requests.get(url)
            res = r.json()['tree']
            names = [f"'{f['path'].removesuffix('.csv').removeprefix(s['l'])}'"
                        for f in res if ".csv" in f['path']]
            print("Couldn't find dataset. The following are currently available:")
            print(*names, sep=", ")
            return None

    return df

print(load_data(""))
