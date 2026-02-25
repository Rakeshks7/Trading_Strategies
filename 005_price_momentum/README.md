# Price Momentum (12-Minus-1) with Kalman Smoothing

Welcome to the repo. If you're here, you already know that momentum works. But you also know that raw momentum is noisy, prone to whipsaws, and susceptible to brutal crashes. 

This repository implements a robust, institutional-grade cross-sectional momentum strategy. 

## The Alpha Factor: Kalman Filtering
We don't just calculate momentum on raw closing prices. We apply a 1D Kalman filter to the price series of every asset in our universe. The Kalman filter recursively estimates the true underlying state of the price by minimizing the mean of the squared error, dynamically adapting to new volatility. 

By calculating our 12-minus-1 return on the *smoothed* Kalman state rather than the noisy raw price, we significantly reduce false positive signals during volatile sideways regimes.

## Core Mechanics
1. **Data:** Ingests EOD adjusted close prices.
2. **Signal:** Calculates $ROC = (P_{t-21} - P_{t-252}) / P_{t-252}$ using Kalman-smoothed prices.
3. **Risk:** Applies an absolute momentum regime filter (SPY 200-SMA) to kill long exposure during structural bear markets.
4. **Sizing:** Allocates capital using Inverse Volatility Parity, ensuring high-beta names don't dominate portfolio variance.

