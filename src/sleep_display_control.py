import os
import uinput
from find_drm_panel import find_drm_panel
from find_framebuffer import find_framebuffer
from find_backlight import find_backlight


DISABLE_POWER_OFF_DRM = os.environ.get("DISABLE_POWER_OFF_DRM") == "yes"

drm_panel_path = find_drm_panel()
framebuffer_path = find_framebuffer()
backlight_path = find_backlight()

if not drm_panel_path:
    raise Exception("there's no matched drm panel")

if not framebuffer_path:
    raise Exception("there's no matched framebuffer")

if not backlight_path:
    raise Exception("there's no matched backlight")

uinput_path = "/dev/uinput"
if not os.path.exists(uinput_path):
    raise FileNotFoundError(f"{file_path} File not found.")

uinput_device = uinput.Device([uinput.KEY_SLEEP, uinput.KEY_WAKEUP])

status_path = os.path.join(backlight_path, "bl_power")


def toggle_display():
    global drm_panel_path
    global framebuffer_path
    global backlight_path
    global uinput_device
    global status_path

    try:
        with open(status_path, "r") as f:
            screen_state = f.read().strip()

        if screen_state == "4":
            # on
            with open(os.path.join(framebuffer_path, "blank"), "w") as f:
                f.write("0")
            with open(os.path.join(backlight_path, "bl_power"), "w") as f:
                f.write("0")
            if not DISABLE_POWER_OFF_DRM:
                with open(os.path.join(drm_panel_path, "status"), "w") as f:
                    f.write("detect")
            uinput_device.emit_click(uinput.KEY_WAKEUP)
        else:
            # off
            if not DISABLE_POWER_OFF_DRM:
                with open(os.path.join(drm_panel_path, "status"), "w") as f:
                    f.write("off")
            with open(os.path.join(framebuffer_path, "blank"), "w") as f:
                f.write("1")
            with open(os.path.join(backlight_path, "bl_power"), "w") as f:
                f.write("4")

        print(f"panel status: {screen_state} to {'0' if screen_state == '4' else '4'}")

    except Exception as e:
        print(f"error occured: {e}")


if __name__ == "__main__":
    toggle_display()
