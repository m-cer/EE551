from flask import Flask, render_template, request, Response
from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory
from PIL import Image
#camera_opencv from Miguel Grinberg's
# flask-video-stream repo
from camera_opencv import Camera

import numpy as np
import time
import atexit
import io


from TB6612FNG import TB6612FNG
from heading import heading
from overlay import compass, system_stats

Device.pin_factory = PiGPIOFactory()

app = Flask(__name__)


A = TB6612FNG(output_one = 'GPIO27', output_two = 'GPIO17', pwm = 'GPIO12')
B = TB6612FNG(output_one = 'GPIO5', output_two = 'GPIO6', pwm = 'GPIO13')

def turnOffMotors():
  A.stop()
  B.stop()

atexit.register(turnOffMotors)

@app.route("/")
def web_interface():
  html = open("templates/index.html")
  response = html.read().replace('\n', '')
  html.close()
  return render_template('index.html')

@app.route("/set_speedA")
def set_speedA():
  speed = request.args.get("speed")
  print("Received " + str(speed))
  A.value = float(speed)
  return "Received " + str(speed)

@app.route("/set_speedB")
def set_speedB():
  speed = request.args.get("speed")
  print("Received " + str(speed))
  B.value = float(speed)
  return "Received " + str(speed)

def gen(camera):
    """Video streaming generator function."""
    hd = heading()
    com = compass()
    stats = system_stats()
    buf = io.BytesIO()
    while True:
        frame = camera.get_frame()
        
        #modify byte stream
        theta = hd.get()
        image = Image.open(io.BytesIO(frame))
        image = stats.overlay(image)
        out = com.overlay(image, theta)
        buf.seek(0)
        out.save(buf, 'JPEG')
        buf.seek(0)
        frame = buf.getvalue()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def main():
  app.run(host='0.0.0.0', threaded=True)

main()
