import os


def find_framebuffer():
    return "/sys/class/graphics/fb0"


if __name__ == "__main__":
    print(find_framebuffer())
