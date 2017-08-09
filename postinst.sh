#!/bin/sh
echo "Setting User Permissions for USB port for EXPEYES: AVR, FT232 and MCP2200"
cat << EOF > /etc/udev/rules.d/99-expeyes.rules
SUBSYSTEM=="usb",ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="21ff", MODE="666"
SUBSYSTEM=="tty",ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", MODE="666"
SUBSYSTEM=="tty",ATTRS{idVendor}=="04d8", ATTRS{idProduct}=="00df", MODE="666"

ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="21ff", ENV{ID_MM_DEVICE_IGNORE}="1"
ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", ENV{ID_MM_DEVICE_IGNORE}="1"
ATTRS{idVendor}=="04d8", ATTRS{idProduct}=="00df", ENV{ID_MM_DEVICE_IGNORE}="1"
EOF
#cat /etc/udev/rules.d/99-expeyes.rules
service udev restart
#/etc/init.d/udev restart
echo "Reconnect EXEYES-17 on USB Port for permissions to take effect"
