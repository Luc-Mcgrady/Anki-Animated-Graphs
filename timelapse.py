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
        title = "intervals",
        bar_count = MAX_INTERVAL,
        x_scale = 1,
        get_data = lambda day: day.intervals,
        show_burden = False,
        log=print
    ):
    deck = DeckManager(mw.col).get(did)

    days = get_days(did)

    plt.style.use("seaborn")
    fig = Figure()
    axes = fig.add_subplot()
    bars = axes.bar(range(0,bar_count),[0] * bar_count)
    # axes.set_xticklabels([i*x_scale for i in range(bar_count)])

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
        return total / count or 1

    @cache
    def burden(intervals: IdHashedList[int]):
        return sum(a/i for i, a in enumerate(intervals) if i > 0)

    def animate(frame):
        day_index = frame // frames_per_day
        sub_frame = (frame % frames_per_day) / frames_per_day

        day: Day = days[day_index]
        data = get_data(day)
        next_data = get_data(days[day_index+1])

        axes.set_title(f"{deck['name']} {title.title()} {day.date}")
        axes.set_xlim(-0.5, lerp(last_day(data), last_day(next_data), sub_frame) + 0.5)
        axes.set_ylim(0, lerp(memo_max(data), memo_max(next_data), sub_frame))
        axes.set_ylabel(f"Total cards: {sum(data)}") 
        axes.set_xlabel(f"Average {title}: {x_scale*average(data):.2f}, Burden: {burden(data):.2f}cards/day") 

        for bar, day, next_day in zip(bars, data, next_data):
            bar.set_height(lerp(day, next_day, sub_frame))
        
        log(f"{frame=}/{frames}")

    anim = FuncAnimation(fig, animate, frames, interval=1000/(frames_per_day*days_per_second))
    anim.save(f"{title}_{did}.mp4")
    plt.show()

def bar_interval(did, progress):
    bar(did, log=progress) # If you want to change the settings do it here

def bar_ease(did, progress):
    bar(did,
        title="ease", # Config
        shown_percentage=0.99,
        bar_count=MAX_EASE,

        x_scale=10, # Just needed for the bar
        get_data=lambda day: day.real_ease,
        log=progress
    )

def pie(did,
        datums : list[any] = [
            lambda day: day.new,
            lambda day: day.learning,
            lambda day: day.young,
            lambda day: day.mature
        ],
        labels = [f"New: %d", f"Learning: %d",  f"Young: %d",  f"Mature: %d"],
        colours = ["cornflowerblue", "orange", "greenyellow", "green"],
        title = "card types",
        label = "cards",

        days_per_second = 5,
        frames_per_day = 5,
        log=print
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
        values = [lerp(datum(day), datum(next_day), sub_frame) for datum in datums]
        values = [v if v > 0 else 0.1 for v in values] # Make sure no zero errors

        # print(values)
        axes.pie(values, None, 
                [label % datum(day) for label, datum in zip(labels, datums)],
                colours
                )
        axes.set_title(f"{deck['name']} {title.title()}")
        axes.set_xlabel(f"Total {label}: {sum(values):.0f}, {day.date}")

        log(f"{frame=}/{frames}")

    anim = FuncAnimation(fig, animate, frames, interval=1000/(frames_per_day*days_per_second))
    anim.save(f"{title}_{did}.mp4")

def pie_card_types(did, progress):
    pie(did, log=progress)

def pie_ratings(did, progress): # This info is very easy to access in anki but I think 4 graphs look nicer than 3
    pie(did, [
            lambda day: day.ratings[0],
            lambda day: day.ratings[1],
            lambda day: day.ratings[2],
            lambda day: day.ratings[3],
        ], 
        ["Again %d", "Hard %d", "Good %d", "Easy %d"],
        ["red", "orange", "greenyellow", "green"],
        title="ratings",
        label="reviews",
        log=progress
        )