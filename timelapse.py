try:
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    from matplotlib.animation import FuncAnimation
except ImportError:
    from .anki_install import dependencies

    dependencies()

from functools import cache

from anki.decks import DeckManager
from aqt import mw

from .day_data import get_days, Day, IdHashedList, MAX_EASE, MAX_INTERVAL

def lerp(a: int, b: int, t: float):
    return a + (b - a) * t

def bar(
        did,
        days_per_second = 5,
        frames_per_day = 5,
        shown_percentage = 0.95,
        bar_type = "intervals",
        bar_count = MAX_INTERVAL,
        x_scale = 1,
        get_data = lambda day: day.intervals
    ):
    deck = DeckManager(mw.col).get(did)

    days = get_days(did)

    plt.style.use("seaborn")
    fig = Figure()
    axes = fig.add_subplot()
    bars = axes.bar([a*x_scale for a in range(0,bar_count)],[0] * bar_count)

    frames = (len(days) - 1) * frames_per_day
    
    @cache
    def last_day(days: IdHashedList[int]):
        target = sum(days) * shown_percentage
        current = 0
        for i, day in enumerate(days):
            current += day
            if current >= target:
                return i
        assert False # Should not exit this for loop
    
    @cache
    def memo_max(*args, **kwargs):
        return max(*args, **kwargs)

    @cache
    def average(intervals: IdHashedList[int]):
        total = 0
        count = 0
        for i, c in enumerate(intervals):
            count += c
            total += i * c
        return total / count

    @cache
    def burden(intervals: IdHashedList[int]):
        return sum(a/i for i, a in enumerate(intervals) if i > 0)

    def animate(frame):
        day_index = frame // frames_per_day
        sub_frame = (frame % frames_per_day) / frames_per_day

        day: Day = days[day_index]
        data = get_data(day)
        next_data = get_data(days[day_index+1])

        axes.set_title(f"{deck['name']} {bar_type.title()} {day.date}")
        axes.set_xlim(-0.5, lerp(last_day(data), last_day(next_data), sub_frame) + 0.5)
        axes.set_ylim(0, lerp(memo_max(data), memo_max(next_data), sub_frame))
        axes.set_ylabel(f"Total cards: {sum(data)}") 
        axes.set_xlabel(f"Average {bar_type}: {x_scale*average(data):.2f}, Burden: {burden(data):.2f}cards/day") 

        for i, b in enumerate(bars):
            b.set_height(lerp(data[i], next_data[i], sub_frame))
        
        print(f"{frame=}/{frames}")

    anim = FuncAnimation(fig, animate, frames, interval=1000/(frames_per_day*days_per_second))
    anim.save(f"{bar_type}_{did}.mp4")
    plt.show()

def bar_interval(did):
    bar(did) # If you want to change the settings do it here

def bar_ease(did):
    bar(did,
        bar_type="ease",
        shown_percentage=0.99,
        bar_count=MAX_EASE,
        get_data=lambda day: day.real_ease
    )

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
        axes.set_xlabel(f"Total cards: {sum(values):.0f}, {day.date}")

        print(f"{frame=}/{frames}")

    anim = FuncAnimation(fig, animate, frames, interval=1000/(frames_per_day*days_per_second))
    anim.save(f"pie_{did}.mp4")