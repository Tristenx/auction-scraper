from auction_content import AuctionContent
from price_check import PriceCheck

auction_content = AuctionContent()
price_check = PriceCheck(auction_content)
print(price_check.read_price_data())
