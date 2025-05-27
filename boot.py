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

import board
import digitalio
import storage

# Constants for board IDs
PICO_BOARD_IDS = {'raspberry_pi_pico', 'raspberry_pi_pico2'}
PICO_W_BOARD_IDS = {'raspberry_pi_pico_w', 'raspberry_pi_pico2_w'}

# Initialize the noStoragePin (GP15)
noStoragePin = digitalio.DigitalInOut(board.GP15)
noStoragePin.switch_to_input(pull=digitalio.Pull.UP)
noStorageStatus = noStoragePin.value

# Determine USB visibility based on board type and GP15 status
noStorage = False
if board.board_id in PICO_BOARD_IDS:
    # On Pi Pico, default to USB visible
    noStorage = not noStorageStatus
elif board.board_id in PICO_W_BOARD_IDS:
    # On Pi Pico W, default to USB hidden
    noStorage = noStorageStatus
else:
    # Handle unexpected board IDs
    raise ValueError(f"Unsupported board ID: {board.board_id}")

# Configure USB drive visibility
if noStorage:
    # Don't show USB drive to host PC
    storage.disable_usb_drive()
    print("Disabling USB drive")
else:
    # Normal boot
    print("USB drive enabled")
