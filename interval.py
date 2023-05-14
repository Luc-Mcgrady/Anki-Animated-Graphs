import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

from copy import copy
from functools import cache

from anki.decks import DeckManager
from aqt import mw

class IdHashedList(list):
    def __hash__(self) -> int:
        return id(self)

class Day:
    new: int
    intervals: IdHashedList[int]

    def __init__(self):
        self.intervals = IdHashedList([0] * 500)
        self.new = 0

    @property
    def learning(self):
        return self.intervals[0]
    
    @property
    def young(self):
        return sum(self.intervals[1:21])

    @property
    def mature(self):
        return sum(self.intervals[21:])
    
    def __iter__(self):
        return self.intervals

def get_days(did):
    card_ids = mw.col.decks.cids(did, children=True)
    #for card in card_ids:

    day_seconds = 60 * 60 * 24
    cards = [mw.col.card_stats_data(card) for card in card_ids]
    cards = [card for card in cards if len(card.revlog) > 0 and card.due_date != 0]

    earliest = min(cards, key=lambda a:a.first_review).first_review // day_seconds # Gets the earliest day reviewed on 
    latest = max(cards, key=lambda a:a.latest_review).latest_review // day_seconds # Gets the latest day reviewed on

    days = [Day() for _ in range(earliest, latest)] # Create an empty array
    for card in cards:
        # mw.col.get_card(card.id)

        revlog = card.revlog[::-1] # flip it so its goes youngest -> oldest
        last = copy(revlog[0])
        last.time = latest * day_seconds
        ranges = zip(revlog, [*revlog[1:], last])

        added = card.added // day_seconds
        added = added if added > earliest else earliest 
        
        for i in range(added, revlog[0].time // day_seconds):
            print(f"{i} - {earliest} = {i-earliest}")
            day = days[i - earliest]
            day.new += 1

        #print()
        for current, next in ranges:
            #print(f"{current.time // day_seconds=}, {next.time // day_seconds=}")
            for i in range(current.time // day_seconds, next.time // day_seconds):
                day = days[i - earliest]
                index = current.interval // day_seconds

                #day_current = day.get(index, 0) + 1
                day.intervals[index] += 1
    
    return days

def interval_timelapse(
        did,
        days_per_second = 5,
        frames_per_day = 5,
        shown_percentage = 0.95,
    ):
    deck = DeckManager(mw.col).get(did)

    days = get_days(did)

    plt.style.use("seaborn")
    fig = Figure()
    axes = fig.add_subplot()
    axes.set_title(f"{deck['name']} Intervals")
    bars = axes.bar(range(0,500),[0] * 500)

    frames = (len(days) - 1) * frames_per_day

    def lerp(a: int, b: int, t: float):
        return a + (b - a) * t
    
    @cache
    def last_day(day: IdHashedList[int]):
        filled_days = [i for i, a in enumerate(day) if a != 0]
        return filled_days[int(len(filled_days)*shown_percentage)]
    
    @cache
    def memo_max(*args, **kwargs):
        return max(*args, **kwargs)

    @cache
    def mean(intervals: IdHashedList[int]):
        total = 0
        count = 0
        for i, c in enumerate(intervals):
            count += c
            total += i * c
        return total / count

    def animate(frame):
        day_index = frame // frames_per_day
        sub_frame = (frame % frames_per_day) / frames_per_day

        intervals: IdHashedList[int] = days[day_index].intervals
        next_intervals = days[day_index+1].intervals

        axes.set_xlim(0, lerp(last_day(intervals), last_day(next_intervals), sub_frame))
        axes.set_ylim(0, lerp(memo_max(intervals), memo_max(next_intervals), sub_frame))
        axes.set_ylabel(f"Total cards: {sum(intervals)}") 
        axes.set_xlabel(f"Average interval: {mean(intervals):.2f} Days") 

        for i, b in enumerate(bars):
            b.set_height(lerp(intervals[i], next_intervals[i], sub_frame))
        
        print(f"{frame=}/{frames}")

    anim = FuncAnimation(fig, animate, frames, interval=1000/(frames_per_day*days_per_second))
    anim.save(f"{did}.mp4")
    plt.show()