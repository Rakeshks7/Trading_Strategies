# Quantitative Options Strategy: Short Call Butterfly with Kalman Filtering

Welcome to the repository. This architecture is designed for a production-grade algorithmic trading environment, specifically targeting volatility compression anomalies using a Short Call Butterfly structure.

## The Quantitative Edge (The Alpha)
Options pricing data is notoriously noisy. Mid-prices bounce erratically due to bid-ask widening, causing standard algorithms to miscalculate the Expected Move and place strategy wings ($K_1$, $K_3$) sub-optimally. 

This repository implements a **1D Kalman Filter** (`core/vol_surface.py`) to dynamically smooth At-The-Money (ATM) Implied Volatility. By estimating the hidden "true" volatility state, we reduce execution drag and optimize our risk-to-reward ratio upon entry.

## Architecture Highlights
* **`core/black_scholes.py`**: Fully vectorized Greek calculations using NumPy/SciPy for high-throughput analysis.
* **`strategy/risk_manager.py`**: Goes beyond stop-losses. Implements rigorous slippage models, fractional Kelly criterion sizing, and a hard Gamma-cutoff to prevent expiration-week pinning traps.
* **`run_strategy.py`**: The main execution harness. 
