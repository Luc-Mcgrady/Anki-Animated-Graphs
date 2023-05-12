from aqt.gui_hooks import deck_browser_will_show_options_menu
# from anki.decks import DeckManager
# from anki.exporting import AnkiExporter
from aqt import mw, QMenu

from typing import Callable

def action(on_triggered: Callable, label:str):
    def wrapper(menu: QMenu, did):
        action = menu.addAction(label)
        action.triggered.connect(lambda:on_triggered(did))
        
    deck_browser_will_show_options_menu.append(wrapper)


def getDeck(did):
    # deck = DeckManager(mw.col).get(did)
    # exporter = AnkiExporter(mw.col)
    # exporter.did = did
    card_ids = mw.col.decks.cids(did, children=True)
    #for card in card_ids:
    card = card_ids[0]
    queue = mw.col.card_stats_data(card).revlog

    print(f"{did=} {queue=}")

action(getDeck, "Create timelapse")