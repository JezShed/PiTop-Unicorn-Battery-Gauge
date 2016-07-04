# PiTop-Unicorn-Battery-Gauge
Battery gauge (and CAPS LOCK status) for the Pi-Top using the Pimoroni Unicorn Hat

Please note, this is ONLY for the [Pi-Top](http://www.pi-top.com/) with a [Pimoroni Unicorn Hat](https://shop.pimoroni.com/products/unicorn-hat).

Battery level is displayed as a multi-coloured battery icon on the 8x8 RGB LED matrix. Caps-Lock is also displayed (as a little letter 'C') and charging status is displayed as a little '+' symbol.

If battery capacity is less than 5% (and not charging) then a graceful shutdown countdown will be displayed. The countdown from 9 to 0 will take 30 seconds before the shutdown command (sudo shutdown -h now) is executed. This gives time for you to quit your work.

If the charger is plugged in during the countdown then the countdown is automatically aborted.

**Installation steps:**

1. If you haven't done so already, make sure you've installed the [Pimoroni Unicorn Hat libraries for Python](https://github.com/pimoroni/unicorn-hat).
2. Please note that the Pimoroni Unicorn Hat actually uses the PWM module to generate the data stream that is fed into the chain of 64 LEDs. The PWM module is normally used to generate the analogue audio (from the 3.5mm jack). The analogue audio must be disabled for the Unicorn hat to work (especially on later releases of Rasbian). This is done by editing the /boot/config.txt file by typing:
`sudo nano /boot/config.txt`
Then make sure these lines are uncommented:
`hdmi_force_hotplug=1`
`hdmi_force_edid_audio=1`
Press CTRL-X to exit and then press Y to accept the save.
(Thank you to [@gadgetoid] for this tip)
3. Copy 'bat.py' file to a suitable location, such as '/home/pi/Pimoroni/unicornhat'.
4. To make sure the program starts everytime the desktop appears, open a console and type:
`sudo nano /etc/profile`.
Scroll to the bottom of the file and add the line:
`sudo python3 /home/pi/Pimoroni/unicornhat/bat.py &`.
Press CTRL-X to exit and then press Y to accept the save.
5. Restart your Pi-Top.

**Notes:**

1. The charge status is sampled every 5 seconds.

2. The CAPS LOCK status is sampled every 0.5 seconds.

See also this excellent [Pi-Top battery monitor](https://github.com/rricharz/pi-top-battery-status) to run on your desktop by [@rricharz](https://github.com/rricharz) 
