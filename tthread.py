from random import randint
from threading import Thread, Event
from time import sleep

class RandomThread:
    def executor(event, dynamic_content, sleep_time):
        while not event.is_set():
            dynamic_content["random"] = randint(0,10000)
            sleep(sleep_time)

    def __init__(self, my_id, sleep_time=0.5):
        self._my_id = my_id
        self._event = Event()
        self._content = {"random":None}
        self._sleep_time = sleep_time

    def start(self):
        self._event.clear()
        self._thread = Thread(
            target=RandomThread.executor,
            args=(
                self._event,
                self._content,
                self._sleep_time
            )
        )
        self._thread.start()

    def stop(self):
        self._event.set()

    def stopjoin(self):
        self.stop()
        self._thread.join()

    def id(self):
        return self._my_id
    

    def get_content(self):
        return self._content['random']

    def is_active(self):
        return not self._event.is_set()

if __name__ == "__main__":
    sleep_time = 0.25
    tthread = RandomThread(0x32a, sleep_time*2)
    tthread.start()
    for i in range(20):
        print(f"{i+1}: tthread has content {tthread.get_content()}")
        sleep(sleep_time)
    tthread.stopjoin()