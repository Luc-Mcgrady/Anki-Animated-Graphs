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

    day_seconds = 60 * 60 * 24
    revlogs = [mw.col.card_stats_data(card).revlog for card in card_ids]
    revlogs = [revlog for revlog in revlogs if len(revlog) > 0]

    earliest = min(revlogs, key=lambda a:a[-1].time if len(a) > 0 else 2e50)[-1].time // day_seconds # Gets the earliest day reviewed on 
    latest = max(revlogs, key=lambda a:a[0].time if len(a) > 0 else -1)[0].time // day_seconds # Gets the latest day reviewed on

    empty_day = [0, 0, 0, 0]

    days = [empty_day] * (latest - earliest) # Create an empty array
    for revlog in revlogs:
        review = -1 # 1 indexed because we're working backwards

        day = revlog[review].time // day_seconds
        print(revlog)

        while day < latest - 1:

            while revlog[review-1].time // day_seconds <= day:
                #print(f"{review=}, {revlog[review].time // day_seconds=}, {day=}")
                review -= 1
            
            current = revlog[review].review_kind
            next_time = revlog[review-1].time // day_seconds if review > -len(revlog) + 2 else latest - 1
            print(f"{current=} {next_time=} {review=}>{-len(revlog)=}")

            while day < next_time:
                #print(f"{day - earliest=} {len(days)=} {next_time - earliest=}")
                days[day - earliest][current] += 1
                day += 1



    print(f"{days=}")

action(getDeck, "Create timelapse")