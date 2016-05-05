# PiTop-Unicorn-Battery-Gauge
Battery gauge (and CAPS LOCK status) for the Pi-Top using the Pimoroni Unicorn Hat

Please note, this is ONLY for the [Pi-Top](http://www.pi-top.com/) with a [Pimoroni Unicorn Hat](https://shop.pimoroni.com/products/unicorn-hat).

**Installation steps:**

1. If you haven't done so already, make sure you've installed the [Pimoroni Unicorn Hat libraries for Python](https://github.com/pimoroni/unicorn-hat).

2. Copy 'bat.py' file to a suitable location, such as '/home/pi/Pimoroni/unicornhat'.
 
3. To make sure the program starts everytime the desktop appears, open a console and type:
`sudo nano /etc/profile`.

4. Scroll to the bottom of the file and add the line:
`sudo python3 /home/pi/Pimoroni/unicornhat/bat.py &`.

5. Press CTRL-X to exit and then press Y to accept the save.

6. Restart your Pi-Top.

**Notes:**

1. The charge status is sampled every 5 seconds.

2. The CAPS LOCK status is sampled every 0.5 seconds.

See also this excellent [Pi-Top battery monitor](https://github.com/rricharz/pi-top-battery-status) to run on your desktop by [@rricharz](https://github.com/rricharz) 
