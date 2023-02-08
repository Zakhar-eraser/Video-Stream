# import required libraries
from vidgear.gears import NetGear
from vidgear.gears import CamGear
import sys
import asyncio

def run():
    # Open live video stream on webcam at first index(i.e. 0) device
    stream = CamGear(source=0).start()

    # Define NetGear server at given IP address and define parameters
    server = NetGear(
        address="127.0.0.1", # don't change this
        port="5454",
        pattern=2,
        logging=True,
        ssh_tunnel_mode="root@78.140.241.126",
        ssh_tunnel_keyfile="C:/Users/79922/.ssh/id_rsa"
    )

    #asyncio.set_event_loop(server.loop)
    #try:
    #    server.loop.run_until_complete(server.task)
    #except (KeyboardInterrupt, SystemExit):
    #    server.close()

    # loop over until KeyBoard Interrupted
    while True:
        try:
            # read frames from stream
            frame = stream.read()

            # check for frame if Nonetype
            if frame is None:
                break
            # send frame to server
            server.send(frame)

        except KeyboardInterrupt:
            server.close()
            stream.stop()
            break


if __name__ == '__main__':
    run()