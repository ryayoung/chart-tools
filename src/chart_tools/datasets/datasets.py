import pandas as pd
import requests
import json
from chart_tools.datasets.locations import locations

# other_names = 'https://api.github.com/repos/ryayoung/datasets/git/trees/main?recursive=1'

def build_source(s, name):
    return f"https://raw.githubusercontent.com/{s['u']}/{s['r']}/{s['b']}/{s['l']}{name}.csv"


def build_request(s):
    return f"https://api.github.com/repos/{s['u']}/{s['r']}/git/trees/{s['b']}?recursive=1"


def validate(name, source):
    # If no name is passed, provide help
    if not name:
        print("Call load_data('help') for a live update on all available data sources and their datasets.")
        print("Call load_data('help', 'source') for a list of sources")
        print("Call load_data('help', <valid_source>) for a live update on all datasets in a given source")
        return False

    elif name == 'help' and source == 'source':
        print("Available data sources:")
        print("----------------------")
        print(*locations.keys(), sep="\n")
        return False

    elif name == 'help':
        keys = locations.keys() if source == None else [source]
        if len(keys) == 1:
            print(f"Available datasets for {source}:")
        else:
            print("All available datasets")
        print("------------------")
        for source in keys:
            s = locations[source]
            url = build_request(s)
            available = requests.get(url).json()['tree']
            names = [f"'{f['path'].removesuffix('.csv').removeprefix(s['l'])}'"
                        for f in available if ".csv" in f['path']]
            print(f"{source}:\n  ", end="")
            print(*names, sep="\n  ")
        return False
    else:
        return True


def load_data(name=None, source=None, **kwargs):
    if not validate(name, source):
        return None
    
    if name and source == None:
        source = 'ryayoung'

    s = locations.get(source, None)
    if not s:
        print(f"Unknown source '{source}'. The following are available:")
        print("-------------------------------------------")
        print(*locations.keys(), sep=", ")
        return None

    url = build_source(s, name)
    
    # Now we know the source is valid.
    # Try to fetch the dataset
    try:
        df = pd.read_csv(url, **kwargs)
        return df
    except Exception as e:
        url = build_request(s)
        r = requests.get(url) # This should work, since source is valid
        res = r.json()['tree']
        names = [f"'{f['path'].removesuffix('.csv').removeprefix(s['l'])}'"
                    for f in res if ".csv" in f['path']]
        print(f"Couldn't find dataset.\nThe following are currently available for '{source}':")
        print("-------------------------------------------------------")
        print(*names, sep=", ")
        return None


# print(load_data(""))
