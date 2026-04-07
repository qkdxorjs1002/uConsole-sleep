import os


def find_power_key():
    EVENT_PATH = "/dev/input/by-path"

    for evt in os.listdir(EVENT_PATH):
        pwr_evt_path = os.path.join(EVENT_PATH, evt)

        if "axp221-pek" in evt:
            return pwr_evt_path

    return ""


if __name__ == "__main__":
    print(find_power_key())
