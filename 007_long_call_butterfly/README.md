# The Long Call Butterfly

## The Objective
This repository implements a systematic, market-neutral options strategy designed to harvest the Volatility Risk Premium (VRP). It executes a 1-2-1 Long Call Butterfly structure, optimizing for localized mean-reversion in Implied Volatility (IV).

## The "Alpha" Factor: Kalman-Filtered IV
Market makers frequently spoof options order books, causing momentary, artificial spikes in Implied Volatility Rank (IVR). Retail traders often execute mean-reversion strategies on these false signals. 

This engine utilizes a **1D Kalman Filter** to dynamically estimate the *true* underlying volatility state. By stripping out the microstructural noise, the strategy only deploys capital when the structural volatility premium is genuinely inflated, drastically improving the win rate and capital efficiency.

## Architecture Highlights
* **Vectorized Pricing:** Custom Black-Scholes-Merton engine utilizing `numpy` for high-throughput Greek calculations.
* **Algorithmic Strike Selection:** Strikes are dynamically placed at the $\pm 1\sigma$ Expected Move boundaries, rather than relying on arbitrary delta targets.
* **Microstructure Risk Management:** Built-in execution guards to prevent fills during high-slippage environments (e.g., the first 15 minutes of the session).