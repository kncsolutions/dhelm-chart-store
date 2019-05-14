import pandas as pd
import datetime
from Parameters import ORDER_PARAMETERS
from historical_data_downloader import historical_data_downloader
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.dates import num2date
from matplotlib.dates import date2num, datestr2num
from mpl_finance import candlestick_ochl as candlestick
import numpy as np


class DhelmChartStore:
    """
    :param row: The exchange,tradingsymbol, type information.
    :param api_key: The api_key
    :param access_token: The access_token
    :param options: List of settings. Append 1 to generate 40, 30, 20 period SMAs in daily and weekly charts.
    """
    def __init__(self, row, api_key, access_token, options=[]):
        self.exchange = row['exchange']
        self.tradingsymbol = row['tradingsymbol']
        self.scrip_type = row['type']
        self.api_key = api_key
        self.access_token = access_token
        self.options = options
        self.sma_chain = False
        if 1 in self.options:
            self.sma_chain = True
        self.df_historical_day = pd.DataFrame()
        self.df_historical_week = pd.DataFrame()
        self.df_historical_30min = pd.DataFrame()
        self.__data_length_day = 1400
        self.__data_length_min = 150
        self.time_frame_day = 'day'
        self.time_frame_min = '30minute'
        self.to_dt = datetime.datetime.strftime((datetime.datetime.now()), '%Y-%m-%d %H:%M:%S')
        self.from_dt_day = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(-self.__data_length_day), '%Y-%m-%d %H:%M:%S')
        self.from_dt_min = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(-self.__data_length_min), '%Y-%m-%d %H:%M:%S')
        self.__get_historical_ohlc()
        if self.scrip_type == 'index':
            self.__update_volume_day()
            self.__update_volume_min()
        self.df_historical_day.fillna(method='ffill', inplace=True)
        self.df_historical_30min.fillna(method='ffill', inplace=True)
        self.__gen_weekly_historical()

        self.df_historical_day['log_ret'] = np.log(self.df_historical_day['close'] / self.df_historical_day['close'].shift(1))
        self.df_historical_day['ma50'] = self.df_historical_day['close'].rolling(window=50).mean()
        if self.sma_chain:
            self.df_historical_day['ma40'] = self.df_historical_day['close'].rolling(window=40).mean()
            self.df_historical_day['ma30'] = self.df_historical_day['close'].rolling(window=30).mean()
            self.df_historical_day['ma20'] = self.df_historical_day['close'].rolling(window=20).mean()
        self.df_historical_day['ma200'] = self.df_historical_day['close'].rolling(window=200).mean()
        self.df_historical_day['vol_ma50'] = self.df_historical_day['volume'].rolling(window=50).mean()

        self.df_historical_30min['log_ret'] = np.log(self.df_historical_30min['close'] / self.df_historical_30min['close'].shift(1))
        self.df_historical_30min['ma50'] = self.df_historical_30min['close'].rolling(window=50).mean()
        self.df_historical_30min['ma200'] = self.df_historical_30min['close'].rolling(window=200).mean()
        self.df_historical_30min['vol_ma50'] = self.df_historical_30min['volume'].rolling(window=50).mean()

        self.df_historical_week['log_ret'] = np.log(self.df_historical_week['close'] / self.df_historical_week['close'].shift(1))
        self.df_historical_week['ma50'] = self.df_historical_week['close'].rolling(window=10).mean()
        if self.sma_chain:
            self.df_historical_week['ma40'] = self.df_historical_week['close'].rolling(window=8).mean()
            self.df_historical_week['ma30'] = self.df_historical_week['close'].rolling(window=6).mean()
            self.df_historical_week['ma20'] = self.df_historical_week['close'].rolling(window=4).mean()
        self.df_historical_week['ma200'] = self.df_historical_week['close'].rolling(window=40).mean()
        self.df_historical_week['vol_ma50'] = self.df_historical_week['volume'].rolling(window=10).mean()
        print(self.df_historical_30min)
        print(self.df_historical_day)
        print(self.df_historical_week)
        self.gen_chart(self.df_historical_day, 'day')
        self.gen_chart_min(self.df_historical_30min, '30min')
        self.gen_chart(self.df_historical_week, 'week')

    def __get_historical_ohlc(self):
        if self.exchange == ORDER_PARAMETERS.EXCHANGE_NSE:
            continuous = False
        else:
            continuous = True
        self.df_historical_day = historical_data_downloader(self.api_key,
                                                            self.access_token,
                                                            self.exchange,
                                                            self.tradingsymbol,
                                                            self.from_dt_day,
                                                            self.to_dt,
                                                            self.time_frame_day,
                                                            continuous).get_historical_data()
        if 'close' not in self.df_historical_day:
            return
        for i, r in self.df_historical_day.iterrows():
            self.df_historical_day.at[i, 'date'] = datetime.datetime.strptime(self.df_historical_day.at[i, 'date'],
                                                                  '%Y-%m-%d %H:%M:%S%z').date()
        self.df_historical_day.set_index('date', inplace=True)
        self.df_historical_day.sort_index(inplace=True)
        self.df_historical_day.index = pd.to_datetime(self.df_historical_day.index)

        self.df_historical_30min = historical_data_downloader(self.api_key,
                                                              self.access_token,
                                                              self.exchange,
                                                              self.tradingsymbol,
                                                              self.from_dt_min,
                                                              self.to_dt,
                                                              self.time_frame_min,
                                                              continuous).get_historical_data()

        self.df_historical_30min.set_index('date', inplace=True)
        self.df_historical_30min.sort_index(inplace=True)
        self.df_historical_30min.index = pd.to_datetime(self.df_historical_30min.index)

    def __update_volume_day(self):
        if 'close' not in self.df_historical_day.columns:
            return
        f_name = self.tradingsymbol
        df_scrip_sheet = pd.read_csv('index_details/symbols/' + f_name + '.csv')
        print(df_scrip_sheet)
        for i, r in df_scrip_sheet.iterrows():
            df_s = historical_data_downloader(self.api_key,
                                              self.access_token,
                                              r['exchange'],
                                              r['tradingsymbol'],
                                              self.from_dt_day,
                                              self.to_dt,
                                              self.time_frame_day,
                                              False).get_historical_data()
            if 'close' not in df_s.columns:
                continue
            for i, r in df_s.iterrows():
                df_s.at[i, 'date'] = datetime.datetime.strptime(
                    df_s.at[i, 'date'],
                    '%Y-%m-%d %H:%M:%S%z').date()
            df_s.set_index('date', inplace=True)
            df_s.sort_index(inplace=True)
            df_s.index = pd.to_datetime(df_s.index)
            self.df_historical_day['volume'] = self.df_historical_day['volume'].add(df_s['volume'])

    def __update_volume_min(self):
        if 'close' not in self.df_historical_30min.columns:
            return
        f_name = self.tradingsymbol
        df_scrip_sheet = pd.read_csv('index_details/symbols/' + f_name + '.csv')
        print(df_scrip_sheet)
        for i, r in df_scrip_sheet.iterrows():
            df_s = historical_data_downloader(self.api_key,
                                              self.access_token,
                                              r['exchange'],
                                              r['tradingsymbol'],
                                              self.from_dt_min,
                                              self.to_dt,
                                              self.time_frame_min,
                                              False).get_historical_data()
            if 'close' not in df_s.columns:
                continue
            df_s.set_index('date', inplace=True)
            df_s.sort_index(inplace=True)
            df_s.index = pd.to_datetime(df_s.index)

            self.df_historical_30min['volume'] = self.df_historical_30min['volume'].add(df_s['volume'])

    def __gen_weekly_historical(self):
        logic = {'open': 'first',
                 'high': 'max',
                 'low': 'min',
                 'close': 'last',
                 'volume': 'sum'}

        offset = pd.offsets.timedelta(days=-6)
        self.df_historical_week = self.df_historical_day.resample('W', loffset=offset).apply(logic)

    def gen_chart(self, df_h, time_frame):
        fig = plt.figure()
        title = 'Price-Volume-SMA '+time_frame+' chart for ' + self.tradingsymbol + '(' + str(
            datetime.datetime.now().date()) + ')'

        gs = GridSpec(2, 1, height_ratios=[3, 1])
        x = np.array(list(range(len(df_h))))
        candlesticks = zip(date2num(df_h.index), df_h['open'], df_h['close'], df_h['high'], df_h['low'],
                           df_h['volume'])
        ax = fig.add_subplot(gs[0])
        ax.set_ylabel('Price', size=7, weight='bold')
        ax.set_title(title, fontsize=10, fontweight='bold')
        candlestick(ax, candlesticks, width=1, colorup='g', colordown='r')
        lma50, = ax.plot(date2num(df_h.index), df_h['ma50'], color='b')
        lma200, = ax.plot(date2num(df_h.index), df_h['ma200'], color='r')
        ax.legend([lma50, lma200], ['50 DAY SMA', '200 DAY SMA'], loc="upper left")
        if self.sma_chain:
            lma40, = ax.plot(date2num(df_h.index), df_h['ma40'], color='g')
            lma30, = ax.plot(date2num(df_h.index), df_h['ma30'], color='m')
            lma20, = ax.plot(date2num(df_h.index), df_h['ma20'], color='k')
            ax.legend([lma50, lma200, lma40, lma30, lma20], ['50 DAY SMA', '200 DAY SMA', '40 DAY SMA', '30 DAY SMA', '20 DAY SMA'], loc="upper left")
        pad = 0.25
        yl = ax.get_ylim()
        ax.set_ylim(yl[0] - (yl[1] - yl[0]) * pad, yl[1])
        ax.grid(True, which='major', axis='both', linestyle='--')
        ax2 = fig.add_subplot(gs[1], sharex=ax)
        ax2.set_position(matplotlib.transforms.Bbox([[0.125, 0.1], [0.9, 0.22]]))
        dates = date2num(df_h.index)
        dates = np.asarray(dates)
        volume = df_h['volume']
        volume = np.asarray(volume)
        pos = df_h['log_ret'] > 0
        neg = df_h['log_ret'] < 0
        ax2.bar(dates[pos], volume[pos], color='green', width=1, align='center')
        ax2.bar(dates[neg], volume[neg], color='red', width=1, align='center')
        vma50, = ax2.plot(date2num(df_h.index), df_h['vol_ma50'], color='b')
        ax2.legend([vma50], ['50 DAY VOLUME SMA'], loc="upper left")
        # scale the x-axis tight
        ax2.set_xlim(min(dates) - 10, max(dates) + 10)
        # the y-ticks for the bar were too dense, keep only every third one
        yticks = ax2.get_yticks()
        # ax2.set_yticks(yticks[::3])
        ax2.ticklabel_format(style='plain')
        ax2.set_ylabel('Volume', size=8, weight='bold')
        # format the x-ticks with a human-readable date.
        xt = ax.get_xticks()
        new_xticks = [datetime.date.isoformat(num2date(d)) for d in xt]
        ax.set_xticklabels(new_xticks, rotation=45, horizontalalignment='right', weight='bold')
        ax.get_xaxis().set_visible(False)
        ax2.set_xticklabels(new_xticks, rotation=45, horizontalalignment='right', weight='bold')
        plt.subplots_adjust(wspace=0, hspace=0)
        fig.set_size_inches((11, 8.5), forward=False)
        fig.savefig('chart_store/chart/' + self.tradingsymbol + '_'+time_frame+'.png',
                    dpi=500, bbox_inches='tight')
        plt.clf()
        plt.cla()
        plt.close()

    def gen_chart_min(self, df_h, time_frame):
        fig = plt.figure()
        title = 'Price-Volume-SMA ' + time_frame + ' chart for ' + self.tradingsymbol + '(' + str(
            datetime.datetime.now().date()) + ')'

        gs = GridSpec(2, 1, height_ratios=[3, 1])
        xx = list(range(len(df_h)))
        xxx = list(range(len(df_h)))[::50]
        xxx.append(xx[-1])
        dd = df_h.index[::50].tolist()
        dd.append(df_h.index[-1])
        candlesticks = zip(xx, df_h['open'], df_h['close'], df_h['high'], df_h['low'],
                           df_h['volume'])
        ax = fig.add_subplot(gs[0])
        ax.set_ylabel('Price', size=7, weight='bold')
        ax.set_title(title, fontsize=10, fontweight='bold')
        candlestick(ax, candlesticks, width=1, colorup='g', colordown='r')
        lma50, = ax.plot(xx, df_h['ma50'], color='b')
        lma200, = ax.plot(xx, df_h['ma200'], color='r')
        ax.legend([lma50, lma200], ['50 PERIOD SMA', '200 PERIOD SMA'], loc="upper left")
        pad = 0.25
        yl = ax.get_ylim()
        ax.set_ylim(yl[0] - (yl[1] - yl[0]) * pad, yl[1])
        ax.grid(True, which='major', axis='both', linestyle='--')
        ax2 = fig.add_subplot(gs[1], sharex=ax)
        ax2.set_position(matplotlib.transforms.Bbox([[0.125, 0.1], [0.9, 0.22]]))
        dates = date2num(df_h.index)
        dates = np.asarray(dates)
        xxxx = np.asarray(xx)
        volume = df_h['volume']
        volume = np.asarray(volume)
        pos = df_h['log_ret'] > 0
        neg = df_h['log_ret'] < 0
        ax2.bar(xxxx[pos],volume[pos], color='green', width=1, align='center')
        ax2.bar(xxxx[neg],volume[neg], color='red', width=1, align='center')
        vma50, = ax2.plot(xx, df_h['vol_ma50'], color='b')
        ax2.legend([vma50], ['50 PERIOD VOLUME SMA'], loc="upper left")
        # scale the x-axis tight
        #ax2.set_xlim(min(dates) - 10, max(dates) + 10)
        # the y-ticks for the bar were too dense, keep only every third one
        yticks = ax2.get_yticks()
        # ax2.set_yticks(yticks[::3])
        ax2.ticklabel_format(style='plain')
        ax2.set_ylabel('Volume', size=8, weight='bold')
        # format the x-ticks with a human-readable date.
        xt = ax.get_xticks()
        ax.set_xticklabels(dd, rotation=45, horizontalalignment='right', weight='bold')

        ax.get_xaxis().set_visible(False)
        ax2.set_xticklabels(dd, rotation=45, horizontalalignment='right', weight='bold')
        plt.subplots_adjust(wspace=0, hspace=0)
        fig.set_size_inches((11, 8.5), forward=False)
        fig.savefig('chart_store/chart/' + self.tradingsymbol + '_' + time_frame + '.png',
                    dpi=500, bbox_inches='tight')
        plt.clf()
        plt.cla()
        plt.close()





