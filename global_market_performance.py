'''
Testing of geopandas with global market data
installing geopandas involves installing each dependency on its own.
pip install pipwin
pip install gdal
pipwin install fiona
pip install geopandas

exchangerates docs:
https://exchangeratesapi.io/documentation/

'''
from datetime import datetime
import io
from urllib.request import urlopen
import geopandas as gpd
import geopandas.datasets
import pandas as pd
import pygeos
import time
import pandas as pd
import numpy as np
import json
import ssl
import collections
import requests
# from bokeh.io import output_notebook, show, output_file, export_png
# from bokeh.plotting import figure
# from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
# from bokeh.palettes import brewer
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
import seaborn as sns
import difflib
import yfinance as yf
from pandas._libs.tslibs.offsets import BDay

# from mpl_toolkits.axes_grid1 import make_axes_locatable
# from selenium import webdriver
# from selenium.webdriver.firefox.service import Service
# from webdriver_manager.firefox import GeckoDriverManager
# import geckodriver_autoinstaller

# geckodriver_autoinstaller.install()  # Check if the current version of geckodriver exists
#                                      # and if it doesn't exist, download it automatically,
#                                      # then add geckodriver to path

# driver = webdriver.Firefox()
# driver.get("http://www.python.org")
# assert "Python" in driver.title


sns.set()

# set context for certificates at FMP
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
# Vincent's key
api_key = '57008807e6292948d06c6e89dc934672'

# turn on pygeos
gpd.options.use_pygeos = True


# %% Retrieve the shape values for the map and store in an excel sheet
# load the geometry data
shape_file = 'ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp'

# Read shapefile using Geopandas
gdf = gpd.read_file(shape_file)[['ADMIN', 'ADM0_A3', 'geometry']]

# Rename columns.
gdf.columns = ['country', 'country_code', 'geometry']
gdf.head()

# drop antarctica
# print(gdf[gdf['country'] == 'Antarctica'])

# Drop row corresponding to 'Antarctica'
gdf = gdf.drop(gdf.index[159])

# gdf.to_excel('country_shape_vals.csv')

# %% Functions


def get_stock_prices(symbol, start_date, end_date):
    """
    Receive the content of ``url``, parse it as JSON and return the object.
    """

    url = ("https://financialmodelingprep.com/api/v3/historical-price-full/" +
           "{}?from={}&to={}&apikey={}".format(symbol, start_date,
                                               end_date, api_key))

    response = urlopen(url, context=ssl_context)
    data = response.read().decode("utf-8")

    prices = json.loads(data)

    prices = pd.DataFrame(prices['historical']) \
        .set_index('date').sort_index()

    return prices


def get_yahoo_prices(ticker, start_date, end_date):

    # load the data
    df_data = yf.Ticker(ticker).history(start=start_date, end=end_date)

    return df_data[['Close']]


def period_return(ticker, start_date, end_date):
    """
    Function to calculate the return for a given ticker and the supplied time period
    :param ticker: str - ticker of the etf
    :param start_date: str - should be the closing pate of the previous period
        e.g, use 2021-12-31 if you want 2022-01-01 to be the period start
    :param end_date: str
    :return: dataframe of period performance for each ticker
    """

    df_prices = get_stock_prices(ticker, start_date, end_date)['adjClose'].to_frame(name=ticker)
    period_ror = (df_prices.iloc[-1] / df_prices.iloc[0] - 1) * 100

    return np.round(period_ror, 2)


def get_country_weights(symbol):
    """
    Receive the content of ``url``, parse it as JSON and return the object.
    """

    url = ("https://financialmodelingprep.com/api/v3/etf-country-weightings/" +
           "{}?apikey={}".format(symbol, api_key))

    response = urlopen(url, context=ssl_context)
    data = response.read().decode("utf-8")

    weightings = json.loads(data)

    df_weightings = pd.DataFrame(weightings).set_index('country').sort_values(by='weightPercentage',
                                                                              ascending=False)

    df_weightings = df_weightings['weightPercentage'].str.rstrip('%').astype('float')

    return df_weightings


def get_etf_holdings(symbol):
    """
    Receive the content of ``url``, parse it as JSON and return the object.
    """

    url = ("https://financialmodelingprep.com/api/v3/etf-holder/" +
           "{}?apikey={}".format(symbol, api_key))

    response = urlopen(url, context=ssl_context)
    data = response.read().decode("utf-8")

    weightings = json.loads(data)

    df_weightings = pd.DataFrame(weightings)

    # df_weightings = df_weightings['weightPercentage'].str.rstrip('%').astype('float')

    return df_weightings


def fx_period_ror(ticker_list, start_date, end_date):
    """
    Determine the period ROR for each required currency
    """
    fx_ror_dict = {}

    for ticker in ticker_list:
        try:
            fx_prices = get_yahoo_prices(ticker, start_date, end_date)
            fx_ror_dict[ticker] = float(fx_prices.iloc[-1] / fx_prices.iloc[0] - 1)
        except:
            print(f'{ticker} could not be retrieved')

    return fx_ror_dict

# %% load in the tickers and retrieve the stock prices to calculate performance


df_tickers = pd.read_excel('country_tickers.xlsx', index_col=0, header=0)
start_date = '2021-12-31'
end_date = '2022-03-18'

# initialize dicts and df
returns_dict = collections.defaultdict(dict)
df_returns = pd.DataFrame()

# cycle through tickers, retrieve pricing data for the specified time range
# and calculate the performance

begin_time = time.perf_counter()

for ticker, fx_symbol in list(zip(df_tickers.index, df_tickers['FX_Symbol'])):
    if fx_symbol != 'USD=X':
        period_ror = period_return(ticker, start_date, end_date)
        returns_dict[ticker]['Return'] = period_ror.values[0]
        returns_dict[ticker]['FX Return'] = fx_period_ror([fx_symbol], start_date, end_date)[fx_symbol]

# convert dict to df and concat to df_tickers
df_returns = pd.DataFrame(data=returns_dict).T
df_returns['Adjusted Return'] = np.round(((1+df_returns['Return'] / 100) * (1 + df_returns['FX Return']) - 1) * 100, 2)

end_time = time.perf_counter()

total_time = end_time - begin_time
print(f'Code executed in {total_time} seconds')

df_merged = pd.concat([df_tickers, df_returns], axis=1)

# add developed and emerging labels
developed = [
    'Canada',
    'United States of America',
    'Austria',
    'Belgium',
    'Denmark',
    'Finland',
    'France',
    'Germany',
    'Ireland',
    'Israel',
    'Italy',
    'Netherlands',
    'Norway',
    'Portugal',
    'Spain',
    'Sweden',
    'Switzerland',
    'United Kingdom',
    'Australia',
    'Hong Kong',
    'Japan',
    'New Zealand',
    'Singapore',
]

# merge with the geometry data
df_joined = gdf.merge(df_merged, left_on='country', right_on='Country', how='left')
df_joined.drop('Country', axis=1, inplace=True)
df_joined.rename(columns={'country': 'Country'}, inplace=True)
# fill nas with 'No Data' so that the map doesn't show it as a zero return
# df_joined.fillna('No Data', inplace=True)

# %% Merge the country weightings in VT
# read the VT weightings csv file
df_vt_weightings = pd.read_csv('Total World Stock ETF_Market diversification (% of equities).csv').dropna()
# convert the percentage string to float
df_vt_weightings['Weight'] = df_vt_weightings['Weight'].str.rstrip('%').astype('float')

# To merge the country weights in VT:
# convert the df_joined countries to list
country_list = df_joined['Country'].to_list()

for country in df_vt_weightings['Country']:
    try:
        closest = difflib.get_close_matches(country, country_list)
        df_vt_weightings.replace(country, closest[0], inplace=True)
    except:
        pass

df_joined = df_joined.merge(df_vt_weightings, left_on='Country', right_on='Country', how='left')

# %% get country weightings of MSCI World for developed markets table

df_xwd = pd.read_csv('XWD_holdings.csv')
for country in df_xwd['Location of Risk']:
    try:
        closest = difflib.get_close_matches(country, country_list)
        df_xwd.replace(country, closest[0], inplace=True)
    except:
        pass

df_xwd = df_xwd.groupby('Location of Risk').sum().reset_index()
df_xwd.rename(columns={'Location of Risk': 'Country',
                       'Weight (%)': 'XWD Weight (%)'}, inplace=True)

df_joined = df_joined.merge(df_xwd[['Country', 'XWD Weight (%)']], left_on='Country', right_on='Country',
                            how='left')

# %% get the weightings of EM countries in EEM

df_eem = pd.read_csv('EEM_holdings.csv')
for country in df_eem['Location']:
    try:
        closest = difflib.get_close_matches(country, country_list)
        df_eem.replace(country, closest[0], inplace=True)
    except:
        pass

df_eem = df_eem.groupby('Location').sum().reset_index()
df_eem.rename(columns={'Location': 'Country',
                       'Weight (%)': 'EEM Weight (%)'}, inplace=True)

df_joined = df_joined.merge(df_eem[['Country', 'EEM Weight (%)']], left_on='Country', right_on='Country',
                            how='left')


# %% Plot

# find min and max returns for color map
# min_return = df_returns.min()
# max_return = df_returns.max()
#
# # convert the data to json for bokeh use
# merged_json = json.loads(df_joined.to_json())
#
# # Convert to String like object.
# json_data = json.dumps(merged_json)
#
# # Input GeoJSON source that contains features for plotting.
# geosource = GeoJSONDataSource(geojson=json_data)
#
# # Define a sequential multi-hue color palette.
# palette = brewer['YlGnBu'][8]
#
# # Reverse color order so that dark blue is highest obesity.
# palette = palette[::-1]
#
# # Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
# color_mapper = LinearColorMapper(palette=palette, low=min_return, high=max_return, nan_color='#d9d9d9')
#
# # Create color bar.
# color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=600, height=20,
#                      border_line_color=None, location=(0, 0), orientation='horizontal',
#                      )
#
# # Create figure object.
# p = figure(title='YTD Country Performance', plot_height=600, plot_width=1000, toolbar_location=None)
# p.xgrid.grid_line_color = None
# p.ygrid.grid_line_color = None
#
# # Add patch renderer to figure.
# p.patches('xs', 'ys', source=geosource,fill_color={'field': 'Return', 'transform': color_mapper},
#           line_color='black', line_width=0.25, fill_alpha=1)
#
# # Specify figure layout.
# p.add_layout(color_bar, 'below')
#
# export_png(p, filename='test.png')
#
# show(p)

# %% Plot using matplotlib instead of bokeh

# fig, ax = plt.subplots(1, 1)
#
# divider = make_axes_locatable(ax)
#
# cax = divider.append_axes("right", size="5%", pad=0.1)
#
# df_joined.plot(column='Return',
#                ax=ax,
#                # figsize=(40, 20),
#                legend=True,
#                legend_kwds={'label': "Return (%)",
#                             'orientation': 'vertical'},
#                cax=cax,
#                edgecolor='black',
#                missing_kwds={'color': 'lightgrey',
#                              'label': 'No Data'}
#                )
# ax.set_axis_off()
# ax.margins(0)
# ax.apply_aspect()
# # plt.tight_layout()
# # plt.show()
#
# plt.savefig('test.png')

# %% matplotlib graphing

# set the color scale
c = ["darkred", "red", "lightcoral", "palegreen", "green", "darkgreen"]
v = [0, .2, .4, .6, .8, 1.]
l = list(zip(v, c))
color_palette = LinearSegmentedColormap.from_list('rg', l, N=256)
norm = TwoSlopeNorm(vmin=df_joined['Adjusted Return'].min(), vcenter=0, vmax=df_joined['Adjusted Return'].max())

# create the plot
ax = df_joined.plot(column='Adjusted Return',
                    figsize=(40, 20),
                    cmap=color_palette,
                    legend=True,
                    legend_kwds={'label': "Return (%)",
                                 'orientation': 'horizontal',
                                 'shrink': 0.7,
                                 'pad': 0.02,
                                 },
                    edgecolor='black',
                    missing_kwds={'color': 'lightgrey',
                                  'label': 'No Data'},
                    norm=norm
                    )

fig = ax.figure
cb_ax = fig.axes[1]
cb_ax.tick_params(labelsize=20)

plt.yticks([])
plt.xticks([])
plt.tight_layout()
# plt.show()

plt.savefig(f'global_market_performance_{end_date}.png', bbox_inches='tight')


# %% create tables

df_developed = df_joined[df_joined['Country'].isin(developed)].sort_values('Adjusted Return', ascending=False)
df_emerging = df_joined[~df_joined['Country'].isin(developed)].sort_values('Adjusted Return', ascending=False)

dev_top_5 = df_developed[df_developed['Adjusted Return'].notna()][['Country',
                                                                   'Adjusted Return', 'XWD Weight (%)']].head(5)
dev_bottom_5 = df_developed[df_developed['Adjusted Return'].notna()][['Country',
                                                                      'Adjusted Return', 'XWD Weight (%)']].tail(5)

em_top_5 = df_emerging[df_emerging['Adjusted Return'].notna()][['Country',
                                                                'Adjusted Return', 'EEM Weight (%)']].head(5)
em_bottom_5 = df_emerging[df_emerging['Adjusted Return'].notna()][['Country',
                                                                   'Adjusted Return', 'EEM Weight (%)']].tail(5)

top_5 = df_joined[['Country', 'Adjusted Return', 'Weight']].sort_values(by='Adjusted Return', ascending=False).head(5)
bottom_5 = df_joined[['Country', 'Adjusted Return', 'Weight']].sort_values(by='Adjusted Return', ascending=False,
                                                                           na_position='first').tail(5)

top_5.rename(columns={'Adjusted Return': 'Return (%)',
                      'Weight': 'Weight (%)*'},
             inplace=True)

bottom_5.rename(columns={'Adjusted Return': 'Return (%)',
                         'Weight': 'Weight (%)*'},
                inplace=True)

dev_top_5.rename(columns={'Adjusted Return': 'Return (%)',
                          'XWD Weight (%)': 'Weight (%)**'},
                 inplace=True)

dev_bottom_5.rename(columns={'Adjusted Return': 'Return (%)',
                             'XWD Weight (%)': 'Weight (%)**'},
                    inplace=True)

em_top_5.rename(columns={'Adjusted Return': 'Return (%)',
                         'EEM Weight (%)': 'Weight (%)^'},
                inplace=True)

em_bottom_5.rename(columns={'Adjusted Return': 'Return (%)',
                            'EEM Weight (%)': 'Weight (%)^'},
                   inplace=True)

# %% Currency adjustment

forex_list = df_tickers['FX_Symbol'].unique().tolist()

test = fx_period_ror(forex_list, start_date, end_date)