from aqt.gui_hooks import deck_browser_will_show_options_menu
from anki.decks import DeckManager
from array import array
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

    day = 60 * 60 * 24
    revlogs = [mw.col.card_stats_data(card).revlog for card in card_ids]
    earliest = min(revlogs, key=lambda a:a[-1].time if len(a) > 0 else 2e50)[-1].time // day # Gets the earliest day reviewed on 
    latest = max(revlogs, key=lambda a:a[0].time if len(a) > 0 else -1)[0].time // day # Gets the latest day reviewed on

    print(f"{earliest=} {latest=}")

action(getDeck, "Create timelapse")