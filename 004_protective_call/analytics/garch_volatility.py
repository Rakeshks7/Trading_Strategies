import numpy as np
import pandas as pd
from scipy.optimize import minimize

class GARCHForecaster:
    
    def __init__(self, returns: pd.Series):
        self.returns = returns * 100  
        
    def _garch_likelihood(self, params, returns):
        omega, alpha, beta = params
        n = len(returns)
        sigma2 = np.zeros(n)
        sigma2[0] = np.var(returns)
        
        for t in range(1, n):
            sigma2[t] = omega + alpha * returns[t-1]**2 + beta * sigma2[t-1]
            
        log_likelihood = -0.5 * np.sum(np.log(sigma2) + returns**2 / sigma2)
        return -log_likelihood

    def forecast_volatility(self) -> float:
        cons = ({'type': 'ineq', 'fun': lambda x: 1 - x[1] - x[2]},
                {'type': 'ineq', 'fun': lambda x: x[0]},
                {'type': 'ineq', 'fun': lambda x: x[1]},
                {'type': 'ineq', 'fun': lambda x: x[2]})
        
        initial_guess = [0.01, 0.1, 0.8]
        
        try:
            res = minimize(self._garch_likelihood, initial_guess, args=(self.returns,), 
                          constraints=cons, method='SLSQP')

            omega, alpha, beta = res.x
            last_return = self.returns.iloc[-1]
            last_var = np.var(self.returns) 
            
            next_var = omega + alpha * last_return**2 + beta * last_var
            annualized_vol = np.sqrt(next_var) * np.sqrt(252) / 100
            return annualized_vol
            
        except Exception as e:
            print(f"GARCH Convergence failed: {e}. Defaulting to historical std.")
            return self.returns.std() * np.sqrt(252) / 100