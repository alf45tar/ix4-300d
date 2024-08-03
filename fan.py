import argparse
import time
import evdev
from   evdev  import InputDevice, categorize, ecodes
from   select import select

device  = InputDevice('/dev/input/event0')

# Function to read temperature from /sys filesystem
def read_temp_sensor(sensor_path):
    try:
        with open(sensor_path, 'r') as file:
            temp_str = file.read().strip()
            # Assuming the temperature is in millidegree Celsius
            return float(temp_str) / 1000.0
    except IOError:
        print(f"Error reading {sensor_path}")
        return None

# Function to set fan speed
def set_fan_speed(fan_path, speed):
    try:
        with open(fan_path, 'w') as file:
            file.write(str(int(speed)))
    except IOError:
        print(f"Error writing {fan_path}")

# Function to read fan speed from /sys filesystem
def read_fan_speed(fan_path):
    try:
        with open(fan_path, 'r') as file:
            speed_str = file.read().strip()
            # Assuming the fan speed is an integer in RPM
            return int(speed_str)
    except IOError:
        print(f"Error reading {fan_path}")
        return None
    except ValueError:
        print(f"Invalid fan speed format in {fan_path}")
        return None

def get_avg_temperature(sensor_paths):
    temps = []
    for path in sensor_paths:
        temp = read_temp_sensor(path)
        if temp is not None:
            temps.append(temp)

    if temps:
        avg_temp = sum(temps) / len(temps)
        return avg_temp
    else:
        return None

def get_max_temperature(sensor_paths):
    temps = []
    for path in sensor_paths:
        temp = read_temp_sensor(path)
        if temp is not None:
            temps.append(temp)

    if temps:
        max_temp = max(temps)
        return max_temp
    else:
        return None

def interpolate_speed(temp, temp_min, temp_max, speed_min, speed_max):
    if temp <= temp_min:
        return speed_min
    elif temp >= temp_max:
        return speed_max
    else:
        return speed_min + (speed_max - speed_min) * (temp - temp_min) / (temp_max - temp_min)

def save_mode(content):
    file_path = '/tmp/fanmode.txt'
    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except Exception as e:
        print(f'An error occurred: {e}')

def switch_to_normal_mode():
    global temp_max
    temp_max = 60.0
    print(f"*** Normal mode *** {temp_min:.0f}°C - {temp_max:.0f}°C ***")
    save_mode("N")

def switch_to_quiet_mode():
    global temp_max
    temp_max = 65.0
    print(f"*** Quiet mode *** {temp_min:.0f}°C - {temp_max:.0f}°C ***")
    save_mode("Q")

def switch_to_fresh_mode():
    global temp_max
    temp_max = 55.0
    print(f"*** Fresh mode *** {temp_min:.0f}°C - {temp_max:.0f}°C ***")
    save_mode("F")

modes = [switch_to_normal_mode, switch_to_fresh_mode, switch_to_quiet_mode]
current_mode_index = 0

def switch_to_next_mode():
    global current_mode_index
    current_mode_index = (current_mode_index + 1) % len(modes)
    modes[current_mode_index]()

def control_fan_speed(sensor_paths, set_fan_path, read_fan_path, debug=False):
    global temp_min
    global temp_max

    # Define temperature and fan speed ranges
    temp_min = 20.0  # Minimum temperature for interpolation
    temp_max = 60.0  # Maximum temperature for interpolation
    speed_min = 60   # Minimum fan speed (0)
    speed_max = 180  # Maximum fan speed (255)
    switch_to_normal_mode()

    while True:
        # Start the timer
        start_time = time.time()
        next_time  = start_time + 4

        # Wait for input or timer expiration
        while time.time() < next_time:
            # Check if there is an available event
            r, w, x = select([device], [], [], next_time - time.time())

            # If there is an available event, read and categorize the event
            if r:
                for event in device.read():
                    if event.type == ecodes.EV_KEY:
                        key_event = categorize(event)
                        if key_event.keystate == key_event.key_down:
                            if key_event.scancode == ecodes.KEY_SCROLLDOWN:
                                # Handle KEY_SCROLLDOWN press
                                # Execute the appropriate function based on the current temp_max
                                switch_to_next_mode()

        avg_temp = get_avg_temperature(sensor_paths)
        max_temp = get_max_temperature(sensor_paths)
        if avg_temp is not None:
            if debug:
                print(f"Avg Temperature: {avg_temp:.1f}°C")
        if max_temp is not None:
            if debug:
                print(f"Max Temperature: {max_temp:.1f}°C")

            fan_speed = interpolate_speed(max_temp, temp_min, temp_max, speed_min, speed_max)
            if debug:
                print(f"Setting fan speed to {fan_speed:.0f}")
            set_fan_speed(set_fan_path, fan_speed)
            time.sleep(1)
            current_fan_speed = read_fan_speed(read_fan_path)
            if current_fan_speed is not None:
                if debug:
                    print(f"Current Fan Speed: {current_fan_speed} RPM")
            else:
                print("Could not read fan speed data.")
        else:
            print("Could not read temperature data.")


if __name__ == "__main__":
    # Paths to the temperature sensor files in /sys filesystem
    sensor_paths = [
        "/sys/class/hwmon/hwmon2/temp1_input",    # disk 1
        "/sys/class/hwmon/hwmon3/temp1_input",    # disk 2
        "/sys/class/hwmon/hwmon4/temp1_input",    # disk 3
        "/sys/class/hwmon/hwmon5/temp1_input",    # disk 4
    ]

    # Path to set the fan speed
    set_fan_path = "/sys/class/hwmon/hwmon1/pwm1"

    # Path to read the fan speed in RPM
    read_fan_path = "/sys/class/hwmon/hwmon1/fan1_input"

    # Switch to manual mode
    set_fan_speed(set_fan_path + "_enable", "1")

    parser = argparse.ArgumentParser(description='Fan control for Lenovo ix4-300d.')
    parser.add_argument('-d', '--debug', action='store_true', help='Print debug information')
    args = parser.parse_args()

    control_fan_speed(sensor_paths, set_fan_path, read_fan_path, debug=args.debug)