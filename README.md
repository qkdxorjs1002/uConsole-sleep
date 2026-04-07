# uConsole-sleep
### Sleep Service Package for uConsole

This service is built for **Ubuntu 22.04** and implemented in **Python**.

It monitors power key events and controls the screen power (on/off).  
Initially, power key events were detected using a polling loop, but this was later replaced with **epoll** to reduce CPU usage.

When the screen turns off for any reason (e.g., screensaver activation, desktop lock, or system sleep), the service detects the screen-off state and applies several power-saving measures:

- Sets the CPU maximum frequency to the minimum
- Disables power to the built-in keyboard
- Disables the keyboard wakeup trigger

I also experimented with switching the CPU governor to `powersave`, but observed a slight delay during state transitions, so the current implementation adjusts the maximum CPU frequency instead.

Similarly, screen-off detection was originally implemented using a polling loop, but it was replaced with **inotify** to further reduce CPU load.

## Components

The service consists of two background processes:

### sleep-remap-powerkey
`/usr/local/bin/sleep_remap_powerkey`

Detects power key events and controls the screen power state.

### sleep-power-control
`/usr/local/bin/sleep_power_control`

Handles power-saving behavior based on the current screen state.

## How to package and install

```
ENV_VERSION=1.0 ./make_uconsole-sleep_package.sh
apt install python3-inotify python3-uinput
sudo dpkg -i uconsole-sleep.deb
```

## Configuration

See `/etc/uconsole-sleep/config` for configuration options.

## More Information

Discussion and updates are available on the ClockworkPi forum:  
https://forum.clockworkpi.com/t/uconsole-sleep-v1-2/15612?u=paragonnov

---

<a href="https://www.buymeacoffee.com/paragonnov" target="_blank">
<img src="https://cdn.buymeacoffee.com/buttons/v2/default-red.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;">
</a>
