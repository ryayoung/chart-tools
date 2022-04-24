<h1> chart-tools &nbsp;&nbsp;&nbsp; <a href="https://pypi.org/project/chart-tools/" alt="Version"> <img src="https://img.shields.io/pypi/v/chart-tools.svg" /></a> </h1>

## Install & Use
```
pip install chart-tools
```
In python...
```py
import chart_tools as ct
```

<br>

# Load some data

### We can use pre-defined sources ...
```py
ct.load_data('covid', 'countries-aggregated') # returns dataframe
```
<img width="469" alt="Screen Shot 2022-04-23 at 10 36 10 PM" src="https://user-images.githubusercontent.com/90723578/164956857-b1834946-7f2f-4c1f-970c-a6bc072229f3.png">

#### How do we know what's available?
```py
ct.load_data()
```
Output:
```
Use load_data(source_name, filename) to load dataframe
Use load_data(source_name) to see all datasets in a source.
Use load_data('all') to see all datasets.
---------
SOURCES:
 'main':      https://github.com/ryayoung/datasets/tree/main/data
 'covid':     https://github.com/datasets/covid-19/tree/main/data
 'football':  https://github.com/datasets/football-datasets/tree/master/datasets
 'sp500':     https://github.com/datasets/s-and-p-500-companies/tree/master/data
 'openml':    https://github.com/datasets/openml-datasets/tree/master/data
```


#### Let's see what's in 'covid', and find the 'countries-aggregated' set
```py
ct.load_data('covid')
```
```
Datasets for 'covid':
---------------------------
  countries-aggregated
  key-countries-pivoted
  reference
  time-series-19-covid-combined
  us_confirmed
  us_deaths
  us_simplified
  worldwide-aggregate
```

#### What about larger sources with sub-directories?
```py
ct.load_data('football')
```
```
Datasets for 'football':
(refer files inside folders using the full path. Ex: 'folder/file')
---------------------------
  la-liga/
    season-0809
    season-0910
    season-1011
    season-1112
    season-1213
    season-1314
    season-1415
    season-1516
    season-1617
    season-1718
    season-1819
  premier-league/
    season-0910
    season-1011
```

#### To get one of these, use the full path
```py
ct.load_data('football', 'la-liga/season-0809')
```
<img width="642" alt="Screen Shot 2022-04-23 at 10 51 59 PM" src="https://user-images.githubusercontent.com/90723578/164957212-1288a9b3-e1d0-4ec4-a75e-c4ee89687901.png">

#### See all files available, organized by source & sub-directory
```py
ct.load_data('all')
```
```
(Use load_data(source_name, filename) to load data)
(Use load_data(source_name) to see available datasets in source)

'main'  -  https://github.com/ryayoung/datasets/tree/main/data
---------------------------------
  ames_engineered
  ames_full
  ames_mini
  stock-tweets

'covid'  -  https://github.com/datasets/covid-19/tree/main/data
---------------------------------
  countries-aggregated
  key-countries-pivoted
  reference
```

#### `load_data` takes the **same** keyword arguments as `pd.read_csv`. For example, set `header=None`
```py
ct.load_data('covid', 'countries-aggregated', header=None)
```
<img width="459" alt="Screen Shot 2022-04-23 at 11 43 37 PM" src="https://user-images.githubusercontent.com/90723578/164958366-381d38a3-3268-4294-a250-6fabf1c354ea.png">

<br>

### Create your own `DataSource`
Let's build a source for my [`/datasets`](https://github.com/ryayoung/datasets) repository. You'll need 4 things:
- `user`: GitHub username
- `repo`: Name of repository
- `branch`: Which branch it's in
- `path`: (optional) directory within the repo that holds all files and sub-directories containing files.
```py
s = ct.DataSource("ryayoung", "datasets", "main", "data")
print(s.datasets)
```
```
['ames_engineered', 'ames_full', 'ames_mini', 'stock-tweets']
```

<br>

```py
s.load("ames_mini", index_col=0)
```
<img width="451" alt="Screen Shot 2022-04-23 at 11 46 43 PM" src="https://user-images.githubusercontent.com/90723578/164958463-8621bc79-562b-4d91-8222-d684e3cccb3c.png">



#### `DataSource` will recursively find all csv files in all the sub-directories within your path.
#### For example, let's build the same source without specifying a path
```py
s = ct.DataSource("ryayoung", "datasets", "main")
print(s.datasets)
```
```
['data/ames_engineered', 'data/ames_full', 'data/ames_mini', 'data/stock-tweets']
```
#### This works the same, but if we want to load a dataset we'd have to use the full path, `data/ames_mini`
#### Here are some examples of using our datasource.

```py
print(s.subdirs)
print(s.datasets)
print(s.datasets_base)
```
```
['data']
['data/ames_engineered', 'data/ames_full', 'data/ames_mini', 'data/stock-tweets']
['ames_engineered', 'ames_full', 'ames_mini', 'stock-tweets']
```

<br>

```py
# Since we never specified a path, we might need to say "path/file"
# like this: s.load("data/ames_mini")
# But since all filenames are unique across all directories, we can just ...
s.load("ames_mini")
# and the file will be found. If two directories contain the same filename, this code won't run
```
<img width="422" alt="Screen Shot 2022-04-23 at 11 55 45 PM" src="https://user-images.githubusercontent.com/90723578/164958729-fefbe6ed-4c99-4755-8e8a-0c8787d7b2d6.png">

`load()` takes the same keyword arguments as `pd.read_csv()`
```py
s.load("ames_mini", index_col=0, usecols=['Id', 'OverallCond', 'LotArea'])
```
<img width="210" alt="Screen Shot 2022-04-23 at 11 59 39 PM" src="https://user-images.githubusercontent.com/90723578/164958838-2c1bf900-63c3-4d87-b29e-99ac852f078b.png">

#### Let's use a more complex source, [`/football-datasets`](https://github.com/datasets/football-datasets/tree/master/datasets) in github's `datasets` account
```py
s = ct.DataSource("datasets", "football-datasets", "master", "datasets")
print(s.root) # Clickable url to take you to the datasource
print(s.req_url) # Url to request github's api for all info on repository
print(s.file_url("la-liga/season-0809")) # url to raw, downloadable file

```
```
https://github.com/datasets/football-datasets/tree/master/datasets
https://api.github.com/repos/datasets/football-datasets/git/trees/master?recursive=1
https://raw.githubusercontent.com/datasets/football-datasets/master/datasets/la-liga/season-0809.csv

```

<br>

```py
s.display_datasets(trunc=14, header=False)
```
```
  la-liga/
    season-0809
    season-0910
    season-1011
    season-1112
    season-1213
    season-1314
    season-1415
    season-1516
    season-1617
    season-1718
    season-1819
  serie-a/
    season-0809
      (38 more files in datasets/football-datasets)
```

<br>

```py
s.subdirs # sub-directories containing 1 or more .csv files
```
```
['la-liga', 'serie-a', 'ligue-1', 'premier-league', 'bundesliga']
```

<br>

```py
s.dir_contents('serie-a') # see all csv files in 'serie-a' directory
```
```
['season-0809', 'season-0910', 'season-1011', 'season-1112', 'season-1213', 'season-1314', 'season-1415', 'season-1516', 'season-1617', 'season-1718', 'season-1819']
```
#### In this source, files share the same names across directories. So we need to use the full path when loading them
```py
s.load("serie-a/season-0809")
```
<img width="472" alt="Screen Shot 2022-04-24 at 12 19 39 AM" src="https://user-images.githubusercontent.com/90723578/164959543-69abf757-1eff-4a36-9d94-f5c463b00ea8.png">











