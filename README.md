<h1> chart-tools &nbsp;&nbsp;&nbsp; <a href="https://pypi.org/project/chart-tools/" alt="Version"> <img src="https://img.shields.io/pypi/v/chart-tools.svg" /></a> </h1>

## Install & Use
```
pip install chart-tools
```
```py
import chart_tools as ct
```

<br>

# [Data Interface](/sampledata.md)

#### Easily load datasets and explore available sources with one line of code
- The [`load_data()`](/sampledata.md) function and [`DataSource`](/sampledata.md) object use Github's API to explore file structures in repositories containing `.csv` files, and easily load files into dataframes. Chart-tools has a pre-defined library (collection of repositories) for you to explore within your notebook and load data from.

#### Robust caching system designed for Jupyter notebooks, performing great with large datasets.
- Any dataframe you load gets cached in memory, remembering which pandas keyword arguments you used when loading the file. Next time you load it, you'll get a _copy_ of the cached dataframe, unless you pass different keyword arguments. Not only is this great for performance with large datasets, but it also eliminates the common need to declare a `df_raw = ...` and then use `df = df_raw.copy()` to get your original data again. 

#### Has a pre-defined library of data sources to explore, and lets you easily define your own library
- 

#### Save an entire Github repository file structure (csv files only) to your desktop
- 

# [Charts & Visualization](/superheat.md)

### [`superheat`](/superheat.md)
- A "super" correlation heatmap you can't find elsewhere

