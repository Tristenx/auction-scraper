class AuctionContent:
    def __init__(self):
        self.text = []
        self.lot_numbers = []
        self.item_descriptions = []
        self.current_bids = []
        self.time_remaining = []
        self.read_content()

    def read_content(self):
        with open(file="search_results.txt", mode="r") as file:
            self.text = file.read()

        lines = self.text.split("\n")
        for i in range(len(lines)):
            words = lines[i].split(" ")
            if words[0] == "Lot":
                self.lot_numbers.append(words[1])
                self.item_descriptions.append(lines[i+1])
                self.current_bids.append(lines[i+4])
                self.time_remaining.append(lines[i+5])
