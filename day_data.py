from aqt import mw
from copy import copy
from datetime import datetime

class IdHashedList(list):
    def __hash__(self) -> int:
        return id(self)

class Day:
    new: int
    intervals: IdHashedList[int]
    timestamp: int

    def __init__(self, timestamp):
        self.intervals = IdHashedList([0] * 500)
        self.new = 0
        self.timestamp = timestamp

    @property
    def learning(self):
        return self.intervals[0]
    
    @property
    def young(self):
        return sum(self.intervals[1:21])

    @property
    def mature(self):
        return sum(self.intervals[21:])
    
    @property
    def date(self):
        return datetime.fromtimestamp(self.timestamp).date()

    def __iter__(self):
        return self.intervals

def get_days(did):
    card_ids = mw.col.decks.cids(did, children=True)
    #for card in card_ids:

    day_seconds = 60 * 60 * 24
    cards = [mw.col.card_stats_data(card) for card in card_ids]
    cards = [card for card in cards]

    earliest = min([card for card in cards if card.first_review != 0], key=lambda a:a.first_review).first_review // day_seconds # Gets the earliest day reviewed on 
    latest = max(cards, key=lambda a:a.latest_review).latest_review // day_seconds # Gets the latest day reviewed on

    days = [Day(i * day_seconds) for i in range(earliest, latest)] # Create an empty array
    for card in cards:
        # mw.col.get_card(card.id)

        added = card.added // day_seconds
        added = added if added > earliest else earliest 

        first_reviewed = card.first_review // day_seconds if card.first_review != 0 else latest

        for i in range(added, first_reviewed):
            day = days[i - earliest]
            day.new += 1

        revlog = card.revlog[::-1] # flip it so its goes youngest -> oldest
        if len(revlog) > 0:
            last = copy(revlog[0])
            last.time = latest * day_seconds
            ranges = zip(revlog, [*revlog[1:], last])

            #print()
            for current, next in ranges:
                #print(f"{current.time // day_seconds=}, {next.time // day_seconds=}")
                for i in range(current.time // day_seconds, next.time // day_seconds):
                    day = days[i - earliest]
                    index = current.interval // day_seconds

                    #day_current = day.get(index, 0) + 1
                    day.intervals[index] += 1
    
    return days