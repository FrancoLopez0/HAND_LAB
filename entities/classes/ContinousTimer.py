from threading import Timer
import time

class ContinousTimer():
    def __init__(self, interval, function):
        self.timer = None
        self.interval = interval
        self.fun = function

    def run(self):
        self.fun()
        self.timer = Timer(interval=self.interval, function=self.run)
        self.timer.start()


if __name__ == "__main__":
    t = ContinousTimer()
    try:
        t.run(msg="Hello")
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Cancel Timer
        t.timer.cancel()