from auction_content import AuctionContent
from price_check import PriceCheck
import pandas as pd

auction_content = AuctionContent()
auction_content.scrape_data()
auction_content.read_content()
price_check = PriceCheck(auction_content)
price_check.get_price_data()
price_check.calculate_prices()

auction_dict = {
    "ITEM": auction_content.item_descriptions,
    "AUCTION_PRICE": price_check.price_after_tax,
    "RETAIL_PRICE": price_check.prices,
    "TIME_REMAINING": auction_content.time_remaining
}

auction_csv = pd.DataFrame(auction_dict)

recommendations = []
print("ITEM | AUCTION_PRICE | RETAIL_PRICE")
for i in range(len(auction_content.item_descriptions)):
    if price_check.prices[i] != "NO DATA" and float(price_check.price_after_tax[i]) < float(price_check.prices[i]):
        print(
            f"{auction_content.item_descriptions[i]} | {price_check.price_after_tax[i]} | {price_check.prices[i]}")
        recommendations.append("YES")
    else:
        recommendations.append("NO")

auction_csv["RECOMMENDATION"] = recommendations
auction_csv.to_csv("auction_csv.csv")
