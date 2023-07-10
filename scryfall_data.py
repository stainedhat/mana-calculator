import re
import json
import time
import requests


class ScryfallAPI:
    def __init__(self):
        self.session = requests.Session()
        self.api_url = "https://api.scryfall.com"

    def get_bulk_data(self):
        url = "https://api.scryfall.com/bulk-data"
        r = self.session.get(url)
        bulk_json = r.json()
        return bulk_json

    def get_cards(self, card_type="default_cards"):
        bulk_data = self.get_bulk_data()
        bulk_data_objects = bulk_data.get("data")
        all_cards_url = None
        for o in bulk_data_objects:
            if o.get("type") == card_type:
                all_cards_url = o.get("download_uri")
        if not all_cards_url:
            raise ValueError("Unable to find all cards url! Cannot download card database")
        all_cards_res = self.session.get(all_cards_url)
        all_cards_json = all_cards_res.json()
        return all_cards_json

    def write_data_to_disk(self, card_data, outfile):
        with open(outfile, "w") as fh:
            json.dump(card_data, fh)

    def load_data_from_disk(self, file_path):
        with open(file_path, "r") as fh:
            data = json.load(fh)
        return data

    def get_paginated_results(self, url, params=None):
        results = []
        res = self.session.get(url, params=params)
        res_json = res.json()
        results.extend(res_json.get("data"))
        if res_json.get("has_more"):
            has_more = True
            while has_more:
                # scryfall docs ask for 100ms between calls so we oblige
                time.sleep(100/1000)
                res = self.session.get(res_json.get("next_page"))
                res_json = res.json()
                results.extend(res_json.get("data"))
                if not res_json.get("has_more"):
                    has_more = False
        return results

    def get_mana_producers(self):
        search = "(produces:w or produces:u or produces:b or produces:r or produces:g or produces:c) format:commander"
        url = f"{self.api_url}/cards/search"
        results = self.get_paginated_results(url, params={"q": search})
        return results

    def mana_parser(self, oracle_text):
        mana_produced = []
        one_mana_symbol_regex = r"Add\s\{([WUBRGC])\}"
        two_mana_symbol_regex = r"Add\s(\{[WUBRGC]\}\{[WUBRGC]\})"
        three_mana_symbol_regex = r"Add\s(\{[WUBRGC]\}\{[WUBRGC]\}\{[WUBRGC]\})"
        four_mana_symbol_regex = r"Add\s(\{[WUBRGC]\}\{[WUBRGC]\}\{[WUBRGC]\}\{[WUBRGC]\})"
        five_mana_symbol_regex = r"Add\s(\{[WUBRGC]\}\{[WUBRGC]\}\{[WUBRGC]\}\{[WUBRGC]\}\{[WUBRGC]\})"
        add_one_mana_regex = r"(Add\sone\smana)"
        add_two_mana_regex = r"(Add\stwo\smana)"
        add_three_mana_regex = r"(Add\sthree\smana)"
        add_four_mana_regex = r"(Add\sfour\smana)"
        add_five_mana_regex = r"(Add\sfive\smana)"
        if re.search(one_mana_symbol_regex, oracle_text) or re.search(add_one_mana_regex, oracle_text):
            mana_produced.append(1)
        if re.search(two_mana_symbol_regex, oracle_text) or re.search(add_two_mana_regex, oracle_text):
            mana_produced.append(2)
        if re.search(three_mana_symbol_regex, oracle_text) or re.search(add_three_mana_regex, oracle_text):
            mana_produced.append(3)
        if re.search(four_mana_symbol_regex, oracle_text) or re.search(add_four_mana_regex, oracle_text):
            mana_produced.append(4)
        if re.search(five_mana_symbol_regex, oracle_text) or re.search(add_five_mana_regex, oracle_text):
            mana_produced.append(5)
        return mana_produced

sf = ScryfallAPI()
# all_cards = sf.get_cards()
# sf.write_data_to_disk(all_cards, "scryfall_data/default_cards.json")
# card_data = sf.load_data_from_disk("scryfall_data/default_cards.json")
mana_producers = sf.get_mana_producers()
for p in mana_producers:
    mana_prod = None
    if p.get("card_faces"):
        for f in p.get("card_faces"):
            o_text = f.get("oracle_text")
            mana_prod = sf.mana_parser(o_text)
    else:
        o_text = p.get("oracle_text")
        mana_prod = sf.mana_parser(o_text)
    if mana_prod:
        p["mana_produced"] = mana_prod
        print(p)
print()