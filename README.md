<pre>
  
    ______     __          _______     __  _______ ____       ____             __ __     
   / ____/____/ /_  ____  / ____(_)   / / / / ___// __ )     / __ \__  _______/ //_/_  __
  / __/ / ___/ __ \/ __ \/ /_  / /   / / / /\__ \/ __  |    / / / / / / / ___/ ,< / / / /
 / /___/ /__/ / / / /_/ / __/ / /   / /_/ /___/ / /_/ /    / /_/ / /_/ / /__/ /| / /_/ / 
/_____/\___/_/ /_/\____/_/   /_/____\____//____/_____/____/_____/\__,_/\___/_/ |_\__, /  
                              /_____/               /_____/                     /____/   
                                                           BY Mr.EchoFi
  
</pre>
<div align="center">


  <img src="https://github.com/MrEchoFi/MrEchoFi/raw/4274f537dec313ac7dde4403fe0fae24259beade/Mr.EchoFi-New-Logo-with-ASCII.jpg" alt="logo" width="240" height="auto" />
  <h1>EchoFi_USB_Ducky</h1>
   
  <p>
   A RED TEAM' rubber ducky USB . By this USB u can inject malicious script or install malware in any pc or laptop but in lab environment or authorization.
  </p>


  📫 How to reach me **http://mrechofi.github.io/Tanjib_portfolio_website/** & **tanjibisham777@gmail.com & tanjibisham888@gmail.com**
 

  # Video for better understanding:
      


https://github.com/user-attachments/assets/cd121eb3-d878-4adc-9a55-2955d7ad4e8c



</div>

# Photo: 
   ![photo_2025-05-27_18-22-54](https://github.com/user-attachments/assets/3f260481-e638-4f2d-a8b8-1eeeb88fa713)



# Components:
  Pi pico, Pi pico W, Pi pico 2, Pi pico2 W
# Installation Process:
  1. Clone the repo.
  2. Download https://circuitpython.org/board/raspberry_pi_pico/
  3. Download CircuitPython for the Raspberry Pi Pico W https://circuitpython.org/board/raspberry_pi_pico_w/ & Download CircuitPython for the Raspberry Pi Pico 2 https://circuitpython.org/board/raspberry_pi_pico2/
  4. Download CircuitPython for the Raspberry Pi Pico 2W https://circuitpython.org/board/raspberry_pi_pico2_w/
  5. Plug the device into a USB port while holding the boot button. It will show up as a removable media device named RPI-RP2.
  6. Copy the downloaded .uf2 file[ u have downloaded the CircuitPython for the Raspberry Pi Pic etc] to the root of the Pico (RPI-RP2). The device will reboot and after a second or so, it will reconnect as CIRCUITPY.
  7. Download adafruit-circuitpython-bundle-9.x-mpy-YYYYMMDD.zip https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20250523/adafruit-circuitpython-bundle-10.x-mpy-20250523.zip and extract it outside the device.
  8. Navigate to lib in the recently extracted folder and copy adafruit_hid to the lib folder on your Raspberry Pi Pico2 or others.
  9. Copy asyncio to the lib folder on your Pico.
  10. Copy adafruit_wsgi to the lib folder on your Pico then copy boot.py from your clone to the root of your Pico.
  11. Copy EchoFi_USB.py, code.py, webapp.py, wsgiserver.py to the root folder of the Pico or others board.
  12. For Pico W Only Create the file secrets.py in the root of the Pico W. This contains the AP name and password to be created by the Pico W.
      As this, secrets = { 'ssid' : "BadAPName", 'password' : "badpassword" }
 13. BTW in payload.dd i have input a ducky script for example. if u need ducky script guid for penetration testing then knock me --> tanjibisham888@gmail.com or, tanjibisham777@gmail.com
 14. Now u can run the EchoFi_USB_Rubber_Ducky by saving the files.

     
