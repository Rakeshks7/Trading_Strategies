# Long Put Butterfly: 


Welcome to the quant desk. This isn't your standard retail options script. This repository is designed to execute the Long Put Butterfly dynamically, adapting to the volatility surface rather than relying on static strike widths.

## The Alpha: Volatility Skew Arbitrage via KDE
Retail traders pick a target price, go $5 up and $5 down, and send the order. We don't do that here. 

Our `strike_optimizer.py` uses Kernel Density Estimation (KDE) to map the historical probability mass of the underlying asset. It then cross-references this probability distribution with the current Implied Volatility (IV) skew. The engine algorithmically selects the short ATM strikes where the Volatility Risk Premium (VRP) is highest, and buys the outer wings where the IV is structurally underpriced relative to our KDE model. 

We are buying cheap insurance and selling expensive stagnation.

## Risk Management
The `risk_engine.py` models slippage dynamically based on the width of the bid-ask spread across four legs, ensuring we don't enter a mathematically sound trade that bleeds out in execution friction. It also enforces strict Portfolio Gamma limits.
