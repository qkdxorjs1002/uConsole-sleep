import struct
import os
import fcntl
import select
import uinput
import threading
from time import time

from find_power_key import find_power_key
from sleep_display_control import toggle_display


EVENT_DEVICE = find_power_key()
KEY_POWER = 116
HOLD_TRIGGER_SEC = float(os.environ.get("HOLD_TRIGGER_SEC") or 0.7)


def timer_input_power_task(device):
    device.emit(uinput.KEY_POWER, 1)
    device.emit(uinput.KEY_POWER, 0)


with open(EVENT_DEVICE, "rb") as f:
    fcntl.ioctl(f, 0x40044590, 1)

    epoll = select.epoll()
    epoll.register(f.fileno(), select.EPOLLIN)

    uinput_device = uinput.Device([uinput.KEY_POWER])

    try:
        last_key_down_timestamp = 0
        input_power_timer = None

        while True:
            events = epoll.poll()
            current_time = time()
            for fileno, event in events:
                if fileno == f.fileno():
                    event_data = f.read(24)
                    if not event_data:
                        break

                    sec, usec, event_type, code, value = struct.unpack(
                        "qqHHi", event_data
                    )

                    if event_type == 1 and code == KEY_POWER:
                        if value == 1:
                            print(f"SRP: power key down input detected.")
                            last_key_down_timestamp = current_time
                            input_power_timer = threading.Timer(
                                HOLD_TRIGGER_SEC,
                                timer_input_power_task,
                                args=(uinput_device,),
                            )
                            input_power_timer.start()
                        else:
                            print(f"SRP: power key up input detected.")
                            if (
                                input_power_timer != None
                                and (current_time - last_key_down_timestamp)
                                < HOLD_TRIGGER_SEC
                            ):
                                input_power_timer.cancel()
                                toggle_display()

    finally:
        epoll.unregister(f.fileno())
        epoll.close()
