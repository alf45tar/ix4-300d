#!/usr/bin/python3

import os
from periphery import GPIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys
import socket
import time
import base64
import io
import time
import evdev
from evdev import InputDevice, categorize, ecodes
from select import select
import psutil

RS = GPIO(29, "out")
A0 = GPIO(30, "out")
CS = GPIO(28, "out")
RW = GPIO(31, "out")
E  = GPIO(32, "out")

D0 = GPIO(33, "out")
D1 = GPIO(34, "out")
D2 = GPIO(35, "out")
D3 = GPIO(36, "out")
D4 = GPIO(37, "out")
D5 = GPIO(38, "out")
D6 = GPIO(39, "out")
D7 = GPIO(40, "out")
DATA = [D7,D6,D5,D4,D3,D2,D1,D0]

A0_DATA = 0x01
A0_CMD  = 0x00

logo = """Qk02JAAAAAAAADYEAAAoAAAAgAAAAEAAAAABAAgAAAAAAAAgAAAjLgAAIy4AAAABAAAAAQAAAAAAAAEBAQACAgIAAwMDAAQEBAAFBQUABgYGAAcHBwAICAgACQkJAAoKCgALCwsADAwMAA0NDQAODg
          4ADw8PABAQEAAREREAEhISABMTEwAUFBQAFRUVABYWFgAXFxcAGBgYABkZGQAaGhoAGxsbABwcHAAdHR0AHh4eAB8fHwAgICAAISEhACIiIgAjIyMAJCQkACUlJQAmJiYAJycnACgoKAApKSkAKioq
          ACsrKwAsLCwALS0tAC4uLgAvLy8AMDAwADExMQAyMjIAMzMzADQ0NAA1NTUANjY2ADc3NwA4ODgAOTk5ADo6OgA7OzsAPDw8AD09PQA+Pj4APz8/AEBAQABBQUEAQkJCAENDQwBEREQARUVFAEZGRg
          BHR0cASEhIAElJSQBKSkoAS0tLAExMTABNTU0ATk5OAE9PTwBQUFAAUVFRAFJSUgBTU1MAVFRUAFVVVQBWVlYAV1dXAFhYWABZWVkAWlpaAFtbWwBcXFwAXV1dAF5eXgBfX18AYGBgAGFhYQBiYmIA
          Y2NjAGRkZABlZWUAZmZmAGdnZwBoaGgAaWlpAGpqagBra2sAbGxsAG1tbQBubm4Ab29vAHBwcABxcXEAcnJyAHNzcwB0dHQAdXV1AHZ2dgB3d3cAeHh4AHl5eQB6enoAe3t7AHx8fAB9fX0Afn5+AH
          9/fwCAgIAAgYGBAIKCggCDg4MAhISEAIWFhQCGhoYAh4eHAIiIiACJiYkAioqKAIuLiwCMjIwAjY2NAI6OjgCPj48AkJCQAJGRkQCSkpIAk5OTAJSUlACVlZUAlpaWAJeXlwCYmJgAmZmZAJqamgCb
          m5sAnJycAJ2dnQCenp4An5+fAKCgoAChoaEAoqKiAKOjowCkpKQApaWlAKampgCnp6cAqKioAKmpqQCqqqoAq6urAKysrACtra0Arq6uAK+vrwCwsLAAsbGxALKysgCzs7MAtLS0ALW1tQC2trYAt7
          e3ALi4uAC5ubkAurq6ALu7uwC8vLwAvb29AL6+vgC/v78AwMDAAMHBwQDCwsIAw8PDAMTExADFxcUAxsbGAMfHxwDIyMgAycnJAMrKygDLy8sAzMzMAM3NzQDOzs4Az8/PANDQ0ADR0dEA0tLSANPT
          0wDU1NQA1dXVANbW1gDX19cA2NjYANnZ2QDa2toA29vbANzc3ADd3d0A3t7eAN/f3wDg4OAA4eHhAOLi4gDj4+MA5OTkAOXl5QDm5uYA5+fnAOjo6ADp6ekA6urqAOvr6wDs7OwA7e3tAO7u7gDv7+
          8A8PDwAPHx8QDy8vIA8/PzAPT09AD19fUA9vb2APf39wD4+PgA+fn5APr6+gD7+/sA/Pz8AP39/QD+/v4A////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAyNFXVM9HgMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHV/PkC4HAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJIT//2AEAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAE3L//3JPAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAADbB/50vAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAVh///3KwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMjP//wyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADJ7//3UkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAyb//9xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFf///9xEAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGL///82AAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAA2////QwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAFNv//4EBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB8////IwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANP///4IFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO3////UgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOv///8AOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOs////UwsAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALf
          ////+SAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAABy/////zUAAAAAAAAAAAAAAAAAAAAAAAAAAxgsJAsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACvf//4MwAAAAAAAAAAAAAAAAAAAAAAAELj8/JBgQFAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAw///HCQAAAAAAAAAAAAAAAAAAAAABNpg0M1WBjJOHbEcdAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAF7//1kAAAAAAAAAAAAAAAAAAAAAD245Xv///7qTk/////+bNwMAAAAAAAAAAAAAAAAAAAAA
          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"""


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def set_gpio(pin,value):
	pin.direction = "out"
	if value == 0:
		outval = False
	else:
		outval = True
	pin.write(outval)

def read_gpio(pin):
	pin.direction = "in"
	if pin.read():
		return 1
	else:
		return 0

def write_lcm(A0type, input):
	mask=128
	set_gpio(E,0)
	for pin in DATA:
		set_gpio(pin,(input & mask))
		mask=int(mask/2)
	set_gpio(A0,A0type)
	set_gpio(RW,0)
	set_gpio(CS,0)
	set_gpio(E,1)
	set_gpio(E,0)
	set_gpio(CS,1)

def read_lcm(page,line):
	set_page(page)
	output = 0x00
	for i in range(line):
		output = 0x00
		set_gpio(E,0)
		set_gpio(A0,A0_DATA)
		set_gpio(RW,1)
		set_gpio(CS,0)
		set_gpio(E,1)
		mask=128
		for pin in DATA:
			pin.direction = "in"
			if pin.read():
				output += mask
			mask=int(mask/2)
		set_gpio(E,0)
		set_gpio(CS,1)
	print(hex(output))

def read_lcm_img():
	outimg = [0] * 8192
	for page in range(8):
		set_page(page)
		for line in range(128):
			set_gpio(E,0)
			set_gpio(A0,A0_DATA)
			set_gpio(RW,1)
			set_gpio(CS,0)
			set_gpio(E,1)
			outimg[(page*8*128)+(0*128)+line] = read_gpio(D0)
			outimg[(page*8*128)+(1*128)+line] = read_gpio(D1)
			outimg[(page*8*128)+(2*128)+line] = read_gpio(D2)
			outimg[(page*8*128)+(3*128)+line] = read_gpio(D3)
			outimg[(page*8*128)+(4*128)+line] = read_gpio(D4)
			outimg[(page*8*128)+(5*128)+line] = read_gpio(D5)
			outimg[(page*8*128)+(6*128)+line] = read_gpio(D6)
			outimg[(page*8*128)+(7*128)+line] = read_gpio(D7)
			set_gpio(E,0)
			set_gpio(CS,1)

	for y in range(64):
		for x in range(128):
			print(outimg[(y*128)+x],end="")
		print("")

def init_lcm():
	set_gpio(RS,1)

	for x in [0xae,0xa2,0xa0,0xc8,0xa6,0x40,0x22,0x81,0x3f,0xf8,0x00,0xa4,0x2c]:
		write_lcm(A0_CMD,x)

	write_lcm(A0_CMD,0x2e)
	write_lcm(A0_CMD,0x2f)
	write_lcm(A0_CMD,0xaf)

def exit_lcm():
	RS.close()
	CS.close()
	RW.close()
	A0.close()
	E.close()
	for x in DATA:
		x.close()

def set_page(page):
	write_lcm(A0_CMD,(0xB0 + page))
	write_lcm(A0_CMD,0x10)
	write_lcm(A0_CMD,0x00)

def draw_lcm(image, display_off = True):
	if display_off:
		write_lcm(A0_CMD,0xae)
	for page in range(8):
		set_page(page)
		for line in range(128):
			write_lcm(A0_DATA, image[(page*128)+line])
	if display_off:
		write_lcm(A0_CMD,0xaf)

def refresh_screen(pixels, width = 128, height = 64):
	img = [0x00] * 1024

	if width > 128:
		width = 128
	if height > 64:
		height = 64

	for y in range(int(height/8)):
		for x in range(width):
			outbyte = 0x00
			for bit in range(8):
				if pixels[x,(y*8)+bit] != 0:
					outbyte += 2**bit
			img[x+(128*y)] = outbyte
	draw_lcm(img)

def draw_logo():
	im = Image.open(io.BytesIO(base64.b64decode(logo)))
	drw = ImageDraw.Draw(im)
	refresh_screen(im.load(), im.size[0], im.size[1])

def get_load_avg():
    try:
        with open('/proc/loadavg', 'r') as f:
            load_avg = f.readline().split()[:3]
        return [float(x) for x in load_avg]
    except:
        return 0

def get_cpu_count():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpu_info = f.read()
        return cpu_info.count('processor\t:')
    except:
        return 2

def cpu_usage():
    load_avg  = get_load_avg()
    cpu_count = get_cpu_count()

    cpu_usage_1min  = (load_avg[0] / cpu_count) * 100
    cpu_usage_5min  = (load_avg[1] / cpu_count) * 100
    cpu_usage_15min = (load_avg[2] / cpu_count) * 100

    return cpu_usage_1min

def get_memory_info():
    try:
        meminfo = {}
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                parts = line.split()
                key = parts[0].rstrip(':')
                value = int(parts[1])  # Value is in kilobytes
                meminfo[key] = value
        return meminfo
    except:
        return {}

def memory_usage():
    try:
        meminfo = get_memory_info()

        mem_total = meminfo['MemTotal']
        mem_free  = meminfo['MemFree']
        buffers   = meminfo['Buffers']
        cached    = meminfo['Cached']

        mem_used          = mem_total - (mem_free + buffers + cached)
        mem_usage_percent = (mem_used / mem_total) * 100

        return mem_usage_percent
    except:
        return 0

def read_sensor(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except:
        return "0"

def read_fanmode():
    file_path = '/tmp/fanmode.txt'
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        print(f'An error occurred: {e}')
        return ''

def display_home():
    try:
        im = Image.new(mode = "L", size = (128, 64))
        drw = ImageDraw.Draw(im)
        drw.text((0, 50), "CPU: " + str(int(cpu_usage())) + "%   RAM: " + str(int(memory_usage())) + "%", fill='white')
        hostname = socket.gethostname()
        drw.text((0, 0), "Hostname: " + hostname, fill='white')
        drw.text((0, 10), "IP: " + get_local_ip(), fill='white')
        cpuTemp = read_sensor('/sys/class/hwmon/hwmon0/temp1_input')
        drw.text((0, 20), "CPU Temp: " + str(round(int(cpuTemp)/1000, 1)) + " °C", fill='white')
        hd1Temp = read_sensor('/sys/class/hwmon/hwmon2/temp1_input')
        hd2Temp = read_sensor('/sys/class/hwmon/hwmon3/temp1_input')
        hd3Temp = read_sensor('/sys/class/hwmon/hwmon4/temp1_input')
        hd4Temp = read_sensor('/sys/class/hwmon/hwmon5/temp1_input')
        drw.text((0, 30), "HDs Temp: " + str(int(int(hd1Temp)/1000)) + " " + str(int(int(hd2Temp)/1000)) + " " + str(int(int(hd3Temp)/1000)) + " " + str(int(int(hd4Temp)/1000)), fill='white')
        fanSpeed = read_sensor('/sys/class/hwmon/hwmon1/fan1_input')
        drw.text((0, 40), "Fan Speed " + read_fanmode() + ": " + fanSpeed.strip() + " rpm", fill='white')
        refresh_screen(im.load(), im.size[0], im.size[1])
        im.save("/tmp/systemstatus.jpg")

    except Exception as e:
        print(f"Error in draw_text: {e}")

def get_md_array_status(md_device):
    try:
        # Read the /proc/mdstat file
        with open('/proc/mdstat', 'r') as f:
            mdstat_content = f.read()

        # Find the section for the specified md device
        device_section = next((section for section in mdstat_content.split('\n\n') if md_device in section), None)

        if not device_section:
            print(f"Device {md_device} not found in /proc/mdstat")
            return None

        # Extract the status line from the device section
        status_line = next((line for line in device_section.split('\n') if 'U' in line), None)

        if status_line:
            return ''.join([c for c in status_line if c in 'U_'])
        else:
            print(f"Status line not found for {md_device}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def display_disk_usage():
    try:
        mountpoint1 = '/boot'
        mountpoint2 = '/'
        mountpoint3 = '/srv'

        # Get disk usage information
        disk_usage1 = psutil.disk_usage(mountpoint1)
        disk_usage2 = psutil.disk_usage(mountpoint2)
        disk_usage3 = psutil.disk_usage(mountpoint3)

        # Create a 128x64 image
        image = Image.new(mode = "L", size = (128, 64))
        draw = ImageDraw.Draw(image)

        # Define the bounding box for the pie chart
        bbox1 = [ 2, 2,  41, 41]
        bbox2 = [44, 2,  83, 41]
        bbox3 = [86, 2, 125, 41]

        # Draw the border around the pie chart
        draw.ellipse(bbox1, outline='white')
        draw.ellipse(bbox2, outline='white')
        draw.ellipse(bbox3, outline='white')

        # Calculate the start and end angles for the pie slices
        start_angle = 0
        end_angle1 = int(360 * (disk_usage1.percent / 100))
        end_angle2 = int(360 * (disk_usage2.percent / 100))
        end_angle3 = int(360 * (disk_usage3.percent / 100))

        # Draw used space slice
        draw.pieslice(bbox1, start=start_angle, end=end_angle1, fill='white')
        draw.pieslice(bbox2, start=start_angle, end=end_angle2, fill='white')
        draw.pieslice(bbox3, start=start_angle, end=end_angle3, fill='white')

        # Add text labels
        draw.text(( 0 + (42 - draw.textlength(mountpoint1)) / 2, 43), mountpoint1, fill='white')
        draw.text((44 + (42 - draw.textlength(mountpoint2)) / 2, 43), mountpoint2, fill='white')
        draw.text((86 + (42 - draw.textlength(mountpoint3)) / 2, 43), mountpoint3, fill='white')

        percent =  str(int(disk_usage1.percent)) + '%'
        if disk_usage1.percent < 50:
                draw.text(( 0 + (42 - draw.textlength(percent)) / 2, 10), percent, fill='white')
        else:
                draw.text(( 0 + (42 - draw.textlength(percent)) / 2, 23), percent, fill='black')

        percent =  str(int(disk_usage2.percent)) + '%'
        if disk_usage2.percent < 50:
                draw.text((44 + (42 - draw.textlength(percent)) / 2, 10), percent, fill='white')
        else:
                draw.text((44 + (42 - draw.textlength(percent)) / 2, 23), percent, fill='black')

        percent =  str(int(disk_usage3.percent)) + '%'
        if disk_usage3.percent < 50:
               draw.text((86 + (42 - draw.textlength(percent)) / 2, 10), percent, fill='white')
        else:
               draw.text((86 + (42 - draw.textlength(percent)) / 2, 23), percent, fill='black')

        status = get_md_array_status('md0')
        draw.text((44 + (42 - draw.textlength(status)) / 2, 53), status, fill='white')
        status = get_md_array_status('md1')
        draw.text((86 + (42 - draw.textlength(status)) / 2, 53), status, fill='white')

        refresh_screen(image.load(), image.size[0], image.size[1])
        image.save("/tmp/diskusage.jpg")

    except Exception as e:
        print(f"Error in display_disk_usage: {e}")

def cycle_backlight(backlight_index=[2]):
    backlight_values = [0, 50, 100, 150, 200, 250]
    backlight_index[0] = (backlight_index[0] + 1) % len(backlight_values)
    set_backlight(backlight_values[backlight_index[0]])

def set_backlight(value):
    pwm_file = '/sys/class/i2c-adapter/i2c-0/0-002e/hwmon/hwmon1/pwm3'
    try:
        with open(pwm_file, 'w') as file:
            file.write(str(value))
    except IOError as e:
        print(f"Failed to write {pwm_file}: {e}")


device  = InputDevice('/dev/input/event0')
screens = [display_home, display_disk_usage]

# Constants for long press detection and backlight cycling
LONG_PRESS_THRESHOLD = 2   # seconds
CYCLE_BACKLIGHT_INTERVAL = 0.5  # seconds

# State variables for button press tracking
button_select_pressed = False
button_select_press_time = None
last_backlight_cycle_time = None
long_press_detected = False

init_lcm()
cycle_backlight()
draw_logo()
time.sleep(5)
index = 0
while True:
    # Display the current screen
    screens[index]()

    # Start the timer for the 60-second delay
    start_time = time.time()
    next_time  = start_time + 60

    # Wait for input or timer expiration
    while time.time() < next_time:
        # Check if there is an available event
        r, w, x = select([device], [], [], 0.1)  # Poll every 0.1 seconds for better responsiveness
        # If there is an available event, read and categorize the event
        if r:
            for event in device.read():
                if event.type == ecodes.EV_KEY:
                    key_event = categorize(event)
                    if key_event.scancode == ecodes.BTN_SELECT:
                        if key_event.keystate == key_event.key_down:
                            # Handle BTN_SELECT press
                            if not button_select_pressed:
                                button_select_pressed = True
                                button_select_press_time = time.time()
                                last_backlight_cycle_time = button_select_press_time  # Initialize backlight cycle time
                                long_press_detected = False
                        elif key_event.keystate == key_event.key_up:
                            # Handle BTN_SELECT release
                            if button_select_pressed:
                                press_duration = time.time() - button_select_press_time
                                if press_duration >= LONG_PRESS_THRESHOLD:
                                    long_press_detected = True
                                else:
                                    if not long_press_detected:  # Only trigger short press if no long press was detected
                                        # Interrupt the delay and move to the next screen
                                        next_time = time.time()
                                button_select_pressed = False
                                button_select_press_time = None
                                last_backlight_cycle_time = None
                                long_press_detected = False
                    else:
                        # Handle other keys
                        if key_event.keystate == key_event.key_down:
                            if key_event.scancode == ecodes.KEY_POWER:
                                pass  # Handle KEY_POWER press
                            elif key_event.scancode == ecodes.KEY_SCROLLDOWN:
                                # Handle KEY_SCROLLDOWN press
                                time.sleep(1)
                                index = -1
                                next_time = time.time()
                                pass
                            elif key_event.scancode == ecodes.KEY_RESTART:
                                pass  # Handle KEY_RESTART press

        # If the BTN_SELECT is pressed for more than LONG_PRESS_THRESHOLD,
        # execute cycle_backlight every CYCLE_BACKLIGHT_INTERVAL seconds
        if button_select_pressed:
            current_time = time.time()
            press_duration = current_time - button_select_press_time
            if  press_duration >= LONG_PRESS_THRESHOLD:
                if current_time - last_backlight_cycle_time >= CYCLE_BACKLIGHT_INTERVAL:
                    cycle_backlight()
                    last_backlight_cycle_time = current_time

    # Move to the next screen
    index = (index + 1) % len(screens)

exit_lcm()
