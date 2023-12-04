import yahoo_fin.options as ops
import yahoo_fin.stock_info as si
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
import matplotlib.pyplot as plt
from collections import defaultdict

import matplotlib.dates as mdates

# expiration_dates = ops.get_expiration_dates("aapl")
# print(expiration_dates)
# stocks =  ["msft"]

class Strategy:
    def __init__(self):
        pass

class DynamicStrategy(Strategy):
    def __init__(self, name, put_margin, call_margin, hold):
        self.stock = 0.0
        self.option = 0.0
        self.position = 0
        self.sp = None
        self.sc = None
        self.hold = hold
        self.assigned = []
        self.name = "Dynamic " + name + " Put " + str(put_margin) + "%" + " Call " + str(call_margin) + "% (min hold " + str(
            hold) + ")"
        self.num = 0
        self.numSP = 0
        self.numSC = 0
        self.put_margin = put_margin
        self.call_margin = call_margin
        self.maxPostion = 0
        self.max = None
        self.min = None
        self.positionList = []
        self.valueList = []
        self.scList = defaultdict(list)

    def Check(self, row):
        close = row["close"]
        open = row["open"]

        if self.sp is not None:
            if self.sp > close:
                # print(self.name, "assingment buy", self.assigned, self.sp, close)
                self.assigned.append(round(self.sp, 2))
                self.position += 100
                self.stock -= 100 * self.sp
                # print ("Buy %f with %f"%(self.sp, close) )
        if self.scList :

            sold =[]
            #print (type(self.scList))
            total = 0
            for k, v in self.scList.items():
                total = total + len(v)
                if k < close:
                    for i in v:
                        self.assigned.remove(i)
                        self.position -= 100
                        self.stock += 100 * k
                        sold.append(i)
            if (len(sold) > 1  ):
                print(self.name, sold, close, self.scList.items())

        self.sc = None
        self.scList.clear()
        if len(self.assigned) > self.hold:
            j = [i for i in self.assigned if ( i < close)] if self.hold == 0 else [i for i in self.assigned if ( min(self.assigned) < i < close)]
            l = 0
            for i in j:
                self.numSC += 1
                self.scList[ close * (1 + (self.call_margin + l ) / 100) ].append(i)
                l = l + 1

            #if len(self.scList) > 0:
                #print(self.name, "sell", self.assigned, j, close, self.scList)

        if len(self.assigned) > self.maxPostion:
            self.maxPostion = len(self.assigned)

        self.sp = close * (1 - (self.put_margin if len(self.assigned) > 0 else self.put_margin-2) / 100)
        self.numSP += 1
        if self.max is None or self.max < row["high"]:
            self.max = row["high"]

        if self.min is None or self.min > row["low"]:
            self.min = row["low"]

        # self.balance += round(100 * 1/ (1+len(self.assigned)),2)
        # print ("%s open %.2f close %0.2f position %d balance %0.2f "%(date, open, close,  self.position, self.stock + close *self.position))
        # print (self.assigned, max(self.assigned) if len(self.assigned) > 0 else 0 )

        self.positionList.append(self.position)
        self.valueList.append((self.stock + row["close"] * self.position))


class HoldNStrategy(Strategy):
    def __init__(self, name, put_margin, call_margin, hold):
        self.stock = 0.0
        self.option = 0.0
        self.position = 0
        self.sp = None
        self.sc = None
        self.hold = hold
        self.assigned = []
        self.name = name + " Put " + str(put_margin) + "%" + " Call " + str(call_margin) + "% (min hold " + str(
            hold) + ")"
        self.num = 0
        self.numSP = 0
        self.numSC = 0
        self.put_margin = put_margin
        self.call_margin = call_margin
        self.maxPostion = 0
        self.max = None
        self.min = None
        self.positionList = []
        self.valueList = []
        self.scList = []

    def Check(self, row):
        close = row["close"]
        open = row["open"]

        if self.sp is not None:
            if self.sp > close:
                # print(self.name, "assingment buy", self.assigned, self.sp, close)
                self.assigned.append(round(self.sp, 2))
                self.position += 100
                self.stock -= 100 * self.sp
                # print ("Buy %f with %f"%(self.sp, close) )
        if self.sc is not None:

            if self.sc < close:
                #print(self.name, "assignment sell", self.assigned, self.scList, close)
                for i in self.scList:
                    self.assigned.remove(i)
                    self.position -= 100
                    self.stock += 100 * self.sc

                # print("Sold %f with %f" % (self.sc, close))

        self.sc = None
        self.scList = []
        if len(self.assigned) > self.hold:
            j = [i for i in self.assigned if ( i < close)] if self.hold == 0 else [i for i in self.assigned if ( min(self.assigned) < i < close)]
            if len(j) > 0:
                #print(self.name, "sell", self.assigned, j, close)
                self.sc = close * (1 + self.call_margin / 100)
                self.numSC += len(j)
                self.scList = j

        if len(self.assigned) > self.maxPostion:
            self.maxPostion = len(self.assigned)

        self.sp = close * (1 - (self.put_margin if len(self.assigned) > 0 else self.put_margin-2) / 100)
        self.numSP += 1
        if self.max is None or self.max < row["high"]:
            self.max = row["high"]

        if self.min is None or self.min > row["low"]:
            self.min = row["low"]

        # self.balance += round(100 * 1/ (1+len(self.assigned)),2)
        # print ("%s open %.2f close %0.2f position %d balance %0.2f "%(date, open, close,  self.position, self.stock + close *self.position))
        # print (self.assigned, max(self.assigned) if len(self.assigned) > 0 else 0 )

        self.positionList.append(self.position)
        self.valueList.append((self.stock + row["close"] * self.position))


# actions = ["call", "put"]
stocks = {"aapl": 3, "nflx": 1, "nvda": 1, "fb": 1, "msft": 2, "spy": 1, "low": 2}
#stocks =  {"sq" : 1}

# stocks =  {"nflx" : 1}
ranges = {
    "2019-2020": {
        "start_date": "1/1/2019",
        "end_date": "31/12/2020",
        "first_monday": "7/1/2019",
        "first_friday": "31/12/2019"}
}

for year, r in ranges.items():
    for k, v in stocks.items():
        print(k, r["start_date"], r["end_date"])
        p = si.get_live_price(k)
        data = si.get_data(k, r["start_date"])

        strategy = []
        strategy.append(HoldNStrategy(k, 5, 5, 1))
        strategy.append(HoldNStrategy(k, 5, 5, 0))
        strategy.append(HoldNStrategy(k, 5, 7, 1))
        #strategy.append(DynamicStrategy(k, 5, 5, 1))
        #strategy.append(DynamicStrategy(k, 5, 5, 0))
        #strategy.append(DynamicStrategy(k, 5, 7, 1))
        monday = dt.strptime(r["first_monday"], "%d/%m/%Y")
        friday = dt.strptime(r["first_friday"], "%d/%m/%Y")
        end = dt.strptime(r["end_date"], "%d/%m/%Y")

        dateList = []
        closeList = []

        while monday < end:
            range = data.loc[monday: friday]
            # print (range)
            row = {"date": monday.strftime("%d/%m/%Y"), "high": round(range["high"].max(), 2),
                   "open": round(range.iloc[0]["open"], 2), "close": round(range.iloc[-1]["close"], 2),
                   "low": round(range["low"].min(), 2)}
            # print ( "Up" if (open  < close) else "Down" )
            # upper = high - open
            # body =  close - open
            # lower = close - low

            # print ("%s-%s, %.2f,%.2f, %.2f, %.2f"%(start.strftime("%d/%m/%Y"), end.strftime("%d/%m/%Y"), high, open, close, low))
            for s in strategy:
                s.Check(row)

            dateList.append(row["date"])
            closeList.append(row["close"])
            monday += timedelta(7)
            friday += timedelta(7)

            # df = pd.DataFrame({'Date' : s.date,                   'Close': s.close})

        fig, ax1 = plt.subplots()
        # Define the date format
        ax1.plot(dateList, closeList, label='close')

        ax1.set_xlabel('Date')
        ax1.set_ylabel('Price')

        ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        #ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))


        ax2 = ax1.twinx()
        for s in strategy:

            print(
                "   %s Position: %d Return (%.2f vs %.2f) , [sc %d sp %d], [max %d curr %d], best [min %.2f max %.2f]" %
                (s.name, s.position, (row["close"] * s.position) + s.stock, (s.max - s.min) * 100, s.numSC,
                 s.numSP, s.maxPostion, len(s.assigned), s.min, s.max))
            print("   ", s.assigned)

            ax2.xaxis.set_major_locator(mdates.DayLocator(interval=5))
            #ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
            ax2.plot(dateList, s.positionList, label=s.name + ' position')
            ax2.plot(dateList, s.valueList, label=s.name + ' value')
        plt.legend(loc="upper left")

        plt.title(k + " " + r["start_date"] + " - " + r["end_date"])
        fig.autofmt_xdate()

        #plt.xticks(rotation=90)
        plt.show()
