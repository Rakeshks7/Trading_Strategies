# Quantitative Covered Call Engine (VRP Optimized)

Most people think Covered Calls are free money. They aren't. They are a trade-off where you sell your upside for immediate premium. 

### The Alpha Secret: The Kalman Filter
Standard strategies use Simple Moving Averages. We don't. We use a **Kalman Filter** to estimate the true price of the underlying by filtering out market noise. This helps us avoid selling calls right before a genuine breakout, or holding a dying stock just for the premium.

### Strategy Nuances:
- **Greeks:** We monitor 'Sticky-Delta' assumptions.
- **Risk:** We model slippage based on the bid-ask spread of the OTM calls, which is where most retail traders lose their edge.