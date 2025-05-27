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

import socketpool
import time
import os
import storage
import html
import asyncio

import wsgiserver as server
from adafruit_wsgi.wsgi_app import WSGIApp
import wifi

from EchoFi_USB import *

# HTML templates
payload_html = """<!DOCTYPE html>
<html>
    <head> <title>EchoFi_USB_PicoW</title> </head>
    <body> <h1>EchoFi_USB</h1>
        <table border="1"> <tr><th>Payload</th><th>Actions</th></tr> {} </table>
        <br>
        <a href="/new">New Script</a>
    </body>
</html>
"""

edit_html = """<!DOCTYPE html>
<html>
  <head>
    <title>Script Editor</title>
  </head>
  <body>
    <form action="/write/{}" method="POST">
      <textarea rows="5" cols="60" name="scriptData">{}</textarea>
      <br/>
      <input type="submit" value="submit"/>
    </form>
    <br>
    <a href="/ducky">Home</a>
  </body>
</html>
"""

new_html = """<!DOCTYPE html>
<html>
  <head>
    <title>New Script</title>
  </head>
  <body>
    <form action="/new" method="POST">
      Script Name<br>
      <textarea rows="1" cols="60" name="scriptName"></textarea>
      Script<br>
      <textarea rows="5" cols="60" name="scriptData"></textarea>
      <br/>
      <input type="submit" value="submit"/>
    </form>
    <br>
    <a href="/ducky">Home</a>
  </body>
</html>
"""

response_html = """<!DOCTYPE html>
<html>
    <head> <title>EchoFi_USB_PicoW</title> </head>
    <body> <h1>EchoFi_USB</h1>
        {}
        <br>
        <a href="/ducky">Home</a>
    </body>
</html>
"""

newrow_html = "<tr><td>{}</td><td><a href='/edit/{}'>Edit</a> / <a href='/run/{}'>Run</a></tr>"

# Utility functions
def setPayload(payload_number):
    return f"payload{payload_number}.dd" if payload_number != 1 else "payload.dd"

def cleanup_text(string):
    """Decode URL-encoded text."""
    if not string:
        return ''
    return html.unescape(string.replace('+', ' '))

# Web application
web_app = WSGIApp()

@web_app.route("/ducky")
def duck_main(request):
    response = ducky_main(request)
    return "200 OK", [('Content-Type', 'text/html')], response

def ducky_main(request):
    payloads = []
    rows = ""
    try:
        files = os.listdir()
        for f in files:
            if f.endswith('.dd'):
                payloads.append(f)
                rows += newrow_html.format(html.escape(f), html.escape(f), html.escape(f))
    except Exception as e:
        rows = f"<tr><td colspan='2'>Error: {html.escape(str(e))}</td></tr>"
    return payload_html.format(rows)

@web_app.route("/edit/<filename>")
def edit(request, filename):
    filename = html.escape(filename)
    try:
        with open(filename, "r", encoding='utf-8') as f:
            textbuffer = f.read()
        response = edit_html.format(filename, html.escape(textbuffer))
    except Exception as e:
        response = response_html.format(f"Error: {html.escape(str(e))}")
    return "200 OK", [('Content-Type', 'text/html')], response

@web_app.route("/write/<filename>", methods=["POST"])
def write_script(request, filename):
    filename = html.escape(filename)
    try:
        data = request.body.getvalue()
        fields = data.split("&")
        form_data = {key: cleanup_text(value) for key, value in (field.split('=') for field in fields)}
        storage.remount("/", readonly=False)
        with open(filename, "w", encoding='utf-8') as f:
            f.write(form_data['scriptData'])
        storage.remount("/", readonly=True)
        response = response_html.format(f"Wrote script {filename}")
    except Exception as e:
        response = response_html.format(f"Error: {html.escape(str(e))}")
    return "200 OK", [('Content-Type', 'text/html')], response

@web_app.route("/new", methods=['GET', 'POST'])
def write_new_script(request):
    if request.method == 'GET':
        return "200 OK", [('Content-Type', 'text/html')], new_html
    try:
        data = request.body.getvalue()
        fields = data.split("&")
        form_data = {key: cleanup_text(value) for key, value in (field.split('=') for field in fields)}
        filename = html.escape(form_data['scriptName'])
        storage.remount("/", readonly=False)
        with open(filename, "w", encoding='utf-8') as f:
            f.write(form_data['scriptData'])
        storage.remount("/", readonly=True)
        response = response_html.format(f"Wrote script {filename}")
    except Exception as e:
        response = response_html.format(f"Error: {html.escape(str(e))}")
    return "200 OK", [('Content-Type', 'text/html')], response

@web_app.route("/run/<filename>")
def run_script(request, filename):
    filename = html.escape(filename)
    try:
        runScript(filename)
        response = response_html.format(f"Running script {filename}")
    except Exception as e:
        response = response_html.format(f"Error: {html.escape(str(e))}")
    return "200 OK", [('Content-Type', 'text/html')], response

@web_app.route("/")
def index(request):
    response = ducky_main(request)
    return "200 OK", [('Content-Type', 'text/html')], response

@web_app.route("/api/run/<filenumber>")
def api_run_script(request, filenumber):
    try:
        filename = setPayload(int(filenumber))
        runScript(filename)
        response = response_html.format(f"Running script {filename}")
    except Exception as e:
        response = response_html.format(f"Error: {html.escape(str(e))}")
    return "200 OK", [('Content-Type', 'text/html')], response

async def startWebService():
    HOST = str(wifi.radio.ipv4_address_ap)
    PORT = 80
    print(f"open this IP in your browser: http://{HOST}:{PORT}/")
    wsgiServer = server.WSGIServer(PORT, application=web_app)
    wsgiServer.start()
    try:
        while True:
            wsgiServer.update_poll()
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        wsgiServer.stop()
