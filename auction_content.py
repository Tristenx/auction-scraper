class AuctionContent:
    def __init__(self):
        self.text = self.get_search_results()
        self.lot_numbers = []
        self.item_descriptions = []
        self.current_bids = []
        self.time_remaining = []
        self.read_content()

    def get_search_results(self):
        with open(file="search_results.txt", mode="r") as file:
            content = file.read()
        return content

    def read_content(self):
        lines = self.text.split("\n")
        for i in range(len(lines)):
            words = lines[i].split(" ")
            if words[0] == "Lot":
                self.lot_numbers.append(words[1])
                self.item_descriptions.append(lines[i+1])
                self.current_bids.append(lines[i+4])
                self.time_remaining.append(lines[i+5])
