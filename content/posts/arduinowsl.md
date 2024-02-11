---
title: "Microcontroller programming in WSL2"
description: "A brief guide for how to setup microcontroller programming in WSL2."
layout: single
date: 2024-01-10
---

## Introduction

Using WSL, Windows users can have access to all of the benefits, tools and features that come with a Linux development environment while having the experience integrate seamlessly with the Windows desktop. Combined with the Windows terminal and VSCode remote development, this experience is completely frictionless, and in my experience certainly much easier than using a virtual machine or dual-booting.

Some tasks however, such as connecting to USB devices and programming microcontrollers, can require a little more setup to get working when using WSL2. WSL2 includes a full Linux kernel that runs inside a managed virtual machine. Thus, to access any USB devices connected to the host machine an open source program called **USBIPD** is required. Luckily, this is fairly easy to setup.

## Tutorial

First, verify you are running a WSL2 distro by running `wsl -l -v` inside Powershell or the command prompt. If you wish to upgrade from WSL1 to WSL2, you can do so with `wsl --set-version <distro name> 2` inside Powershell/command prompt. Additionally, your kernel version inside WSL must be 5.10.60.1 or later, this can be verified by running `uname -a` inside WSL. These steps have been tested for Ubuntu 22.04.2, however for different distros the commands may be slightly different.

Now to install the software. Navigate to https://github.com/dorssel/usbipd-win/releases to download the latest _.msi_ installer. Running this will setup the USPIPD service as well as the tools required to connect a usb device to WSL.

Next, if running Ubuntu, inside WSL run the following commands:

```
sudo apt install linux-tools-virtual hwdata
sudo update-alternatives --install /usr/local/bin/usbip usbip `ls /usr/lib/linux-tools/*/usbip | tail -n1` 20
```

This will install the USP/IP linux tools as well as a database of USB hardware identifiers. If you are running a different distro, check the documentation at https://github.com/dorssel/usbipd-win/wiki/WSL-support to see if there are any instructions that apply to you.

## Testing

Running `lsusb` inside the Ubuntu/WSL terminal will list all of the USB devices connected to WSL:

```
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

If we navigate back to Windows and run `usbipd wsl list`, all of the USB devices connected to the Windows machine will be displayed, as well as their bus IDs and their connection status:

```
BUSID  VID:PID    DEVICE  STATE
2-1    1a86:7523  USB-SERIAL CH340 (COM11)  Not attached
2-5    27c6:639c  Goodix MOC Fingerprint  Not attached
2-6    0c45:6739  Integrated Webcam  Not attached
2-10   8087:0033  Intel(R) Wireless Bluetooth(R)  Not attached
```

The _USB-SERIAL CH340 (COM11)_ is the Arduino Uno which I would like to program inside WSL. To attach it to the WSL instance, we need to run the following inside an **Administrator Powershell / Command Prompt**: `usbipd wsl attach --busid 2-1`. Likewise, it can be detached with `usbipd wsl detach --busid 2-1`.

In the WSL, running `lsusb` now yields:

```
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 004: ID 1a86:7523 QinHeng Electronics CH340 serial converter
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

Showing we can now sucessfully access the USB device inside WSL. We are now ready to program the microcontroller, for example using the [Arduino CLI](https://arduino.github.io/arduino-cli) or [AVR Dude](https://github.com/avrdudes/avrdude)

## Useful Sites

https://learn.microsoft.com/en-us/windows/wsl/connect-usb
https://github.com/dorssel/usbipd-win/releases
https://github.com/dorssel/usbipd-win/wiki/WSL-support#usbip-client-tools
