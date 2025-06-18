from auction_content import AuctionContent
from price_check import PriceCheck

auction_content = AuctionContent()
auction_content.scrape_data()
auction_content.read_content()
price_check = PriceCheck(auction_content)
price_check.get_price_data()
print(price_check.bids)
print(price_check.price_after_tax)
price_check.calculate_prices()
print(price_check.prices)
