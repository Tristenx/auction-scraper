from auction_content import AuctionContent
from price_check import PriceCheck

auction_content = AuctionContent()
# auction_content.scrape_data()
auction_content.read_content()
price_check = PriceCheck(auction_content)
# price_check.get_price_data()
price_check.calculate_prices()

print("ITEM | AUCTION_PRICE | RETAIL_PRICE")

for i in range(len(auction_content.item_descriptions)):
    print(
        f"{auction_content.item_descriptions[i]} | {price_check.price_after_tax[i]} | {price_check.prices[i]}")
