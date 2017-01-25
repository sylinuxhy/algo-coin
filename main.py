import sys
from custom_strategies import SMACrossesStrategy
from config import TradingEngineConfig, BacktestConfig
from enums import TradingType
from trading import TradingEngine
from log import LOG as log


def parse_command_line(argv: list):
    # Every engine run requires a static config object
    config = TradingEngineConfig()
    if 'live' in argv:
        # WARNING: Live trading. money will be lost ;^)
        log.critical("WARNING: Live trading. money will be lost ;^)")
        config.type = TradingType.LIVE
        config.exchange_options.trading_type = TradingType.LIVE
    elif 'sandbox' in argv:
        # Trade against sandbox
        log.info("Sandbox trading")
        config.type = TradingType.SANDBOX
        config.exchange_options.trading_type = TradingType.SANDBOX
    elif 'backtest' in argv:
        # Backtest against trade data
        log.info("Backtesting")
        config.type = TradingType.BACKTEST
        config.backtest_options = BacktestConfig()

        # TODO specify exchange data as input
        config.backtest_options.file = "./data/exchange/krakenUSD.csv"
        config.exchange_options.trading_type = TradingType.BACKTEST

    if 'verbose' in argv:
        # Print/log extra info
        config.verbose = True

    return config


def main(argv: list):
    config = parse_command_line(argv)
    # Instantiate trading engine
    #
    # The engine is responsible for managing the different components,
    # including the strategies, the bank/risk engine, and the
    # exchange/backtest engine.
    te = TradingEngine(config)

    # A sample strategy that impelements the correct interface
    ts = SMACrossesStrategy(10, 5)

    # Register the strategy with the Trading engine
    te.registerStrategy(ts)

    # Run the live trading engine
    te.run()

if __name__ == '__main__':
    main(sys.argv)
