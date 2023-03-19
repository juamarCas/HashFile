FROM debian:11

ENV DEBIAN_FRONTEND noninteractive

LABEL made_by = Juan Martin
LABEL description = "Technical test for monitoreointeligente, \n" \
                    "it builds a debian package for the hashfile application"

RUN apt update -y && \
    apt upgrade -y && \
    apt install -y python3 && \
    apt clean

RUN apt install -y python3-setuptools
RUN apt install -y devscripts debhelper dh-python
RUN apt install -y python3-aiofiles
RUN apt install -y python3-all

#for some reason, debhelper-compat is up to version 12, version 13 is needed, and can't be updated
#so install it manually
RUN curl -o package.deb http://ftp.de.debian.org/debian/pool/main/d/debhelper/debhelper_13.3.4_all.deb
RUN dpkg -i package.deb

RUN mkdir -p /build/package/

WORKDIR /build/hashfile

COPY ./ ./

RUN chmod +x debian/rules

RUN python3 setup.py sdist

RUN debuild -us -uc -sa -i -I -b --changes-option="-DDistribution=focal" -d -p../dist/*

WORKDIR /build/

CMD find ./ -maxdepth 1 -type f -exec cp {} ./package/ \;
