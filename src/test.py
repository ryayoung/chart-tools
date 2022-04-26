# import chart_tools as ct
from dataclasses import dataclass

# ct.load_data()


@dataclass
class something:
    dfs: [str]


class KwargDF:

    def __init__(self, df, **kwargs):
        self.__df = df
        self.__kwarg_str = str(kwargs)

    @property
    def df(self):
        return self.__df.copy() # return a COPY

    @property
    def kwarg_str(self) -> int:
        return self.__kwarg_str



# s = KwargDF("hello")

# print(s.__df)


lol = something(["hi", "lol"])

print(lol.dfs)
