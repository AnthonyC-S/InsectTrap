# Initial Setup of Raspberry Pi Environment

Start with a new/fresh Raspberry Pi OS image to the SD card. Our device used Raspberry Pi 4 OS (64-bit) and was loaded onto the SD card with Raspberry Pi Imager, https://www.raspberrypi.com/software/.

Follow instructions to set up Raspberry Pi and connect to the internet. Our device used default initial settings., https://www.raspberrypi.com/documentation/computers/getting-started.html.

Open the terminal / command shell to update packages.

    sudo apt update
    sudo apt upgrade

Install git package.

    sudo apt install git
    git --version

Install webdriver and check location.

    sudo apt install chromium-chromedriver
    whereis chromedriver

Download InsectTrap code in the directory of your choice, e.g. /home/pi.

    git clone https://github.com/anthonynic28/InsectTrap.git

Install Pyenv, https://github.com/pyenv/pyenv, for the Insect Trap virtual environment.

    curl https://pyenv.run | bash

Set up your shell environment for Pyenv.

    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc

Restart shell.

    exec $SHELL

Install Python dependencies.

    sudo apt install --yes libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libgdbm-dev lzma lzma-dev tcl-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev wget curl make build-essential openssl

Update Pyenv package.

    pyenv update

Install python 3.11.2 to Pyenv.

    pyenv install 3.11.2

Create a new virtual environment with Python 3.11.2 within the InsectTrap folder you cloned from git.

    cd InsectTrap
    pyenv virtualenv 3.11.2 insect-venv

Activate the new virtual environment.

    source .insect-venv/bin/activate

Update pip package while insect-venv is active.

    python -m pip install --upgrade pip

Install InsectTrap dependencies, modify path to requirements.txt if necessary.

    python -m pip install -r /home/pi/InsectTrap/requirements.txt

Start pigpio daemon to control servo motors before running Python script.

    sudo pigpio

All necessary packages should be installed and InsectTrap can be initialized with auto mode off. Note, it will be necessary to add your own username and password in the Get_Classification.py script to the variables: username and password.

    python InsectTrapProject/main.py --autoOFF
