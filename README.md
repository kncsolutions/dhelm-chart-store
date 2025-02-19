# dhelm-chart-store
To use this tool clone this package.
At first daily login through Dhelm-Screener is required to use this tool.
## The python version
The tool is tested with python 3.7. 
## The main executable
**The main executable is kite_chart_store.py**
Open a command window and navigate to `dhelm-chart-store` folder. The run the command.
```python
py kite_chart_store.py
```

## Parameter Fill up
To generate charts, the `chart_store_settings.xlsx` file
in `chart_store` folder has to be filled up properly. It has three
columns.
1. `exchange : ` Valid values are from `{NSE, BSE, NFO, MCX}`.
2. `tradingsymbol : ` The valid trading symbol. E.g. `SBIN`.
3. `type : ` Valid values are from `{index,scrip}`. If the trading symbol is an index, then select index,
otherwise select scrip.

## Chart generation settings.
To integrate different indicators, manipulate the `DhelmChartStore.py` file.

## Other important files
Once in a month preferably at the beginning, the `instrument_list_downloader.py` file should be executed.

## Other execution notes
If you are using anaconda, then on windows the following batch files can be used for one click
execution:
1. `kite_chart_store.bat : ` To generate charts.
2. `datadumper.bat : ` To download the list of valid instruments.
To use the batch files, the root must be set at line 1 of the batch files, to your anaconda
path.

## Results
The generated charts are stored in `chart_store/chart` folder.
