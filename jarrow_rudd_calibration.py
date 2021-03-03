# -*- coding: utf-8 -*-
"""Jarrow-Rudd_calibration

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uwPmuoQGYPzqiyfbtNAt1SWrfJjEZJdx
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csc_matrix
from scipy.stats import bernoulli
from math import exp, sqrt

# %matplotlib inline

def call_price(S0, K, sigma, div, r, N, T): 
  t = (T/12)/(N-1)
  u = exp((r-div-((sigma**2)/2))*t + sigma*sqrt(t)) 
  d = exp((r-div-((sigma**2)/2))*t - sigma*sqrt(t)) 
  p = (exp((r-div)*t)-d)/(u-d)

  stock_prices = csc_matrix((N,N))
  call_prices = csc_matrix((N,N))

  stock_prices[0,0] = S0

  for i in range(1,N):
    M = i + 1 
    stock_prices[i,0] = d*stock_prices[i-1,0]
    for j in range(1,M):
      stock_prices[i,j] = u*stock_prices[i-1,j-1]

  payoff = stock_prices[-1,].toarray() - K 
  payoff.shape = (payoff.size,)
  payoff = np.where(payoff >= 0, payoff, 0)


  call_prices[-1,:] = payoff
  for i in range(N-2, -1, -1 ):
    for j in range(i+1):
      call_prices[i,j] = exp(-r*t)*((1-p)*call_prices[i+1,j] + p*call_prices[i+1,j+1])

  print('call price at strike ',K,' = ',call_prices[0,0])

  return call_prices[0,0]

def put_price(S0, K, sigma, div, r, N):
  put = call_price(S0, K, sigma, div, r, N, T) - S0*exp(-div) + K*exp(-r)
  return print('put price at strike ',K,' = ',put)

S0 = 179
K= 200
sigma = 0.26
div = 0 # yield 
r = 0.015
N = 40 # number of steps plus 1  == size of matrix 
T = 3 # Time until maturity in months

call_price(S0, K, sigma, div, r, N, T)
put_price(S0, K, sigma, div, r, N)

