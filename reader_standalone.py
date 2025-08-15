from serial import Serial
from threading import Lock
import time


class Reader:
    def __init__(self, port: str = "/dev/ttyUSB0"):
        self.com = Serial(port = port, baudrate=38400)
        self.com_lock = Lock()

    def get_answer(self, cmd: str):
        with self.com_lock:
            self.com.write((cmd + '\n').encode('utf-8'))
            reply = self.com.readline().decode('utf-8').strip()
            return reply

    def open(self):
        self.get_answer("reader_open")

    def close(self):
        self.get_answer("reader_close")

    def read(self):
        answer = self.get_answer("reader_read")
        if answer:
            return answer
        else:
            while not self.get_answer("reader_status") == "idle":
                time.sleep(.5)
            return self.get_answer("reader_res")