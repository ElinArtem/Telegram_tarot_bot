import random
import json


def conect_json(file_name):
    with open(file_name) as f:
        return json.loads(f.read())


def create_layout(card_count: int = 1):
    cards = conect_json("cards.json")
    layout_info = []
    text_info = ""
    for i in range(card_count):
        card = random.choice(cards)
        rotation = random.choice(["straight", "inverted"])
        cards.remove(card)
        layout_info.append({**card, "rotation": rotation})
        text_info += f"№{i+1} of card\n\
name: {card['name']}\n\
rotation: {rotation}\n\n"
    return layout_info, text_info

