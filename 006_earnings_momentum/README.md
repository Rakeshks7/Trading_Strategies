# Earnings-Momentum: Back test Engine

Welcome to the repo. If you're reading this, you're moving past retail screeners and building systematic, quantifiable edges. 

This repository targets the Post-Earnings Announcement Drift (PEAD). We don't buy the news; we buy the institutional assimilation gap that follows. 

## The Alpha Factor: The Kalman Filter
Standard momentum strategies get chopped to pieces by the volatility crush that happens in the days following an earnings print. To solve this, this repo includes a 1-dimensional Kalman Filter in the `signal_generator.py` module. It acts as an adaptive, zero-lag smoother. It assumes the stock price is a noisy observation of a true hidden state (the institutional accumulation drift). By mathematically filtering out the retail noise, we get a much cleaner trend confirmation before we deploy capital.

## Architecture Highlights
* **Data Engine:** Handles point-in-time fundamental alignment.
* **Alpha:** Calculates Standardized Unexpected Earnings (SUE) and Kalman-smoothed momentum.
* **Risk:** Implements Average True Range (ATR) based position sizing to equalize risk across assets, plus dynamic trailing stops.

* **Execution:** Models the T+2 delayed entry and incorporates a pessimistic slippage model.
