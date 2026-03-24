# Interest Rate Risk Hedging - Futures (Institutional Grade)

Welcome to the repo. If you're reading this, you already know that hedging fixed-income portfolios isn't about perfectly predicting the market; it's about structural risk transfer and surviving liquidity shocks.

This repository implements a dynamic duration hedge using Treasury Futures. 

## The Core Mechanics
We are neutralizing our cash portfolio's sensitivity to interest rates by taking an offsetting short position in Treasury futures. The baseline mathematics rely on matching the Dollar Value of a 1 Basis Point move (DV01). 

The raw hedge ratio is defined as:
$$N = \frac{DV01_{Portfolio}}{DV01_{CTD}} \times CF$$

Where $CF$ is the exchange-assigned Conversion Factor for the Cheapest-to-Deliver (CTD) bond.



## Kalman Filter Basis Tracking
The raw hedge ratio assumes perfect correlation between your portfolio and the CTD bond. In reality, the basis (the spread between the two) is incredibly noisy. If you rebalance your hedge on every 1-tick move, transaction costs will bleed your portfolio dry.

We use a 1-Dimensional Kalman Filter to track the 'true' hidden state of the yield spread. It recursively updates our belief about the basis risk, filtering out high-frequency noise. We only execute adjustment trades when the *filtered* state deviates from our threshold, saving massive execution costs while maintaining a tight risk profile.

