import yahoo_fin.options as ops
import yahoo_fin.stock_info as si 
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
#expiration_dates = ops.get_expiration_dates("aapl")
#print(expiration_dates)
#stocks =  ["msft"]

class Stragegy:
    def __init__(self):
        self.balance = 0.0
        self.position = 0
        self.sp = None
        self.sc = None
        self.assigned =[]

    def Check(self, date, open, close):
        if self.sp != None:
            if  self.sp > close: 
                self.assigned.append( self.sp)
                
        for a in self.assigned:
            if close > a:
                self.assigned.remove(a)
        if close - open > 0:
            self.sp = close -1 - len(self.assigned)
            self.balance += round(100 * 1/ (1+len(self.assigned)),2)
        else:
            self.sp = None
        print (date, open, close, self.balance, self.assigned)
        

actions = ["call", "put"]
stocks =  ["qqq"]
#stocks =  ["sq", "amd", "dis", "v"]
for s in stocks:
    print (s)
    p = si.get_live_price(s)
    data = si.get_data(s, start_date ="1/1/2020")
    today = dt.strptime("26/7/2020", "%d/%m/%Y")
    start = dt.strptime("6/1/2020", "%d/%m/%Y")
    end = dt.strptime("10/1/2020", "%d/%m/%Y")
    prev_close = None
    sp = None
    assigned = 0
    s =  Stragegy()
    while start < today :
        range = data.loc[start : end]
        #print (range)
        high = round(range["high"].max(), 2)
        open = round(range.iloc[0]["open"], 2)
        close = round(range.iloc[-1]["close"], 2)
        low = round(range["low"].min(), 2 )
        #print ( "Up" if (open  < close) else "Down" )
        upper = high - open
        body =  close - open 
        lower = close - low
        
        #print ("%s-%s, %.2f,%.2f, %.2f, %.2f"%(start.strftime("%d/%m/%Y"), end.strftime("%d/%m/%Y"), high, open, close, low))
        
        s.Check(start.strftime("%d/%m/%Y"), open,close)
        start += timedelta(7)
        end += timedelta(7)
        
        
