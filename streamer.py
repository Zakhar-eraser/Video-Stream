# import required libraries
from vidgear.gears import CamGear
from vidgear.gears import NetGear
import sys

def run():
    ssh_con = "root@78.140.241.126"

    if len(sys.argv) > 1:
        ssh_con = sys.argv[1]
    else:
        print(ssh_con + " used")

    options = {
        "ssh_tunnel_mode": ssh_con, # defaults to port 22
        "ssh_tunnel_keyfile":'C:/Users/79922/.ssh/id_rsa',
    }

    # Open live video stream on webcam at first index(i.e. 0) device
    stream = CamGear(source=0).start()

    # Define NetGear server at given IP address and define parameters
    server = NetGear(
        address="127.0.0.1", # don't change this
        port="5454",
        pattern=2,
        logging=True,
        **options
    )

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