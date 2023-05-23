from aqt import mw
from copy import copy
from datetime import datetime

class IdHashedList(list):
    def __hash__(self) -> int:
        return id(self)

MAX_INTERVAL = 500
MAX_EASE = 30

class Day:
    new: int
    intervals: IdHashedList[int]
    real_ease: IdHashedList[int]
    ratings: IdHashedList[int]

    timestamp: int

    def __init__(self, timestamp):
        self.intervals = IdHashedList([0] * MAX_INTERVAL)
        self.real_ease = IdHashedList([0] * MAX_EASE)
        self.ratings = IdHashedList([0, 0, 0, 0])

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
    excluded = mw.col.find_cards(f"is:suspended")

    card_ids = mw.col.decks.cids(did, children=True)
    card_ids = [id for id in card_ids if id not in excluded]

    day_seconds = 60 * 60 * 24
    cards = [mw.col.card_stats_data(card) for card in card_ids]

    earliest = min([card for card in cards if card.first_review != 0], key=lambda a:a.first_review).first_review // day_seconds # Gets the earliest day reviewed on 
    latest = max(cards, key=lambda a:a.latest_review).latest_review // day_seconds # Gets the latest day reviewed on
    latest += 1 # I dont know why we need this

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
            last = copy(revlog[-1])
            last.time = latest * day_seconds

            ranges = zip(revlog, [*revlog[1:], last])

            #print()
            for current, next in ranges:
                #print(f"{current.time // day_seconds=}, {next.time // day_seconds=}")
                for i in range(current.time // day_seconds, next.time // day_seconds):
                    day = days[i - earliest]
                    # For some reason this interval doesn't match up with the stats at the end but it doesn't seem to be a bug
                    interval = current.interval // day_seconds
                    day.intervals[interval] += 1

                    if current.interval > 0 and next is not last:
                        real_ease_index = (10 * next.interval) // current.interval # As a 10*%
                        # print(f"{real_ease_index=} {current.interval=} {next.interval=} {current.button_chosen}")

                        if 1 < real_ease_index < MAX_EASE:
                            day.real_ease[real_ease_index] += 1
            
            for review in revlog:
                days[(review.time // day_seconds) - earliest].ratings[review.button_chosen - 1] += 1
        
    return days