import time


class Timer:
    def __init__(self, timer_name: str = "process"):
        self._timer_name = timer_name
        self._start_time = None
        self.run_time = 0

    def __enter__(self):
        self._start_time = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        t = time.time() - self._start_time
        minutes = int(t / 60)
        seconds = t % 60
        print(f"{self._timer_name} completed in {str(minutes) + 'm ' if minutes > 0 else ''}{round(seconds, 3)}s")
