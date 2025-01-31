
import socket

def init(address):
    try:
        """ Open the socket at the specified address, call the command sent and return data """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(address)
    except socket.timeout:
        raise socket.timeout(socket.timeout)
    except socket.error:
        raise socket.error(socket.error)
    finally:
        sock.close()

def read(address, circuit, name, type, ttl):
    result = None
    try:
        """ Open the socket at the specified address, call the command sent and return data """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(address)
        """ Send the command """
        READ_COMMAND = 'read -m {2} -c {0} {1}\n'
        command = READ_COMMAND.format(circuit, name, ttl)
        sock.sendall(command.encode())
        """ Get the result decoded UTF-8 """
        decoded = sock.recv(256).decode('utf-8').rstrip()
        if 'ERR:' not in decoded:
            result = humanize(type, decoded)
    except socket.timeout:
        raise RuntimeError(socket.timeout)
    except socket.error:
        raise RuntimeError(socket.error)
    finally:
        sock.close()
    return result

def write(address, circuit, name, value):
    result = None
    try:
        """ Open the socket at the specified address, call the command sent and return data """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(address)
        """ Send the command """
        WRITE_COMMAND = 'write -c {0} {1} {2}\n'
        command = WRITE_COMMAND.format(circuit, name, value)
        sock.sendall(command.encode())
        """ Get the result decoded UTF-8 """
        result = sock.recv(256).decode('utf-8').rstrip()
    except socket.timeout:
        raise RuntimeError(socket.timeout)
    except socket.error:
        raise RuntimeError(socket.error)
    finally:
        sock.close()
    return result


def raw(address, command):
    result = None
    try:
        """ Open the socket at the specified address, call the command sent and return data """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(address)
        """ Send the command """
        sock.sendall((command + '\n').encode())
        """ Get the result decoded UTF-8 """
        result = sock.recv(256).decode('utf-8').rstrip()
    except socket.timeout:
        raise RuntimeError(socket.timeout)
    except socket.error:
        raise RuntimeError(socket.error)
    finally:
        sock.close()
    return result


def humanize(type, value):
    _state = None
    if type == 0:
        _state = format(
            float(value), '.1f')
    elif type == 1:
        _state = value.replace(';-:-', '')
    elif type == 2:
        """ This can be a value [0;1] or string ['off';'on'] """
        if isinstance(value, int):
            if value == 1:
                _state = 'on'
            else:
                _state = 'off'
        else:
            _state = value
    elif type == 3:
        _state = value
    elif type == 4:
        if 'ok' not in value.split(';'):
            return
        _state = value.partition(';')[0]
    return _state
