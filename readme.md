# Anki Animated Graphs

[Video](http://www.youtube.com/watch?v=WDyhZYgIQk8)

[![Anki Animated Graphs](http://img.youtube.com/vi/WDyhZYgIQk8/0.jpg)](http://www.youtube.com/watch?v=WDyhZYgIQk8 "Anki Animated Graphs")

**Edited together in Kdenlive*

# Usage

1. Download the addon and put it in your addons folder
2. Select the deck you want to generate a graph for and select one of the 4 new options.
3. Download matplotlib if prompted. (I didn't test the install code and especially didn't test it on mac so if it doesn't work)


## Options

### <ins>Create Interval Bars</ins>
Create a time-lapse of your intervals over time  
![intervals_1663035216169-f001169](https://github.com/Luc-mcgrady/anki-animated-graphs/assets/63685643/06ef7e63-a4e0-40c8-a9c3-9974b465c31b)


*Full disclosure, for some reason the intervals at the end and the intervals in the anki stats are different. The reason for this I don't know but the graph looks pretty regardless*

### <ins>Create Ease Bars</ins>

Bar animated chart but this time for your ease.
![ease_1663035216169-f000407](https://github.com/Luc-mcgrady/anki-animated-graphs/assets/63685643/72b719b9-08fc-42d9-b501-def2202f98b1)

#### Known Issues
- For some reason matplotlib made changing the numbers on the bottom of the bar difficult, so the ease is actually 10* what it says it is)
- I opted to make it so that "ease" was actually $\frac{current review}{next review}$ to support custom schedulers)
- (Due after a card does its last review it dissapears from the graph. This is probably fixable but I tried and it was annoying 😐)
- I left the burden stat on which is totally unrelated to the thing that is graphed. Its good to know I guess.

### <ins>Create Card Type Pie</ins>
This is the animated version of your card types (young, mature etc). 
![card types_1663035216169-f000545](https://github.com/Luc-mcgrady/anki-animated-graphs/assets/63685643/242ce547-c42d-4633-b811-ba629f1cd102)

*This wont be perfect because the new cards come in when they are created not when they are moved into your deck. Also learning cards are just counted as cards with an interval less than 1. Theres probably a way to fix that but it shouldn't make too big a difference.*

### <ins>Create Rating Pie</ins>
![ratings_1663035216169-f000001](https://github.com/Luc-mcgrady/anki-animated-graphs/assets/63685643/bf6ab39d-e521-4e8c-9083-7364227bd0b0)

This option creates an animated pie chart of all the ratings you gave to reviews on every day you rated them.

# Matplotlib install

For all of these your going to need python installed with pip. All the automatic install does is run these commands so its probably more reliable than doing this manually. Only read this if the automatic install has failed.

## Linux
Just install matplotlib  
```sh
$ pip install matplotlib
```  

If this doesn't work then my only guess is your pip is probably for a different python than the one anki uses. so try find the one python uses and run that ones pip.  

## Windows

In windows it wont count if you install matplotlib in your python site-packages like if you did the linux way. Anki has its own python runtime and its own packages. Conveniently these packages are in the lib folder

```bat
pip install --target=".../anki/lib" matplotlib
```

Where .../anki = your anki install location.

## Mac

Probably the same as windows, otherwise good luck.
