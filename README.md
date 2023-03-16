# Control 3x3 screen

## Installation guide

### Download required build tools
sudo apt install git make g++ python3-pip

### Clone rpi-rgb-led-matrix repo into ./lib dir
cd lib && git clone https://github.com/hzeller/rpi-rgb-led-matrix

### Build core
cd rpi-rgb-led-matrix && make all

### Install required python modules
sudo apt install python3-dev python3-pillow

### Build python binding
make build-python PYTHON=python3
sudo make install-python PYTHON=python3

### Install requirements.txt
cd ../../ && sudo pip install -r requirements.txt

### Run main.py
sudo python3 main.py

Also need to check if your rpi IP address matches than one in config/conf.yaml

# TO DO
- autocheck IP and write into conf.yaml
- full code refactoring
- use Flask instead of HTTPServer
- many more in the future