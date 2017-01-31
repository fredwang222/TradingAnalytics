This is the readme file for ML4T_Fall_2016_MC3P3

This project has 4 parts.

PART I: CREATE 3 TECHNICAL INDICATORS

momentum.py:
This is a python program to generate the N-day-momentum (default: 10 day).

Run as: python momentum.py  
(modify the code to set gen_plot=True to generate plot)



Bollinger_Band.py:
This is a python program to generate the Bollinger_Band of a stock in a period of time.

Run as: python Bollinger_Band.py  
(modify the code to set gen_plot=True to generate plot)


MACD.py:
This is a python program to generate the moving averge convergence divergence of a stock in a period of time. 
This indicator contains the exponential moving average of 12,26 days so the result will mostly begins in Feburary.

Run as: python MACD.py
(modify the code to set gen_plot=True to generate plot)

###Combine###
indicators.py
This file is the combination of 3 indicators. You don't need to run this file.





PART II: RULE BASED TRADER
rule_based.py
This python file will generate a order file and market simulator will use this order file to show the portfolio value changes.

run as: python rule_based.py
(default setting will plot the portfolio of 2010.01.01-2010.12.31 rule_based IBM/IBM_Benchmark)
(Change time period in function RBtest_code will give you the result you want)




PART III: MACHINE LEARNING BASED TRADER
ML_based.py
This python file will use BagLearner to train data from 2006.01.01-2009.12.31 and based on the model to generate an order file.
Market simulator will use that order file to give portforlio information.

run as: python ML_based.py
(default setting will plot the portfolio of 2010.01.01-2010.12.31 ML_based IBM/IBM_Benchmark)
(Change time period in function MLtest_code will give you the result you want)


PART IV: COMPARATIVE ANALYSIS
compare.py
This file is not required for this project. This python file will plot 3 graphs and the last graph will give a comparison of 
rule_based trader, ML_based trader and IBM_Benchmark. 
run as: python compare.py












