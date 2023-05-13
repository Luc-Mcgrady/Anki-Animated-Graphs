from aqt.gui_hooks import deck_browser_will_show_options_menu
from anki.decks import DeckManager
from array import array
# from anki.exporting import AnkiExporter
from aqt import mw, QMenu

from typing import Callable
from copy import copy

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

    day_seconds = 60 * 60 * 24
    cards = [mw.col.card_stats_data(card) for card in card_ids]
    cards = [card for card in cards if len(card.revlog) > 0 and card.due_date is not None]

    earliest = min(cards, key=lambda a:a.first_review).first_review // day_seconds # Gets the earliest day reviewed on 
    latest = max(cards, key=lambda a:a.latest_review).latest_review // day_seconds # Gets the latest day reviewed on

    empty_day = {}

    days = [empty_day.copy() for _ in range(earliest, latest)] # Create an empty array
    for card in cards:
        # mw.col.get_card(card.id)

        revlog = card.revlog[::-1] # flip it so its goes youngest -> oldest
        last = copy(revlog[0])
        last.time = latest * day_seconds
        ranges = zip(revlog, [*revlog[1:], last])
        
        print()
        for current, next in ranges:
            #print(f"{current.time // day_seconds=}, {next.time // day_seconds=}")
            for i in range(current.time // day_seconds, next.time // day_seconds):
                day = days[i - earliest]
                index = current.interval // day_seconds

                day_current = day.get(index, 0) + 1
                day[index] = day_current

    print(f"{days=}")

action(getDeck, "Create timelapse")