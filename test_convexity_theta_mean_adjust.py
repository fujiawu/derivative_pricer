
import numpy as np
import matplotlib.pyplot as plt

def pay_off_straddle(s, k):
    return np.abs(s-k)
    #return np.max([s-k, 0])
    #return np.max([k-s, 0])
vpay_off_straddle = np.vectorize(pay_off_straddle)

def straddle_pricer(S, K, TimeToMaturity, DailyVol, N = 100000):
    S_scenarios = np.random.lognormal(np.log(S), DailyVol * np.sqrt(TimeToMaturity), N)
    payoffs = vpay_off_straddle(S_scenarios, K)
    return np.average(payoffs)
vstraddle_pricer = np.vectorize(straddle_pricer)


S0 = 100
K = 100
TimeToMaturity = 4
DailyStd = 0.1

BasePrice = straddle_pricer(S0, K, TimeToMaturity, DailyStd)

Spots = np.random.lognormal(np.log(S0), DailyStd, 100)
Prices = vstraddle_pricer(Spots, K, TimeToMaturity, DailyStd) - BasePrice

SpotsForFit = np.random.lognormal(np.log(S0), 0.01, 100)
PricesForFit = vstraddle_pricer(SpotsForFit, K, TimeToMaturity, DailyStd) - BasePrice

linefit = np.polyfit(SpotsForFit, PricesForFit, 2)

Spotsfit = np.arange(np.min(Spots), np.max(Spots))
Pricesfit = Spotsfit * linefit[1] + np.square(Spotsfit) * linefit[0] + linefit[2]

Convexity = 2*linefit[0]
Mean = np.average(Prices)
ConvexityEffect = 0.5 * Convexity * S0 * S0 * DailyStd * DailyStd

BasePriceTomorrow = straddle_pricer(S0, K, TimeToMaturity-1, DailyStd)
Theta = BasePriceTomorrow - BasePrice

print "Convexity:", Convexity
print "ConvexityEffect:", ConvexityEffect
print "Mean:", Mean
print "Theta:", Theta

plt.plot(Spots, Prices, 'ro')
plt.plot(SpotsForFit, PricesForFit, 'bo')
plt.plot(Spotsfit, Pricesfit, 'b-')
plt.show()

