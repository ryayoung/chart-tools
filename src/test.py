import chart_tools as ct
from dataclasses import dataclass
import time

# s = ct.DataSource('ryayoung', 'datasets', 'main', 'data')

# ct.set_library("https://raw.githubusercontent.com/ryayoung/datasets/main/test-library.json")

df = ct.load_data('ames_mini')

plt, ax = ct.superheat(df.corr())
plt.show()
# ct.library_help()
# print(s.load('ames_mini'))
# 
# 
# name = "data/ames"
# 
# print(name.split('/')[-1])
