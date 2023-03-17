import configparser
import argparse
import hashlib
import dbus
import dbus.service
import asyncio
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop



class DBusService(dbus.service.Object):

    def __init__(self):
        bus_name = dbus.service.BusName(
            "com.monitoreointeligente.retotecnico", bus=dbus.SessionBus()
        )

        dbus.service.Object.__init__(self, bus_name, "/com/monitoreointeligente/retotecnico")

    async def Operation(self, path, type):
        with open(path, "a") as file:
            file.write("you have called me" + "\n")


    @dbus.service.method(
        "com.monitoreointeligente.retotecnico", in_signature="ss", out_signature="s"
    )
    def calcular(self, path, type):
        """
        Calculates checksum
        :param path: path to the file that will be the checksum applied
        :param type: type of hashcode will be implemented
        :return: result of the hash operation
        """
        asyncio.run(self.Operation(path, type))
        self.terminado("adqwda", 0, "message", "res")
        return type

    @dbus.service.signal("com.monitoreointeligente.retotecnico", signature="suss")
    def terminado(self, token, code, errorMessage, result):
        """
        Signal called at the end of the operation
        :param token: string token of the value 
        :param code: an error code value.
        :param errorMessage: an error message  string detailing the error code.
        :param result: a result string.
        """
        pass


DBusGMainLoop(set_as_default=True)
myService = DBusService()

GLib.MainLoop().run()
