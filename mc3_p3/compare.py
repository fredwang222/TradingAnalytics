import numpy as np
import datetime as dt
from util import get_data, plot_data
import math
import csv
import marketsim as mk
import dateutil
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import Bollinger_Band as bb
import momentum as mt
import MACD as macd
import BagLearner as bag
import rule_based as rb
import ML_based as ml

RULEBASED = rb.RBtest_code(sd = dt.datetime(2010,1,1), ed = dt.datetime(2010,12,31))
ML_BASED = ml.MLtest_code(sd=dt.datetime(2010,1,1), ed = dt.datetime(2010,12,31))
#RULEBASED.set_index(['Date'])
#ML_BASED.set_index(['Date'])
df = pd.concat([RULEBASED,ML_BASED['ML_Based']],axis=1)
df.plot(fontsize=12,color=['black','blue','green'])
plt.show()
