import datetime

class ExecutionGuard:
    def __init__(self):
        self.safe_start_time = datetime.time(9, 45)
        self.safe_end_time = datetime.time(15, 45)
        
    def check_liquidity_conditions(self, time_of_day: str, bid_ask_spread: float, max_allowable_spread: float = 0.10) -> bool:
        try:
            h, m = map(int, time_of_day.split(':'))
            current_time = datetime.time(h, m)
        except ValueError:
            return False

        if not (self.safe_start_time <= current_time <= self.safe_end_time):
            return False

        if bid_ask_spread > max_allowable_spread:
            return False
            
        return True