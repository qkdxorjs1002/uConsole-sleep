#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p uconsole-sleep/DEBIAN
mkdir -p uconsole-sleep/usr/local/bin
mkdir -p uconsole-sleep/usr/local/lib/uconsole-sleep
mkdir -p uconsole-sleep/etc/uconsole-sleep
mkdir -p uconsole-sleep/etc/systemd/system

cp "$SCRIPT_DIR/src/find_backlight.py"        uconsole-sleep/usr/local/lib/uconsole-sleep/find_backlight.py
cp "$SCRIPT_DIR/src/find_drm_panel.py"        uconsole-sleep/usr/local/lib/uconsole-sleep/find_drm_panel.py
cp "$SCRIPT_DIR/src/find_framebuffer.py"      uconsole-sleep/usr/local/lib/uconsole-sleep/find_framebuffer.py
cp "$SCRIPT_DIR/src/find_internal_kb.py"      uconsole-sleep/usr/local/lib/uconsole-sleep/find_internal_kb.py
cp "$SCRIPT_DIR/src/find_power_key.py"        uconsole-sleep/usr/local/lib/uconsole-sleep/find_power_key.py
cp "$SCRIPT_DIR/src/sleep_display_control.py" uconsole-sleep/usr/local/lib/uconsole-sleep/sleep_display_control.py
cp "$SCRIPT_DIR/src/sleep_power_control.py"   uconsole-sleep/usr/local/lib/uconsole-sleep/sleep_power_control.py
cp "$SCRIPT_DIR/src/sleep_remap_powerkey.py"  uconsole-sleep/usr/local/lib/uconsole-sleep/sleep_remap_powerkey.py

cat << 'EOF' > uconsole-sleep/usr/local/bin/sleep_power_control
#!/bin/bash
cd /usr/local/lib/uconsole-sleep
exec python3 -u sleep_power_control.py "$@"
EOF

cat << 'EOF' > uconsole-sleep/usr/local/bin/sleep_remap_powerkey
#!/bin/bash
cd /usr/local/lib/uconsole-sleep
exec python3 -u sleep_remap_powerkey.py "$@"
EOF

cp "$SCRIPT_DIR/config.default" uconsole-sleep/etc/uconsole-sleep/config.default

cp "$SCRIPT_DIR/services/sleep-power-control.service"  uconsole-sleep/etc/systemd/system/sleep-power-control.service
cp "$SCRIPT_DIR/services/sleep-remap-powerkey.service" uconsole-sleep/etc/systemd/system/sleep-remap-powerkey.service

cat << 'EOF' > uconsole-sleep/DEBIAN/control
Package: uconsole-sleep
Version: ENV_VERSION
Maintainer: paragonnov (github.com/qkdxorjs1002)
Original-Maintainer: paragonnov (github.com/qkdxorjs1002)
Architecture: all
Depends: python3, python3-inotify, python3-uinput
Description: uConsole Sleep control scripts.
 Source-Site: https://github.com/qkdxorjs1002/uConsole-sleep
EOF

sed -i "s|ENV_VERSION|$ENV_VERSION|g" uconsole-sleep/DEBIAN/control

cat << 'EOF' > uconsole-sleep/DEBIAN/postinst
#!/bin/bash

cp -n /etc/uconsole-sleep/config.default /etc/uconsole-sleep/config

systemctl daemon-reload

systemctl enable sleep-power-control.service
systemctl enable sleep-remap-powerkey.service

systemctl start sleep-power-control.service
systemctl start sleep-remap-powerkey.service
EOF

cat << 'EOF' > uconsole-sleep/DEBIAN/prerm
#!/bin/bash

systemctl stop sleep-power-control.service
systemctl stop sleep-remap-powerkey.service

systemctl disable sleep-power-control.service
systemctl disable sleep-remap-powerkey.service
EOF

cat << 'EOF' > uconsole-sleep/DEBIAN/postrm
#!/bin/bash

systemctl daemon-reload
EOF

chmod +x uconsole-sleep/etc/uconsole-sleep/*
chmod +x uconsole-sleep/usr/local/bin/*
chmod +x uconsole-sleep/DEBIAN/postinst uconsole-sleep/DEBIAN/prerm uconsole-sleep/DEBIAN/postrm

dpkg-deb --build --root-owner-group uconsole-sleep

rm -rf uconsole-sleep
