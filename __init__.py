from aqt.gui_hooks import deck_browser_will_show_options_menu
from aqt import QMenu

from typing import Callable

from .timelapse import interval_bar, type_pie

def action(on_triggered: Callable, label:str):
    def wrapper(menu: QMenu, did):
        action = menu.addAction(label)
        action.triggered.connect(lambda:on_triggered(did))
        
    deck_browser_will_show_options_menu.append(wrapper)

action(interval_bar, "Create timelapse")
action(type_pie, "Create pie")