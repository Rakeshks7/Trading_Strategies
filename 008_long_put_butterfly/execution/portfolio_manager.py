class PortfolioManager:
    def __init__(self, account_size: float = 100000.0):
        self.account_size = account_size

    def calculate_position_size(self, net_debit: float, win_prob: float = 0.40) -> int:
        b = 2.5 
        p = win_prob
        q = 1 - p
        
        kelly_pct = (b * p - q) / b
        adj_kelly = max(0.0, kelly_pct / 2.0)

        max_alloc = 0.02
        trade_alloc_pct = min(adj_kelly, max_alloc)
        
        capital_to_deploy = self.account_size * trade_alloc_pct

        contracts = int(capital_to_deploy / (net_debit * 100))
        return max(1, contracts) # Always at least 1 if signal fires