import ender3serial as printer
from flask import Flask, jsonify, request, abort
import atexit
import os

app = Flask(__name__)

@app.route('/api/1.0/', methods=['GET'])
def getTemp():
    json = {
    "nozzleTemp": printer.nozzleTemp,
    "bedTemp": printer.bedTemp,
    "position": {
        'x' : printer.xpos, 
        'y' : printer.ypos,
        'z' : printer.zpos
    }
    }
    return jsonify(json)

@app.route('/api/1.0/', methods=['POST'])
def sendCommand():    
    if not request.json or not 'command' in request.json:
        abort(400)

    printer.sendCommand(printer.ser, request.json['command'].encode())
    return jsonify({'status': "Success"}), 201
    
@app.route('/api/1.0/uploadfile/', methods=['POST'])
def uploadFile():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(os.path.join('/home/pi/code/todo', uploaded_file.filename))
        #print("I would be printing %s" % uploaded_file.filename)
        os.system("python2 ender3serial.py")
        
        return jsonify({'status': "Success"}), 201
    
def closeSerialOnExit():
    printer.ser.close()

atexit.register(closeSerialOnExit)
    
if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)

