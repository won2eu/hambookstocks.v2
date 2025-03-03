class trade_service:
    def update_price(stock):
        alpha = 0.01
        stock.stock_price = stock.stock_price + (stock.trend_buy - stock.trend_sell) * alpha


    def update_sell(stock):
        stock.trend_sell += 1
        stock.total_sell += 1

    def update_buy(stock):
        stock.trend_buy += 1
        stock.total_buy += 1
