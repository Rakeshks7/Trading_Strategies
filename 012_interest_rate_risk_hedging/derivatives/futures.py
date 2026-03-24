class TreasuryFuture:
    def __init__(self, symbol: str, ctd_price: float, cf: float):
        self.symbol = symbol
        self.ctd_price = ctd_price
        self.cf = cf 

    def calculate_ctd_dv01(self, modified_duration: float, contract_size: float = 100_000) -> float:
        market_value = (self.ctd_price / 100) * contract_size
        bps_shift = 0.0001
        
        return market_value * modified_duration * bps_shift