# Quantitative Covered Put Engine (Short-Squeeze Optimized)

Welcome. Most retail traders stay away from Covered Puts because shorting stock is "scary." In this repo, we embrace the short side by treating it with the same mathematical rigor as a long-bias fund.

### The "Alpha" Secret: The Hurst Exponent
We don't just sell puts because we are short. We use the **Hurst Exponent ($H$)** to determine the "regime" of the stock. 
- If $H < 0.5$, the stock is mean-reverting. We sell puts closer to the money to capture high theta.
- If $H > 0.5$, the stock is trending. We sell puts further OTM to avoid getting run over by a downward move that exceeds our put protection.

### Strategy Nuances:
- **Borrow Costs:** Unlike calls, shorting stock costs money (HTB - Hard to Borrow). Our engine factors in the rebate rate.
- **Skew:** We specifically target the 'Put Wing' where volatility is usually highest.