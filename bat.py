#!/usr/bin/env python

##########################################################
## pi-top Battery level gauge using Pimoroni's Unicorn  ##
## Hat by calling 'pt-battery' and capturing its output.##
## Also displays CAPS-LOCK status                       ##
## Example by Jez - @JezShed                            ##
## Version 1.2, 1st May 2016                            ##
##########################################################

import unicornhat, time, subprocess


def drawbattery():    #Draw the naked battery
    for n in range(1, 8):
        unicornhat.set_pixel(3, n, 64, 64, 255)
        unicornhat.set_pixel(7, n, 64, 64, 255)
    for n in range(4, 7):
        unicornhat.set_pixel(n, 0, 192, 192, 192)
        unicornhat.set_pixel(n, 7, 192, 192, 192)
    unicornhat.show()


def getbatterystatus():
    # Issue 'pt-battery' command and capture response
    p = subprocess.Popen(["pt-battery"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    answer, err = p.communicate()
    return(answer)


def chargecapacity(batterystatus):
    # Now search the returned string for the capacity figure
    bat=-1 # Rogue value of -1 if no usable response from pt-battery
    str1=str(batterystatus)
    str2="Capacity" # Search for this word
    position=str1.find(str2)+9
    capacity=(str1[position:position+4])
    if capacity[3]=="%":
        capacity=capacity[0:3]
    try:
        bat=int(capacity)
    except ValueError:
        print("pt-battery didn't return a capacity figure, probably busy, I'll try again.")
    return(bat)


def showcapacity(bat,startanim):
    # Plot the battery level on the Unicorn Hat
    b=0
    for y in range(0,6):
        batthreshold=int(16.666*y)
        if y==0:            # Red
            r=255
            g=0
        if y==1:
            r=255
            g=128
        if y==2:
            r=255
            g=192
        if y==3:
            r=192
            g=255
        if y==4:
            r=128
            g=255
        if y==5:            # through to Green
            r=0
            g=255
        if bat<batthreshold:
            r=0
            g=0
        elif startanim==1:
            unicornhat.set_pixel(4,6-y,255,255,255)
            unicornhat.set_pixel(5,6-y,255,255,255)
            unicornhat.set_pixel(6,6-y,255,255,255)
            unicornhat.show()
            time.sleep(0.1)
            unicornhat.set_pixel(4,6-y,r,g,b)
            unicornhat.set_pixel(5,6-y,r,g,b)
            unicornhat.set_pixel(6,6-y,r,g,b)
            unicornhat.show()
            time.sleep(0.1)

        unicornhat.set_pixel(4,6-y,r,g,b)
        unicornhat.set_pixel(5,6-y,r,g,b)
        unicornhat.set_pixel(6,6-y,r,g,b)


def showchargesymbol(batterystatus):
    if batterystatus.find("Charging")>0:
        r=255
    else:
        r=0
    unicornhat.set_pixel(1,0,r,0,0)
    unicornhat.set_pixel(0,1,r,0,0)
    unicornhat.set_pixel(1,1,r,0,0)
    unicornhat.set_pixel(2,1,r,0,0)
    unicornhat.set_pixel(1,2,r,0,0)


def capslockstatus():
    p = subprocess.Popen(["xset q | grep LED"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    answer, err = p.communicate()
    led=int(str(answer)[67:68]) # Extract 67th character from string
    return(led)                 # =1 for CAPS LOCK ON


def showcapslock(led):
    if led==1:
        r=255
        g=255
        b=255
    else:
        r=0
        g=0
        b=0
    unicornhat.set_pixel(0,5,r,g,b)
    unicornhat.set_pixel(0,6,r,g,b)
    unicornhat.set_pixel(0,7,r,g,b)
    unicornhat.set_pixel(1,5,r,g,b)
    unicornhat.set_pixel(1,7,r,g,b)


##############################
## Main program starts here ##
##############################
unicornhat.rotation(0)
unicornhat.clear()          # Clear the display
unicornhat.brightness(0.5)  # Globalunicorn brightness
drawbattery()               # Draw the battery
unicornhat.show()
time.sleep(0.5)
startanim=1                 # Start-up anim only on the first run
while True:
    batterystatus=str(getbatterystatus())
    print(batterystatus)
    bat=chargecapacity(batterystatus)
    if bat!=-1:
        showcapacity(bat,startanim)
    startanim=0
    
    # Display little "+" symbol if we are charging
    showchargesymbol(batterystatus)

    # Checks CAPS LOCK 10 times (once every 0.5 Secs) then carries on
    for y in range(0,10):
        showcapslock(capslockstatus())
        unicornhat.show()
        time.sleep(0.5)     # Sleep most of the time
