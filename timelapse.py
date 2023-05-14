import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

from functools import cache

from anki.decks import DeckManager
from aqt import mw

from .day_data import get_days, Day, IdHashedList

def lerp(a: int, b: int, t: float):
    return a + (b - a) * t

def interval_bar(
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
    anim.save(f"bar_{did}.mp4")
    plt.show()

def type_pie(did,
            days_per_second = 5,
            frames_per_day = 5,
            ):
    deck = DeckManager(mw.col).get(did)
    days = get_days(did)
    frames = (len(days) - 1) * frames_per_day

    fig = Figure()
    axes = fig.add_subplot()

    # day.new, day.learning, day.young, day.mature
    def animate(frame):
        day_index = frame // frames_per_day
        sub_frame = (frame % frames_per_day) / frames_per_day

        day: Day = days[day_index]
        next_day = days[day_index + 1]
        
        axes.clear()
        values = [
            lerp(day.new, next_day.new, sub_frame), 
            lerp(day.learning, next_day.learning, sub_frame),
            lerp(day.young, next_day.young, sub_frame),
            lerp(day.mature, next_day.mature, sub_frame)
        ]
        # print(values)
        axes.pie(values, None, 
                [f"New: {day.new}"  , f"Learning: {day.learning}",  f"Young: {day.young}",  f"Mature: {day.mature}"], 
                ["cornflowerblue"   , "orange",                     "greenyellow",          "green"]
                )
        axes.set_title(f"{deck['name']}")
        axes.set_xlabel(f"Total cards: {sum(day.intervals)}")

        print(f"{frame=}/{frames}")

    anim = FuncAnimation(fig, animate, frames, interval=1000/(frames_per_day*days_per_second))
    anim.save(f"pie_{did}.mp4")