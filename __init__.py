from aqt.gui_hooks import deck_browser_will_show_options_menu
from aqt import QMenu, mw, QThreadPool, QRunnable, QObject, pyqtSignal
from aqt.utils import tooltip

from typing import Callable

from .timelapse import bar_interval, bar_ease, pie_card_types, pie_ratings
from .anki_install import dependencies

class Worker(QRunnable):
    class Hooks(QObject):
        finished = pyqtSignal()
        progress = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

        self.hooks.progress.connect(self.log)

    def run(self) -> None:
        result = self.func()
        self.hooks.finished.emit(result)

    hooks = Hooks()

    def thread(self, func: Callable):
        self.func = lambda: func(self.hooks.progress.emit)
        QThreadPool().globalInstance().start(_worker)

    @staticmethod
    def log(msg):
        print(msg)
        tooltip(msg)


_worker = Worker()

def action(on_triggered: Callable, label:str):
    def wrapper(menu: QMenu, did):
        action = menu.addAction(label)
        action.triggered.connect(lambda: _worker.thread(lambda progress:on_triggered(did, progress)))
        
    deck_browser_will_show_options_menu.append(wrapper)

action(bar_interval, "Create interval bars")
action(bar_ease, "Create ease bars")
action(pie_card_types, "Create card type pie")
action(pie_ratings, "Create rating pie")

install_action = mw.form.menuTools.addAction("Install Matplotlib")
install_action.triggered.connect(dependencies)