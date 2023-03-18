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


