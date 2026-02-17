#  The Protective Call Protocol

> "Bearish conviction, defined risk."

## Overview
This repository contains a production-grade implementation of the **Protective Call** strategy. It is designed for institutional-grade execution, separating the *Alpha* (Signal) from the *Mechanics* (Hedging) and the *Safety* (Risk Management).

Most GitHub repos just short a stock and buy a random call. This engine is different. It uses **GARCH(1,1) Volatility Forecasting** to ensure we aren't overpaying for the insurance (Call Option). If the implied volatility is too high relative to our forecast, the Risk Manager kills the trade.

## Architecture
* `analytics/`: Where the math happens. Contains a custom GARCH forecaster and a vector-optimized Black-Scholes solver.
* `risk/`: The "No" department. It checks Borrow Rates (Hard-to-Borrow logic) and calculates Kelly Criterion sizing.
* `strategy/`: The orchestrator. It looks for statistical overextension (Z-Score > 2.0) to initiate the short.

## The Alpha Factor
We don't just buy protection blindly.
1.  **Forecast vs. Implied:** We calculate the Fair Value volatility using GARCH.
2.  **Borrow Cost Filter:** If the cost to borrow the stock > 10% annualized, the trade is rejected. The "carry" is too expensive.
3.  **Delta Targeting:** We algorithmically select the option strike that provides exactly 0.30 Delta, optimizing the leverage-to-protection ratio.
