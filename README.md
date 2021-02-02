# One Click Print

Python code to turn any printer into a one click printer

## Installation

* Copy the contents of `backend` into `home/pi/code` on your pi.
* Open a terminal window and install flask with 
```bash
pip3 install Flask 
```

## Usage

* Plug you printer into the USB0 port
* Run `apiController.py`
* Find the local IP address of your pi
* Use the following api schema to control your printer

## API Schema
#### Get Position:
Method: `GET`\
Endpoint: `/api/1.0/`

#### Send Command:
Method: `POST`\
Endpoint: `/api/1.0/`\
JSON Body: ```{command: <GCODE Command to send>}```

#### Send File:
Method: `POST`\
Endpoint: `/api/1.0/uploadfile/`\
File Body: ```{file: <GCODE File to send>}```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to test thoroughly before submitting a pull request.

## Contributors
* [Toby Johnson]("https://github.com/fishbigger")

## License
[MIT](https://choosealicense.com/licenses/mit/)
