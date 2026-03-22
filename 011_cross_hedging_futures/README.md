# Dynamic Cross-Hedging via Kalman Filtering

Welcome to the repo. If you're here, you already know that textbook hedging doesn't work in the real world. Assets don't move in perfect 1:1 lockstep. 

This repository implements a professional-grade cross-hedging framework. Instead of relying on static, backward-looking correlation windows, we use a Kalman Filter to dynamically estimate the Optimal Hedge Ratio (OHR). 



## The Math (The "Why")
Traditional OHR is calculated as:
$$OHR = \rho \left( \frac{\sigma_S}{\sigma_F} \right)$$

We model this relationship dynamically. Let $y_t$ be the spot asset returns and $x_t$ be the proxy futures returns. We assume a hidden state $\beta_t$ (our hedge ratio):
Observation equation: $$y_t = \beta_t x_t + v_t$$
State equation: $$\beta_t = \beta_{t-1} + w_t$$

The filter updates our belief about $\beta$ (the hedge ratio) at every time step, balancing our previous estimate against new market noise. 

## Risk Management
You aren't trading price here; you are trading the *basis* (the spread between the spot and the beta-adjusted futures). This repo includes a `risk_manager` that tracks the rolling Z-score of this basis. If the Z-score blows out beyond our threshold (a "black swan" decoupling), it cuts the futures leg to prevent infinite liability.