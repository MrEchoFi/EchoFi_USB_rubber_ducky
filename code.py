# EchoFi_USB is developed and modified by Md. Abu Naser Nayeem [tanjib]_Mr.EchoFi
# copyright (c) 2025 Md. Abu Naser Nayeem [tanjib]_Mr.EchoFi
# Note- this project is inspaired by dbisu|pico-ducky and this script is better and modified script from dbisu|pico-ducky
""" 
███████╗ ██████╗██╗  ██╗ ██████╗ ███████╗██╗    ██╗   ██╗███████╗██████╗ 
██╔════╝██╔════╝██║  ██║██╔═══██╗██╔════╝██║    ██║   ██║██╔════╝██╔══██╗
█████╗  ██║     ███████║██║   ██║█████╗  ██║    ██║   ██║███████╗██████╔╝
██╔══╝  ██║     ██╔══██║██║   ██║██╔══╝  ██║    ██║   ██║╚════██║██╔══██╗
███████╗╚██████╗██║  ██║╚██████╔╝██║     ██║    ╚██████╔╝███████║██████╔╝
╚══════╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝     ╚═════╝ ╚══════╝╚═════╝ 
                                                                         
 """
import time
import asyncio
import digitalio
from board import *
import board
from EchoFi_USB import *
import supervisor

# Check for Pico W boards and import WiFi and webapp modules if applicable
if board.board_id in ['raspberry_pi_pico_w', 'raspberry_pi_pico2_w']:
    import wifi
    from webapp import *

# Sleep at the start to allow the device to be recognized by the host computer
time.sleep(0.5)

def startWiFi():
    """Initialize WiFi connection using secrets from secrets.py."""
    import ipaddress
    try:
        from secrets import secrets
    except ImportError:
        print("WiFi secrets are kept in secrets.py, please add them there!")
        raise

    try:
        print("Connecting to WiFi...")
        wifi.radio.connect(secrets['ssid'], secrets['password'])
        print("WiFi connected successfully!")
        HOST = repr(wifi.radio.ipv4_address)
        PORT = 80  # Port to listen on
        print(f"Host: {HOST}, Port: {PORT}")
    except Exception as e:
        print(f"Failed to connect to WiFi: {e}")
        raise

# Disable automatic reloading when files are written to the Pico
supervisor.runtime.autoreload = False

# Initialize the LED based on the board type
if board.board_id in ['raspberry_pi_pico', 'raspberry_pi_pico2']:
    led = pwmio.PWMOut(board.LED, frequency=5000, duty_cycle=0)
elif board.board_id in ['raspberry_pi_pico_w', 'raspberry_pi_pico2_w']:
    led = digitalio.DigitalInOut(board.LED)
    led.switch_to_output()
else:
    raise RuntimeError("Unsupported board type!")

# Check programming status and execute payload if not in setup mode
progStatus = getProgrammingStatus()
print("Programming Status:", progStatus)
if not progStatus:
    print("Finding payload...")
    payload = selectPayload()
    print(f"Running payload: {payload}")
    runScript(payload)
    print("Payload execution completed.")
else:
    print("Update your payload.")

# LED state for blinking
led_state = False

async def main_loop():
    """Main asynchronous loop for handling tasks."""
    global led

    # Create tasks for button monitoring and LED blinking
    button_task = asyncio.create_task(monitor_buttons(button1))
    if board.board_id in ['raspberry_pi_pico_w', 'raspberry_pi_pico2_w']:
        pico_led_task = asyncio.create_task(blink_pico_w_led(led))
        print("Starting WiFi...")
        startWiFi()
        print("Starting Web Service...")
        webservice_task = asyncio.create_task(startWebService())
        await asyncio.gather(pico_led_task, button_task, webservice_task)
    else:
        pico_led_task = asyncio.create_task(blink_pico_led(led))
        await asyncio.gather(pico_led_task, button_task)

# Run the main loop
asyncio.run(main_loop())