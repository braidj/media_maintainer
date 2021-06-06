import os
import sys
import time
from dataclasses import dataclass, field
from typing import Any, ClassVar
import random


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""

@dataclass
class Timer:
    timers:  ClassVar  = dict()
    name: Any = None
    text: Any = "Elapsed time: {:0.4f} seconds"
    logger: Any = print
    _start_time: Any = field(default=None, init=False, repr=False)

    def __enter__(self):
        """Start a new timer as a context manager"""
        self.start()
        return self

    def __exit__(self, *exc_info):
        """Stop the context manager timer"""
        self.stop()

    def __post_init__(self):
        """Initialization: add timer to dict of timers"""
        if self.name:
            self.timers.setdefault(self.name, 0)

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

        if self.logger:
            self.logger(self.text.format(elapsed_time))
        if self.name:
            self.timers[self.name] += elapsed_time

        return elapsed_time

def mockDecryption(filmName):

    t=Timer(filmName)
    with t:
        time.sleep(random.randint(1,10))


if __name__ == "__main__":

    #pass in a folder
    # work out the name of the film
    # combine and convert into mp4 in one step

    mockVideos = ['dog.ts','cat.ts','monkey.ts',"one day.ts","star wars.ts","something else.ts"]

    for f in mockVideos:
        print(f"Decrypting {f}")
        mockDecryption(f)

    # with t:
    #     time.sleep(0)
         
    # with t:
    #     time.sleep(2)

    #print(t.timers)
    print(Timer.timers)