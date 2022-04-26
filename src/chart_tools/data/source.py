from dataclasses import dataclass
from operator import countOf
import pandas as pd
import requests
import json
import os
from hashlib import md5

default_lib = None


def check_internet():
    """ Don't hit github api if no internet """
    try:
        request = requests.get("https://www.google.com/", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout) as e:
        return False


# ----------------------------------------------------------------------
# Note: change this to DFCache and make it hold all cache data
# ----------------------------------------------------------------------
class KwargDF:

    def __init__(self, df:pd.DataFrame()=None, **kwargs):
        self.df = df
        self.kwarg_str = str(kwargs)

    @property
    def df(self) -> pd.DataFrame():
        return self._df.copy() # return a COPY

    @property
    def kwarg_str(self) -> int:
        return self._kwarg_str



@dataclass
class Source:
    __user: str
    __repo: str
    __branch: str
    __path: str
    __datasets = [str]
    __cached_dfs = {KwargDF} # Can't directly change. Only add/remove/change

    # Getters
    @property
    def user(self):
        return self.__user.strip("/")
    @property
    def repo(self):
        return self.__repo.strip("/")
    @property
    def branch(self):
        return self.__branch.strip("/")
    @property
    def path(self):
        return self.__path.strip("/")

    def cache_get(self, dataset_name=None): # Not property, since we might need just dataset
        if not dataset_name:
            return self.__cached_dfs
        return self.__cached_dfs.get(dataset_name, KwargDF()).df # returns copy

    @property
    def datasets(self) -> list:
        """
        Load datasets only when we try to access them
        """
        if self.__datasets == []:
            self.__datasets = self.refresh_datasets()
        return self.__datasets

    # Getters - calculated
    @property
    def subdirs(self) -> list:
        """
        First layer of sub-directories in datasource.
        """
        return list(set([
                f.split('/')[0] for f in self.datasets if "/" in f
            ]))

    @property
    def datasets_base(self) -> list:
        """
        Base filenames, without path
        """
        return [f.rsplit('/', 1)[-1] for f in self.datasets]

    @property
    def root(self) -> str:
        """
        User-friendly url to visit the source on Github.com
        """
        return f"https://github.com/{self.user}/{self.repo}/tree/{self.branch}/{self.path}"
    
    @property
    def req_url(self) -> str:
        """
        Url to Github API for getting all files in repo and branch
        """
        return f"https://api.github.com/repos/{self.user}/{self.repo}/git/trees/{self.branch}?recursive=1"

    # Setters - include validation logic
    @user.setter
    def user(self, value):
        if "/" in value:
            raise ValueError("Github username can't have slashes")
        self.__user = value

    @repo.setter
    def repo(self, value):
        if "/" in value:
            raise ValueError("Github repository name can't have slashes")
        self.__repo = value

    @branch.setter
    def branch(self, value):
        if "/" in value:
            raise ValueError("Github branch name can't have slashes")
        self.__branch = value

    @path.setter
    def path(self, value):
        if value.endswith("/"):
            raise ValueError("Path must not end with a slash")
        self.__path = value
        # Update datasets since path changed, but only if we have valid data
        if self.user != "" and self.repo != "" and self.branch != "":
            self.refresh_datasets()
    

    def cache_exists(self, key, **kwargs):
        if key in self.__cached_dfs:
            if self.__cached_dfs[key].kwarg_str == str(kwargs):
                return True
        return False


    def cache_add(self, key, df, **kwargs):
        """ Add new frame to cache """
        kwarg_df = KwargDF(df, **kwargs)
        if self.cache_exists(key, **kwargs):
            if not self.__cached_dfs[key] == kwarg_df:
                self.__cached_dfs[key] = kwarg_df
            return
        self.__cached_dfs[key] = kwarg_df


    def cache_pop(self, key):
        self.__cached_dfs.pop(key)


    def file_url(self, filename) -> str:
        """
        Url to raw, downloadable file
        """
        path = f"{self.path}/" if len(self.path) > 0 else self.path
        return f"https://raw.githubusercontent.com/{self.user}/{self.repo}/{self.branch}/{path}{filename}.csv"


    def req_files(self) -> list:
        """ Request files """
        if check_internet():
            return requests.get(self.req_url).json()
        return None
    

    def dir_contents(self, dir) -> list:
        """ Get filenames in directory """
        return [f.removeprefix(f"{dir}/") for f in self.datasets if f.startswith(dir)]


    def load(self, fname, save=True, **kwargs) -> pd.DataFrame:
        # Validate it exists
        # This also validates that datasets are loaded and connection to GH works
        name = None
        if countOf(self.datasets, fname) == 1:
            name = fname
        elif countOf(self.datasets_base, fname) == 1:
            name = [f for f in self.datasets if f.rsplit('/', 1)[-1] == fname][0]
        else:
            raise ValueError(
                "Either the file doesn't exist, or you specified a filename "
                "that is duplicated across multiple sub-directories in the chosen path. "
                "If the latter is true, please use the full subpath instead."
                )

        # Check cache
        if self.cache_exists(name, **kwargs):
            if save == True:
                return self.cache_get(name)
            else:
                # Passing save=False will not only prevent caching, but it will
                # pop an existing cache for that version of the data if exists
                self.cache_pop(name)

        # Load new data, cache, and return
        df = pd.read_csv(self.file_url(fname), **kwargs)
        self.cache_add(name, df, **kwargs)
        return self.cache_get(name)


    def save_cached(self, dir="", **kwargs):
        if dir != "":
            if not os.path.exists(dir):
                os.mkdir(dir)
            dir = f"{dir}/"
        for name, item in self.cache.items():
            item['df'].to_csv(f"{dir}{name}.csv", **kwargs)
        

    def save_all(self, dir="", **kwargs):
        # Make directory for custom path
        if dir != "":
            p = ""
            for d in dir.split("/"):
                if p != "":
                    p = f"{p}/{d}"
                else:
                    p = d
                if not os.path.exists(p):
                    os.mkdir(p)

        # Make directories for all sub-paths
        for name in self.datasets:
            fullpath = name.split("/")
            if dir != "":
                fullpath = [dir] + fullpath
            p = None
            if len(fullpath) > 1:
                path = fullpath[:-1]
                p = ""
                for d in path:
                    if p != "":
                        p = f"{p}/{d}"
                    else:
                        p = d
                    if not os.path.exists(p):
                        os.mkdir(p)

        # Save datasets
        for name in self.datasets:
            save = False if name not in self.cache else True
            df = self.load(name, save=save, **kwargs)
            if dir != "":
                df.to_csv(f"{dir}/{name}.csv", **kwargs)
            else:
                df.to_csv(f"{name}.csv", **kwargs)
        

    def refresh_datasets(self):
        res = self.req_files()
        if not res:
            return []

        if res.get("message") == "Not Found":
            raise ValueError("No files found. Likely an invalid data source")
        
        return [f['path'].removesuffix('.csv').removeprefix(f"{self.path}/")
                    for f in res['tree'] if ".csv" in f['path']]


