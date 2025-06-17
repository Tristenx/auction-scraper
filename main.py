from auction_content import AuctionContent
from price_check import PriceCheck

auction_content = AuctionContent()
price_check = PriceCheck(auction_content)
print(price_check.bids)
print(price_check.price_after_tax)
price_check.calculate_prices()
print(price_check.prices)
