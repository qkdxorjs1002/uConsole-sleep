import os
import inotify.adapters
import inotify.constants

# from find_drm_panel import find_drm_panel
from find_backlight import find_backlight
from find_internal_kb import find_internal_kb

SAVING_CPU_FREQ = os.environ.get("SAVING_CPU_FREQ")
DISABLE_POWER_OFF_KB = os.environ.get("DISABLE_POWER_OFF_KB") == "yes"
DISABLE_CPU_MIN_FREQ = os.environ.get("DISABLE_CPU_MIN_FREQ") == "yes"


def control_by_state(state):
    global kb_device_path
    global kb_device_id
    global usb_driver_path
    global cpu_policy_path

    if state:
        if not DISABLE_CPU_MIN_FREQ:
            with open(os.path.join(cpu_policy_path, "scaling_max_freq"), "w") as f:
                f.write(default_cpu_freq_max)
            print(f"cpu freq max: {default_cpu_freq_max}")
            with open(os.path.join(cpu_policy_path, "scaling_min_freq"), "w") as f:
                f.write(default_cpu_freq_min)
            print(f"cpu freq min: {default_cpu_freq_min}")
        if not DISABLE_POWER_OFF_KB:
            with open(os.path.join(usb_driver_path, "bind"), "w") as f:
                f.write(kb_device_id)
            print("kb power state: bind")
        with open(os.path.join(kb_device_path, "power/control"), "w") as f:
            f.write("on")
    else:
        with open(os.path.join(kb_device_path, "power/control"), "w") as f:
            f.write("auto")
        if not DISABLE_POWER_OFF_KB:
            with open(os.path.join(usb_driver_path, "unbind"), "w") as f:
                f.write(kb_device_id)
            print("kb power state: unbind")
        if not DISABLE_CPU_MIN_FREQ:
            with open(os.path.join(cpu_policy_path, "scaling_min_freq"), "w") as f:
                f.write(saving_cpu_freq_min)
            print(f"cpu freq min: {saving_cpu_freq_min}")
            with open(os.path.join(cpu_policy_path, "scaling_max_freq"), "w") as f:
                f.write(saving_cpu_freq_max)
            print(f"cpu freq max: {saving_cpu_freq_max}")


backlight_path = find_backlight()
# drm_panel_path = find_drm_panel()
kb_device_path = find_internal_kb()
kb_device_id = os.path.basename(kb_device_path)
usb_driver_path = "/sys/bus/usb/drivers/usb"
cpu_policy_path = "/sys/devices/system/cpu/cpufreq/policy0"

if not backlight_path:
    raise Exception("there's no matched backlight")

# if not drm_panel_path:
#    raise Exception("there's no matched drm panel")

if not kb_device_path:
    raise Exception("there's no matched kb")

with open(os.path.join(kb_device_path, "power/autosuspend_delay_ms"), "w") as f:
    f.write("0")
    print(f"{kb_device_path}/power/autosuspend_delay_ms = 0")

if not SAVING_CPU_FREQ:
    with open(os.path.join(cpu_policy_path, "cpuinfo_min_freq"), "r") as f:
        saving_cpu_freq_min = f.read().strip()
        saving_cpu_freq_max = saving_cpu_freq_min
else:
    saving_cpu_freq_min, saving_cpu_freq_max = SAVING_CPU_FREQ.split(",")
    saving_cpu_freq_min = f"{saving_cpu_freq_min}000"
    saving_cpu_freq_max = f"{saving_cpu_freq_max}000"
print(f"saving_cpu_freq_min: {saving_cpu_freq_min}")
print(f"saving_cpu_freq_max: {saving_cpu_freq_max}")

with open(os.path.join(cpu_policy_path, "scaling_min_freq"), "r") as f:
    default_cpu_freq_min = f.read().strip()
    print(f"default_cpu_freq_min: {default_cpu_freq_min}")

with open(os.path.join(cpu_policy_path, "scaling_max_freq"), "r") as f:
    default_cpu_freq_max = f.read().strip()
    print(f"default_cpu_freq_max: {default_cpu_freq_max}")

backlight_bl_path = os.path.join(backlight_path, "bl_power")
with open(backlight_bl_path, "r") as f:
    screen_state = f.read().strip()

# drm_enabled_path = os.path.join(drm_panel_path, "enabled")
# with open(drm_enabled_path, "r") as f:
#    screen_state = f.read().strip()

try:
    control_by_state(screen_state != "4")
#    control_by_state(screen_state != "disabled")
except Exception as e:
    print(f"Error occurred: {e}, on init. ignored")

i = inotify.adapters.Inotify()
i.add_watch(backlight_bl_path, mask=inotify.constants.IN_MODIFY)

print(f"Monitoring {backlight_bl_path} for changes...")

last_screen_state = ""
while True:
    try:
        list(i.event_gen(yield_nones=False, timeout_s=1))

        with open(backlight_bl_path, "r") as f:
            screen_state = f.read().strip()

        if screen_state == last_screen_state:
            continue
        last_screen_state = screen_state

        control_by_state(screen_state != "4")

    except Exception as e:
        print(f"Error occurred: {e}")
