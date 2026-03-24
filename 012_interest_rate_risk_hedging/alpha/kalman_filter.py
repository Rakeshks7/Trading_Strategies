class DynamicBasisFilter:
    def __init__(self, process_variance: float, measurement_variance: float):
        self.Q = process_variance
        self.R = measurement_variance

        self.x_hat = 0.0 
        self.P = 1.0     

    def update(self, measurement: float) -> float:
        x_hat_minus = self.x_hat
        P_minus = self.P + self.Q

        K = P_minus / (P_minus + self.R)

        self.x_hat = x_hat_minus + K * (measurement - x_hat_minus)

        self.P = (1 - K) * P_minus
        
        
        
        return self.x_hat