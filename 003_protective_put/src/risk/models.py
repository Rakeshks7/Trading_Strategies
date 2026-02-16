class RiskManager:
    @staticmethod
    def apply_slippage(price: float, vol: float, is_buy: bool = True) -> float:
        impact = price * (vol * 0.05) 
        return price + impact if is_buy else price - impact