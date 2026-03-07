\# Short Put Butterfly: Volatility Breakout Engine



This repository implements a systematic Short Put Butterfly strategy. This is a net-credit, multi-leg options strategy designed to capitalize on explosive directional breakouts following periods of severe market consolidation.



\## The Alpha Factor

Standard implementations blindly roll this strategy every 30 days. This engine utilizes a \*\*Volatility Squeeze Detector\*\* (`signals/regime\_filter.py`). We rank historical Bollinger Band Widths to identify the lowest decile of volatility compression. We only deploy capital when the spring is fully coiled.



\## Slippage

The ceiling wing of this trade is a deep ITM short put. In the real world, market makers will gauge you on the bid-ask spread here. Our `portfolio/slippage\_engine.py` dynamically models this transaction cost penalty based on the option's moneyness, ensuring our expected value (EV) calculations reflect reality, not textbook fantasy.

