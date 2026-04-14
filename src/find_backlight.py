import os


def find_backlight():
    return "/sys/class/backlight/backlight@0"


if __name__ == "__main__":
    print(find_backlight())
