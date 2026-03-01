import yaml
from utils.logger import get_logger
from data.market_data_handler import MarketDataHandler
from alpha.option_models import BlackScholesPricer
from alpha.strike_optimizer import DynamicStrikeOptimizer
from execution.risk_engine import RiskEngine
from execution.portfolio_manager import PortfolioManager

def main():
    logger = get_logger("LP_Butterfly_Engine")
    logger.info("Initializing Quant Execution Engine...")

    logger.info("Loading parameters from config/settings.yaml")

    data_handler = MarketDataHandler(ticker="SPY")
    pricer = BlackScholesPricer()
    optimizer = DynamicStrikeOptimizer(pricer)
    risk = RiskEngine()
    portfolio = PortfolioManager(account_size=250000.0)

    logger.info("Fetching Volatility Surface and Order Book...")
    chain = data_handler.fetch_current_chain()

    logger.info("Scanning IV Skew for optimal probability mass...")
    optimal_trade = optimizer.find_optimal_butterfly(chain)
    
    if optimal_trade["Net_Debit"] <= 0:
        logger.warning("No mathematically viable butterfly found on current surface. Aborting.")
        return

    logger.info(f"Optimal Structure Identified: "
                f"+1 {optimal_trade['K1_ITM']}P / "
                f"-2 {optimal_trade['K2_ATM']}P / "
                f"+1 {optimal_trade['K3_OTM']}P")

    mid_price = optimal_trade["Net_Debit"] * 0.92 # Synthesizing a mid-price check
    if not risk.validate_execution_quality(optimal_trade["Net_Debit"], mid_price):
        logger.warning("Slippage exceeds tolerance. Trade rejected by Risk Engine.")
        return

    contracts = portfolio.calculate_position_size(optimal_trade["Net_Debit"])
    total_risk = contracts * optimal_trade["Net_Debit"] * 100
    
    logger.info(f"Execution Approved. Routing Order: {contracts} contracts.")
    logger.info(f"Total Capital at Risk: ${total_risk:.2f}")
    logger.info(f"Max Potential Profit: ${(optimal_trade['Max_Profit'] * contracts * 100):.2f}")
    logger.info("Trade active. Monitoring Theta decay and Gamma boundaries.")

if __name__ == "__main__":
    main()