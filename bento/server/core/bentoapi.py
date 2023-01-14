"""
this file defines the bento api that is exposed to functions executed by clients.
    - want to allow functions to send data back to their clients, use the Stem library to extend their circuits, etc.
"""

import logging
import struct
import sys
import base64
import select


def send(data):
    """
    pack data len, append the actual data, and send to server
        - will be picked up by the dedicated exchange process for this function
    """
    if data is not None:#这里的数据类型经限于str和btype类型？
        if isinstance(data, str):
            datalen= struct.pack("Q", len(data.encode()))#这里加encode以适应中文字符串
            sys.stdout.buffer.write(datalen) 
            sys.stdout.write(data)
        else:
            datalen= struct.pack("Q", len(data))
            sys.stdout.buffer.write(datalen) 
            sys.stdout.buffer.write(data)
        sys.stdout.buffer.flush()
        sys.stdout.flush()
        return len(data)
    return 0
        

def recv():
    """
    recv data from the client through our pipe to the server 
    """
    bdata= sys.stdin.buffer.read(8) 
    datalen,= struct.unpack("Q", bdata) 
    data= sys.stdin.buffer.read(datalen)
    return data


def poll():
    """
    return whether there is data in the pipe
    """
    return sys.stdin.buffer in select.select([sys.stdin.buffer], [], [], 0)[0] 
    


# TODO write safe wrapper functions for performing Stem library functionality
# Stem accesses the tor controller which can view other clients streams/circuits so we want to prevent that type of stuff
