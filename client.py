#!/usr/bin/env python

# This is client.py file
from scipy.misc import imread, imresize, imsave, imshow
import socket               # Import socket module

import numpy as np

end_from_server = 'MyEnd'.encode()
def recv_end(the_socket):
    total_data = []
    i = 1
    while True:
            cur_data = the_socket.recv(8192)
            #print(type(cur_data))
            if end_from_server in cur_data:
                total_data.append(cur_data[:cur_data.find(end_from_server)])
                break
            total_data.append(cur_data)
            if len(total_data) > 1:
                # check if end_of_data was split
                last_pair = total_data[-2] + total_data[-1]
                if end_from_server in last_pair:
                    total_data[-2] = last_pair[:last_pair.find(end_from_server)]
                    total_data.pop()
                    break
            print('reading until end.... %d' % i)
            i += 1
    return b''.join(total_data)

s = socket.socket()         # Create a socket object
#host = socket.gethostname() # Get local machine name
host = "graphic02.doc.ic.ac.uk"
port = 12348                # Reserve a port for your service.

s.connect((host, port))
end = 'MyEnd'

while True:
    print("Enter input (type exit to quit): ", end='')
    in_msg = input()
    # s.sendall(in_msg.encode())
    # suppose msg is file path, read this file and send bytes
    if in_msg != "exit":
        msg = imread(in_msg)
        # msg = imresize(msg, (224, 224))
        msg = msg.tostring()
        print('encoded image to string message')
    else:  #
        msg = in_msg.encode()
        print('cliean type exit -> quit program')
        print('sending message with end-symbole')
        s.sendall(msg + end.encode())
        break

    print('sending message with end-symbole')
    s.sendall(msg + end.encode())

    # reply_from_server = s.recv(1024).decode()
    try:
        reply_from_server = recv_end(s)
        res_img = np.fromstring(reply_from_server, dtype=np.uint8)
        print(res_img.shape)
        res_img = res_img.reshape(264, 352, 3)
        imsave('cur_res_img.JPEG', res_img)
        # imshow(res_img)
    # print()
    except Exception as e:
        print('reading error:', e)

    # print("server predicts: %s" % reply_from_server)
    # if reply_from_server == "bye":
    #     break
