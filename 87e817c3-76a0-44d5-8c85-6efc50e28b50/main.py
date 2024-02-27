from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the assets that the strategy will involve
        self.tickers = ["AAPL", "MSFT"]

    @property
    def assets(self):
        # Return the list of tickers the strategy involves
        return self.tickers

    @property
    def interval(self):
        # The data interval for backtesting and live trading, e.g., "1day" for daily data
        return "1day"

    def run(self, data):
        # Execute the strategy and return target allocations for each asset
        allocation_dict = {}
        
        # Calculate a simple Moving Average Convergence Divergence (MACD)
        # signal for each asset and make trading decisions based on this indicator
        for ticker in self.tickers:
            macd_data = MACD(ticker, data["ohlcv"], fast=12, slow=26)
            macd_line = macd_data.get("MACD")
            signal_line = macd_data.get("signal")
            
            # Check if MACD crosses above the signal line indicating a buying signal
            if macd_line and signal_line and macd_line[-1] > signal_line[-1] and macd_line[-2] < signal_line[-2]:
                allocation_dict[ticker] = 0.5 # Allocate 50% to this asset
            else:
                allocation_dict[ticker] = 0 # Do not allocate to this asset
        
        # Ensure the strategy does not allocate more than 100% in total by normalizing if necessary
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 1:
            allocation_dict = {ticker: weight / total_allocation for ticker, weight in allocation_dict.items()}
        
        return TargetAllocation(allocation_dict)