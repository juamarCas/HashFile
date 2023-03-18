import configparser
import argparse
import hashlib
import dbus
import dbus.service
import asyncio, aiofiles
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop
import json
import os
import datetime

result = {
    'token': '',
    'codigoerror': 0,
    'mensajeerror': ''
}

class DBusService(dbus.service.Object):

    def __init__(self, maximoactivas, log_file_path):

        self.maximoactivas = maximoactivas
        self.solicitudesactivas = 0
        self.log_file_path = log_file_path

        self.hashMethodsDictionary = {
            'sha1'   : hashlib.sha1,
            'sha224' : hashlib.sha224,
            'sha256' : hashlib.sha256,
            'sha384' : hashlib.sha384,
            'sha512' : hashlib.sha512,
            'blake2b': hashlib.blake2b,
            'blake2s': hashlib.blake2s,
            'md5'    : hashlib.md5
        }

        bus_name = dbus.service.BusName(
            "com.monitoreointeligente.retotecnico", bus=dbus.SessionBus()
        )

        dbus.service.Object.__init__(self, bus_name, "/com/monitoreointeligente/retotecnico")

    @dbus.service.method(
            "com.monitoreointeligente.retotecnico", in_signature="", out_signature="q"
    )
    def SolicitudesActivas(self):
        return self.solicitudesactivas
    
    @dbus.service.method(
            "com.monitoreointeligente.retotecnico", in_signature="", out_signature="q"
    )
    def MaximoSolicitudes(self):
        return self.maximoactivas
    
    @dbus.service.method(
            "com.monitoreointeligente.retotecnico", in_signature="q", out_signature=""
    )
    def SetMaximoSolicitudes(self, value):
        self.maximoactivas = value


    async def Operation(self, path, type):
        """
        Transform a file into a hashed hex string
        :param path: path to the file
        :param type: type of hashing
        :return: result object with the corresponding values
        """
        try:
            async with aiofiles.open(path, mode='r') as f:
                contents = await f.read() 
                content_bytes = contents.encode('utf-8')
                hashMethod = self.hashMethodsDictionary[type]()
                hashMethod.update(content_bytes)
                result['codigoerror'] = 0
                result['mensajeerror'] = ""
                result['token'] = hashMethod.hexdigest()

        except FileNotFoundError:
            result['codigoerror'] = 3
            result['mensajeerror'] = "File not found"
            result['token'] = ''

        return result


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

        if type not in self.hashMethodsDictionary:
            result['token']        = ""
            result['mensajeerror'] = "Not valid hash type"
            result['codigoerror']  = 1
            return json.dumps(result)
       

        if self.solicitudesactivas >= self.maximoactivas:
            result['token']        = ""
            result['mensajeerror'] = "The maximum number of processes has been reached"
            result['codigoerror']  = 2
            return json.dumps(result)
        
        self.solicitudesactivas += 1
            
        
        asyncio.run(self.Operation(path, type))
        self.terminado(result['token'], result['codigoerror'], result['mensajeerror'], "res")
        self.solicitudesactivas -= 1
        asyncio.run(self.print_to_log(result))
        return json.dumps(result)

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

    async def print_to_log(self, result):
        """
        Writes the provided result to the log file with the current timestamp.

        :param result: a dictionary containing the token, error code, and error message
        """
        async with aiofiles.open(self.log_file_path, mode='a') as f:
            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime("%d-%m-%Y %H:%M")
            contents = await f.write(
                f"{formatted_time}:\n"
                f"\ttoken: {result['token']}\n"
                f"\tcodigo error: {str(result['codigoerror'])}\n"
                f"\tmensaje error: {result['mensajeerror']}\n"
            )
            
  

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="path to the ini file")
    parser.add_argument('--input_file', 
                        type=str, help="path to the init file")

    args = parser.parse_args()
    if not args.input_file:
        parser.error("You have not set any file path")
    
    if not os.path.isfile(args.input_file):
        raise FileNotFoundError(f"file not found. Please check the file path and try again.")

    config_file = configparser.ConfigParser()

    config_file.read(args.input_file)
    
    maximo_activas_str = config_file["config"]["maximoactivas"]
    logfile_path  = config_file['config']["logfile_path"]

    if not logfile_path:
        parser.error("You have not set any file path")

    maximo_activas = 0
    try:
        maximo_activas = int(maximo_activas_str)
    except ValueError:
        print("Error: not a valid integer number")
        exit()


    DBusGMainLoop(set_as_default=True)
   
    myService = DBusService(maximoactivas=maximo_activas, log_file_path=logfile_path)
    GLib.MainLoop().run()
