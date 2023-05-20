from aqt.gui_hooks import deck_browser_will_show_options_menu
from aqt import QMenu, mw

from typing import Callable

from .timelapse import bar_interval, bar_ease, type_pie
from .anki_install import dependencies

def action(on_triggered: Callable, label:str):
    def wrapper(menu: QMenu, did):
        action = menu.addAction(label)
        action.triggered.connect(lambda:on_triggered(did))
        
    deck_browser_will_show_options_menu.append(wrapper)

action(bar_interval, "Create interval bars")
action(bar_ease, "Create ease bars")
action(type_pie, "Create pie")

install_action = mw.form.menuTools.addAction("Install Matplotlib")
install_action.triggered.connect(dependencies)