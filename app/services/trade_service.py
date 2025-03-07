class trade_service:
    def update_price(stock):
        alpha = 0.01
        new_price = stock.stock_price + (stock.trend_buy - stock.trend_sell) * alpha
        # 새로운 가격으로 업데이트하기

    def update_sell(stock):
        stock.trend_sell += 1
        stock.total_sell += 1

    def update_buy(stock):
        stock.trend_buy += 1
        stock.total_buy += 1
