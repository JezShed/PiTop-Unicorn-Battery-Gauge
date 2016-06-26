#!/usr/bin/env python

##########################################################
## pi-top Battery level gauge using Pimoroni's Unicorn  ##
## Hat by calling 'pt-battery' and capturing its output.##
## Also displays CAPS-LOCK status.                      ##
## Now starts a shutdown sequence if battery < 5%       ##
## Example by Jez - @JezShed                            ##
## Version 1.4, 22nd June 2016                          ##
##########################################################

import unicornhat, time, subprocess, sys


def plotnum(num):
    if num==9:
        bitmap=[
            "........",
            "....###.",
            "...#...#",
            "...#...#",
            "....####",
            ".......#",
            ".......#",
            "....###."]
    if num==8:
        bitmap=[
            "........",
            "....###.",
            "...#...#",
            "...#...#",
            "....###.",
            "...#...#",
            "...#...#",
            "....###."]
    if num==7:
        bitmap=[
            "........",
            "...#####",
            ".......#",
            ".......#",
            "......#.",
            "......#.",
            ".....#..",
            ".....#.."]
    if num==6:
        bitmap=[
            "........",
            "....###.",
            "...#....",
            "...#....",
            "...####.",
            "...#...#",
            "...#...#",
            "....###."]
    if num==5:
        bitmap=[
            "........",
            "...#####",
            "...#....",
            "...#....",
            "....###.",
            ".......#",
            ".......#",
            "...####."]
    if num==4:
        bitmap=[
            "........",
            "......#.",
            ".....##.",
            "....#.#.",
            "...#..#.",
            "...#####",
            "......#.",
            "......#."]
    if num==3:
        bitmap=[
            "........",
            "...#####",
            "......#.",
            ".....#..",
            "....###.",
            ".......#",
            ".......#",
            "...####."]
    if num==2:
        bitmap=[
            "........",
            "....###.",
            "...#...#",
            ".......#",
            "......#.",
            ".....#..",
            "....#...",
            "...#####"]
    if num==1:
        bitmap=[
            "........",
            ".....#..",
            "....##..",
            "...#.#..",
            ".....#..",
            ".....#..",
            ".....#..",
            "...#####"]
    if num==0:
        bitmap=[
            "........",
            "....###.",
            "...#...#",
            "...#...#",
            "...#...#",
            "...#...#",
            "...#...#",
            "....###.",
            "........"]

    for y in range(0, 8):
        for x in range(0, 8):
            if bitmap[y][x]=="#":
                unicornhat.set_pixel(x,y,255,255,255)
            else:
                unicornhat.set_pixel(x,y,0,0,0)
    unicornhat.show()

    time.sleep(0.1)

    for y in range(0, 8):
        for x in range(0, 8):
            if bitmap[y][x]=="#":
                unicornhat.set_pixel(x,y,255,0,0)
            else:
                unicornhat.set_pixel(x,y,0,0,0)
    unicornhat.show()

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
    #print(batterystatus)
    bat=-1 # Rogue value of -1 if no usable response from pt-battery
    str1=str(batterystatus)
    str2="Capacity" # Search for this word
    position=str1.find(str2)+9
    capacity=(str1[position:position+4])
    #print('*',capacity,'*',sep="")
    if capacity[3]=="%":
        capacity=capacity[0:3]
    elif capacity[2]=="%":
        capacity=capacity[0:2]
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


def shutdownsequence():
    unicornhat.clear()
    for n in range(9,-1,-1):
        plotnum(n)
        time.sleep(2)
        batterystatus=str(getbatterystatus())
        if batterystatus.find("Charging")>0: # Back on charge?
            unicornhat.clear()  # Clear the display
            drawbattery()   # Draw the battery
            unicornhat.show()
            return()        # Carry on
#    subprocess.call("sudo shutdown -h now")  # Issue shutdown command
    p = subprocess.Popen(["sudo shutdown -h now"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sys.exit(0)             # Quit this program
    

##############################
## Main program starts here ##
##############################
unicornhat.rotation(0)
unicornhat.clear()          # Clear the display
unicornhat.brightness(0.5)  # Global unicorn brightness
drawbattery()               # Draw the battery
unicornhat.show()
time.sleep(0.5)
shutdownlevel=5             # Battery level that will trigger a shutdown
startanim=1                 # Start-up anim only on the first run
while True:
    batterystatus=str(getbatterystatus())
    print(batterystatus)
    bat=chargecapacity(batterystatus)
    if bat!=-1:
        showcapacity(bat,startanim)
    elif startanim == 1:
        showcapacity(100,startanim) # Shows 100% on startup if pt-battery
                                    # returns error (which it does when
                                    # fully charged and plugged in.
            
    startanim=0
    
    # Display little "+" symbol if we are charging
    showchargesymbol(batterystatus)

    if batterystatus.find("Discharging")>0:
        if bat<=shutdownlevel and bat!=-1:
            shutdownsequence()      # Shutdown gracefully

    # Checks CAPS LOCK 10 times (once every 0.5 Secs) then carries on
    for y in range(0,10):
        showcapslock(capslockstatus())
        unicornhat.show()
        time.sleep(0.5)     # Sleep most of the time
