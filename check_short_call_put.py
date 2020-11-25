import yahoo_fin.options as ops
import yahoo_fin.stock_info as si 

import pandas
#expiration_dates = ops.get_expiration_dates("aapl")
#print(expiration_dates)
#index(['Contract Name', 'Last Trade Date', 'Strike', 'Last Price', 'Bid',
#       'Ask', 'Change', '% Change', 'Volume', 'Open Interest',
#       'Implied Volatility'],
#      dtype='object')

#stocks =  ["sq", "amd", "dis", "v"]
stocks = ["aapl", "nflx", "nvda", "tsla", "sq", "intc", "arkk", "tsm", "v"]
for s in stocks:
    period = 2
    p = si.get_live_price(s)
    print ("Stock %s, price = %.2f"%(s,p))
    expire_dates = ops.get_expiration_dates(s)
    for date in expire_dates:
        
        period -= 1
        if period < 0:
            break
        premium = int (p/100) + 0.5 
        
        options = ops.get_options_chain(s, date)
        start = p*1.05
        end = p*1.3
        print ("Checking Call option for %s premium %f for range %0.1f - %0.1f"%(date, premium, start,end ))
        
        calls = options["calls"]
        selected = calls.loc[(calls['Last Price']> premium ) & (calls['Strike']> start) & (calls['Strike']< end)  ]
        for ind in selected.index:
            print( " Strike: %s %s Last: %s Volume: %s OI: %s " %
            (selected['Strike'][ind], selected['Contract Name'][ind], selected['Last Price'][ind],
            selected['Volume'][ind], selected['Open Interest'][ind]) )
        start = p*0.7
        end = p*0.95
        print ("Checking Put option for %s premium %f for range %0.1f - %0.1f"%(date, premium, start,end ))
        
        puts = options["puts"]
        selected = puts.loc[(puts['Last Price']> premium) & (puts['Strike']> start)  & (puts['Strike']< end)  ]
        for ind in selected.index:
            print( " Strike: %s %s Last: %s Volume: %s OI: %s " %
            (selected['Strike'][ind], selected['Contract Name'][ind], selected['Last Price'][ind],
            selected['Volume'][ind], selected['Open Interest'][ind]) )
        
#chain = pandas.read_csv(file_name)
#print(chain.columns)
#['Strike'], d['Last Price']