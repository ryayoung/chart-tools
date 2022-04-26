from chart_tools.data.datasource import DataSource
import pandas as pd


class Library:
    load_help = True
    load_help_all = True

    def __init__(self, url):
        self.url = url
        self.data = None
        self.sources = None

        self.load(self.url)

    def __repr__(self):
        if self.sources != None:
            string = ""
            for s in self.sources.values():
                string += s.__repr__() + "\n"
            return string
        
    def load(self, url):
        # Online library
        if url.startswith("https"):
            try:
                self.data = dict(requests.get(url).json())
            except Exception as e:
                self.data = None
        # Local library
        else:
            try:
                with open(url) as f:
                    self.data = json.load(f)
            except Exception as e:
                print(e)
                self.data = None
        
        if self.data:
            # Make sure library follows correct structure
            for key in list(self.data.keys()):
                if not sorted(list(self.data[key].keys())) == sorted(['u', 'r', 'b', 'p']):
                    raise ValueError("Wrong library structure. Keys must be ['u', 'r', 'b', 'p']")

            self.url = url
            self.sources = { k: DataSource(v['u'], v['r'], v['b'], v['p'], k) for k, v in self.data.items() }

    
    def display_sources(self) -> None:
        if self.sources:
            for s in self.sources.values():
                print(f" '{s.name}':{(10-len(s.name))*' '}{s.root}")


    def display_all(self) -> None:
        """
        Documentation
        """
        if not self.sources:
            return
        
        for s in self.sources.values():
            if s.datasets == []:
                continue
            print(f"'{s.name}'  -  {s.root}")
            print("---------------------------------")
            s.display_datasets(header=False, trunc=15)
    

    def load_data(self, source:str=None, file:str=None, save=True, **kwargs) -> pd.DataFrame:
        if not self.sources:
            return
        
        if not source and not file:
            if Library.load_help:
                print("Use load_data(source_name, filename) to load dataframe")
                print("Use load_data(source_name) to see all datasets in a source.")
                print("Use load_data('all') to see all datasets.")
                Library.load_help = False
            print("---------\nSOURCES:")
            self.display_sources()
            return
        
        if source == 'all' and not file:
            if Library.load_help_all:
                print("(Use load_data(source_name, filename) to load data)")
                print("(Use load_data(source_name) to see available datasets in source)")
                print("")
                Library.load_help_all = False
            self.display_all()
            return
        
        if not file:
            if source in self.sources.keys():
                self.sources[source].display_datasets()
                return None
            if "main" in self.sources:
                if source in self.sources.get("main", {}).datasets:
                    return self.sources['main'].load(source, save, **kwargs)

            print(f"Unknown source, '{source}'")
            return
            
        if source not in self.sources:
            print(f"Unknown source, '{source}'")
            return
        
        if self.sources[source].datasets != []:
            return self.sources[source].load(file, save, **kwargs)




# --------------------------------------------------------------------------------
default_lib = Library("https://raw.githubusercontent.com/ryayoung/datasets/main/chart-tools-default-library.json")

def set_library(url):
    default_lib.load(url)

def load_data(source=None, file=None, save=True, **kwargs) -> pd.DataFrame:
    return default_lib.load_data(source, file, save, **kwargs)
