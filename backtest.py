''' ONE DAY BITCOIN 1M CHART'''

''' STEP 1: Initialize / Define '''

import pandas as pd
import numpy as np
from itertools import islice

filename = 'BTCUSDT-1m-2022-07-11.csv' #plug in like 10 CSVs
dataSet = pd.read_csv(filename,usecols=[0,1,2])

dataSet = pd.DataFrame(dataSet)
data = dataSet.values.tolist()

#print(data)

period = 240  #pre-determined buy window
capital = 1440  #total capital
allowance = 240  #amount spent per buy
current_allowance = 0  #how much can be spent currently
haveBought= False  #have we bought during this period?

assets = []  #total assets held at end

def __init__(self, assets, period, capital, allowance, current_allowance, haveBought):
    self.period = period
    self.capital = capital
    self.allowance = allowance
    self.current_allowance = current_allowance
    self.assets = assets
    self.haveBought = haveBought

def window(seq, n=period):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = list(islice(it, n))
    arr = []
    if len(result) == n:
        arr.append(result)
    for elem in it:
        result = result[1:] + [elem]
        arr.append(result)
    return arr
        
def buy(currentAllowance, price):
    "Buys at the price in the price dataset for currentAllowance"
    amt = currentAllowance/price
    assets.append(amt)
    print('\nWe bought', amt, 'for', currentAllowance, 'at ', price)
    
SMA = []  #running list of previous Simple Moving Averages

def calculateSMA(prices):
    "Calculates a running list of Simple Moving Averages in the prices list"
    print('\nthe prices are: ',prices)
    a = []
    a = window(prices, period)
    
    for i in range(len(a)):
        tmp = sum(a[i])/period
        SMA.append(tmp)
        
        
''' STEP 2: Calculate SMA '''

#print(data[:])  # can't do multi-dimensional slicing of lists 

i = 0
priceArr= []

# pass array of only the 2nd items

for i in range(len(data)):
    priceArr.append(data[i][2])
    
# print(priceArr)    

calculateSMA(priceArr)
print('\nThe simple moving average is: ', SMA)


'''STEP 3: Create the control group'''

control = []  #standard DCA control group
i = 0

for i in range(len(data)):
    for j in range(len(data[i])):
        if i%period == 0 and j == 2:
            tmp= allowance/data[i][j]
            control.append(tmp)
            print('we bought ', tmp, 'for ', allowance, 'at ', data[i][j])

control = np.sum(control)
print('\nThe amount of BTC bought via standard DCA was: ', control)

''' STEP 4: Calculate Sigma '''

sigma = []  #array of previous standard deviations

def calculateSigma(prices):
    ''' the formula is std = sqrt(mean(abs(x - x.mean())**2)) but there's a numpy function so I will do that '''
    x = []
    x = window(prices, period)
    
    #Need to convert to single dimensional
    
    for i in range(len(x)):
        tmp = np.std(x[i])
        sigma.append(tmp)

calculateSigma(priceArr)

print('\nThe standard deviation, sigma, is: ',sigma)

''' STEP 5: Buy Logic '''
print('\nLength of Data: ', len(data))
print('\nLength of SMA: ', len(SMA))
print('\nLength of Sigma: ', len(sigma))

for i in range(len(sigma)):
    for j in range(len(data[i])):
        if i%period == 0 and j == 2 and capital > 0:
            haveBought = False
            if (SMA[i]- 2*sigma[i]) > data[i+period][j] and current_allowance > 0 and haveBought is False:
                buy(current_allowance, data[i+period][j])
                capital -= current_allowance
                current_allowance = 0
                haveBought = True
                print('The remaining balance is: ', capital)
                if capital == 0:
                    break
            elif (SMA[i]- sigma[i]) > data[i+period][j] and current_allowance > 0 and haveBought is False:
                buy(current_allowance, data[i+period][j])
                capital -= current_allowance
                current_allowance = 0
                haveBought = True
                print('The remaining balance is: ', capital)
                if capital == 0: 
                    break
            else:
                if current_allowance < capital:
                    current_allowance += allowance
                    haveBought = False
                    print('The current allowance is: ', current_allowance)
                else:
                    print('the current allowance is: ', current_allowance)
        elif i%period !=0 and j==2 and capital > 0:
            if (SMA[i]- 2*sigma[i]) > data[i+period][j] and current_allowance > 0 and haveBought is False:                
                buy(current_allowance, data[i+period][j])
                capital -= current_allowance
                current_allowance = 0
                haveBought = True
                print('The remaining balance is: ', capital)
                if capital == 0: 
                    break
            elif (SMA[i]- sigma[i]) > data[i+period][j] and current_allowance > 0 and haveBought is False:
                buy(current_allowance, data[i+period][j])
                capital -= current_allowance
                current_allowance = 0
                haveBought = True
                print('The remaining balance is: ', capital)
                if capital == 0:
                    break
            else:
                if current_allowance < capital:
                    current_allowance += allowance
                    haveBought = False
                    print('The current allowance is: ', current_allowance)
                else:
                    print('the current allowance is: ', current_allowance)
        else: 
            if capital > 0 or capital - current_allowance < 0:
                continue
            else:
                break


    
print('\nOur assets are: ', assets)
print('\nthe number of purchases made was: ', len(assets))

outcome = sum(assets)

print('The amount of assets purchased with strategy is: ',outcome) 
print('The amount of assets purchased via traditional strategy is: ',control)
print('Did our strategy work? ', outcome > control)
