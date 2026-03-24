import math
import logging

class RiskManager:
    def __init__(self, max_margin_capital: float):
        self.max_margin = max_margin_capital

    def apply_slippage_and_limits(self, target_contracts: float, current_position: int, contract_multiplier: float) -> int:
        executable_contracts = math.floor(target_contracts)

        margin_per_contract = 2500.0
        required_margin = executable_contracts * margin_per_contract
        
        if required_margin > self.max_margin:
            logging.warning(f"MARGIN LIMIT BREACH. Required: ${required_margin}, Max: ${self.max_margin}")
            executable_contracts = math.floor(self.max_margin / margin_per_contract)
            logging.warning(f"Clipping execution to {executable_contracts} contracts to preserve cash buffer.")

        contracts_to_trade = executable_contracts - current_position
        
        return contracts_to_trade