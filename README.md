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
- The [`load_data()`](/sampledata.md) function and [`DataSource`](/sampledata.md) object use Github's API to explore file structures in repositories containing `.csv` files, and easily load files into dataframes.
- `load_data()` uses a pre-defined set of DataSources from Github, allowing you to explore the .csv files within them and load a file into a dataframe, all with one line of code.
- If you have a repository you'd like to get data from, you can create a `DataSource` object which lets you explore its file structure and easily load data, without ever visiting Github!

# Charts & Visualization

### [`superheat`](/superheat.md)
- A "super" correlation heatmap you can't find elsewhere

