import unittest
import json
import dbus
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

#test if the validator is working correctly
def test_invalid_hash_type_calcular() -> None:
    path = "../HashFile.py"
    hashtype = "invalid"
 
    result = iface.calcular(path, hashtype)
    data = json.loads(result)

    assert data['codigoerror'] == 1
    

#test if the validator is working correctly
def test_valid_hash_type_calcular() -> None:
    #change the path to some valid path in your system
    path = "/home/config.ini"
    hashtype = "md5"
 
    result = iface.calcular(path, hashtype)
    data = json.loads(result)
    print(result)
    assert data['codigoerror'] == 0
    

  
INTERFACE = "com.monitoreointeligente.retotecnico"
OBJ_PATH  = "/com/monitoreointeligente/retotecnico"
BUS_NAME  = "com.monitoreointeligente.retotecnico"

def handle_signal(token, code, message, result):
    print("res token: ", token)

def loop_init():
    print("hello")
    bus.add_signal_receiver(handle_signal, 
                            dbus_interface=INTERFACE,
                            signal_name="terminado")
    path = "/home/juanmartin/Desktop/test.txt"
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
   
    