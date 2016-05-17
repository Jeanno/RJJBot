from base_module import BaseModule
import re
import requests
import json
import urllib
from parse import parse

class HearthstoneModule(BaseModule):

  def process_message(self, m):

    text = m.get('text')
    if text is None:
      return None
    text = re.sub(' +', ' ', text).strip() # strip multiple spaces
    try:
      res = parse('/card {}', text)
    except:
      res = None
    if res:
      cardStr = urllib.quote(res[0])
      url = 'https://omgvamp-hearthstone-v1.p.mashape.com/cards/search/' + cardStr + '?collectible=1'
      with open("config/hearthstone_module.json", 'r') as f:
          config = json.load(f)
      headers = {
        'X-Mashape-Key' : config["mashapeKey"],
        'Accept-Charset': 'UTF-8'
      }
      try:
          r = requests.get(url, headers=headers)
          retStr = ''
          ary = r.json()
          for card in ary:
            if card["type"] == "Minion":
                summary = str(card["cost"]) + "/" + \
                        str(card["attack"]) + "/" + str(card["health"])
            elif card["type"] == "Weapon":
                summary = str(card["cost"]) + "/" + \
                        str(card["attack"]) + "/" + str(card["durability"])
            else:
                summary = str(card["cost"])
            text = re.sub('<[^<]+?>', '', card["text"])
            cardStr = card["name"] + " (" + summary + ") - " + text + "\n"
            retStr += cardStr
          return retStr
      except:
          return "Card not found."


    return None

