import yahoo_fin.options as ops
import yahoo_fin.stock_info as si 
import sys
import pandas
import argparse
#expiration_dates = ops.get_expiration_dates("aapl")
#print(expiration_dates)
#index(['Contract Name', 'Last Trade Date', 'Strike', 'Last Price', 'Bid',
#       'Ask', 'Change', '% Change', 'Volume', 'Open Interest',
#       'Implied Volatility'],
#      dtype='object')

#stocks =  ["sq", "amd", "dis", "v"]
#ARK 
premium_stock2 = {"ARKK": 1,
"ARKW": 1,
"PSTG": 1,
 "BIGC": 1,
 "fsly": 1,
 "tdoc": 1,
 "se": 1,
 "rkt": 0.2,
 "work": 0.2,
"ROKU":1 
}
premium_stock1 = {"BABA": 1,
"hd": 1,
"low":0.5
}
premium_stock = {"aapl": 0.5, 
    "amd" : 0.3, 
    "dis" : 0.5, 
    "docu": 1.0, 
    "fsly": 1, 
    "intc":0.2,
    "low":1,
    "msft" : 0.5, 
    "nflx": 1, 
    "nvda": 1, 
    "rkt": 0.5,
    "roku": 1,
    "sq": 1.0,
    "tdoc": 1.0,
    "tlt": 1,
    "tsla": 1.0,
    "tsm" : 0.5,
    "WORK" :0.2,
    "v" : 0.5}
def check():
    
    for stock, premium in premium_stock.items() :
        period = 3
        price = si.get_live_price(stock)
        
        print ("Stock %s, price = %.2f, premium= %.2f "%(stock, price, premium))
        
        
        
        expire_dates = ops.get_expiration_dates(stock)
        for date in expire_dates:
            
            period -= 1
            if period < 0:
                break
            
            options = ops.get_options_chain(stock, date)
            start = price*1.05
            print ("Checking Call option for %s premium %f for range from %0.1f"%(date, premium, start ))
            
            calls = options["calls"]
            selected = calls.loc[(calls['Last Price']> premium ) & (calls['Strike']> start) & (calls['Strike']< start * 1.5)]
            for ind in selected.index:
                print( " Strike: %s %s Last: %s Bid: %s Ask: %s Volume: %s OI: %s " %
                (selected['Strike'][ind], selected['Contract Name'][ind], selected['Last Price'][ind],
                selected['Bid'][ind], selected['Ask'][ind], selected['Volume'][ind], selected['Open Interest'][ind]) )
            
            start = price*0.95
            
            print ("Checking Put option for %s premium %f for range from %0.1f "%(date, premium, start ))
            
            puts = options["puts"]
            selected = puts.loc[(puts['Last Price']> premium) &  (puts['Strike']< start)  &  (puts['Strike']> start * .5) ]
            for ind in selected.index:
                print( " Strike: %s %s Last: %s Bid: %s Ask: %s Volume: %s OI: %s " %
                (selected['Strike'][ind], selected['Contract Name'][ind], selected['Last Price'][ind],
                selected['Bid'][ind], selected['Ask'][ind], selected['Volume'][ind], selected['Open Interest'][ind]) )
            

#stock = input("stock:  ")
#premium = float(input("Expected premium:   "))
check()

#parser = argparse.ArgumentParser(description='Process some integers.')
#parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                    help='an integer for the accumulator')
#parser.add_argument('-t', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')

#args = parser.parse_args()
#print args.accumulate(args.integers)