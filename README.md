# Hash File
This project is part of the technical test for "monitoreointeligente".</br>
It is a Dbus service sunning as a systemd service in the background that calculates the checksum of a given file.

## Core files
The main application script is located in the following directory:
```
debian->hashfile->usr->bin->HashFile.py
```

The service file is located in the following directory:
```
debian->hashfile->etc->systemd->system->hashService.service
```

## How to build it:
* Download the files, in case the name of the root directory is giving problems, change it to "hashfile"

* install the following packages
```
apt install python3-setuptools
apt install python3-all
apt install dh-python
apt install devscripts debhelper
apt install debhelp-compat
```
* run the setup file
```
python3 setup.py sdist
```

*lastly run the build command
```
debuild -us -uc -sa -i -I -b --changes-option="-DDistribution=focal" -d -p../dist/*
```
The deb packages will be located in the root directory  where the project is located.

## Build it using docker
* using the dockerfile, build an image first with the following command:
```
docker build -t <image_name>:<tag> .
```
* Excecute the container, it will automatically build the package and save it in a desired location
```
socker run --name <container_name> -v /output/path/of/my/machine:/build/package <image_name>:<tag>
```
Note, that only the output path and names should be modified. After running it, all the .deb packages will be in the ouput path

# installing
* before installing the service, it needs the following package:
```
apt install python3-aiofiles
```

* Install the .deb package
* before enabling the service, createa config file in /home directory. This is an example config file:
```
[config]
maximoactivas = 5
logfile_path  = /home/user/Desktop/log.txt
```

* Enable the service
```
systemctl enable hashService
```

* Reload the systemd daemon
```
systemctl daemon-reload
```

* Start the service
```
systemctl start hashService
```
To test the service you can create a client and test its functionality. This is an example client:
```python
import dbus
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

INTERFACE = "com.monitoreointeligente.retotecnico"
OBJ_PATH  = "/com/monitoreointeligente/retotecnico"
BUS_NAME  = "com.monitoreointeligente.retotecnico"
def handle_signal(token, code, message, result):
    print("res token: ", token)

def loop_init():
    bus.add_signal_receiver(handle_signal, 
                            dbus_interface=INTERFACE,
                            signal_name="terminado")
    path = "/home/user/Desktop/test.txt"
    message = iface.calcular(path, "md5")
    print(message)

DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
obj = bus.get_object(BUS_NAME ,OBJ_PATH)
iface = dbus.Interface(obj, dbus_interface=INTERFACE)

if __name__ == '__main__':
    GLib.idle_add(loop_init)
    GLib.MainLoop().run()   
    #iface.connect_to_signal("terminado", handle_signal)

```

this client will send a path to a file and print the checksum. </br>
Tests are also available in the Testing folder: 
```
debian->hashfile->usr->bin->testing
```
