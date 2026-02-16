# Dynamic Protective Put (Quant Grade)

Welcome to the lab. This isn't your textbook "buy a stock and a put" script. We are solving for the **Cost of Carry**. The biggest enemy of a protective put is **Theta (Time Decay)**. 

### The Alpha: Kalman Filter Signal
Standard hedges trigger on moving average crossovers. By the time an MA crosses, you've already lost 5% and IV has spiked, making the put expensive. We use a **Kalman Filter** to estimate the "True State" of the stock price. It filters out market noise, allowing us to buy protection *before* the volatility expansion begins.

### How to use:
1. Drop your OHLC data in `data/`.
2. Adjust `risk_appetite` in `run_strategy.py`.
3. Run `python run_strategy.py`.