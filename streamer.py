# import required libraries
from vidgear.gears import VideoGear
from vidgear.gears import NetGear
import sys

ssh_con = "test@127.0.0.1:22"

if len(sys.argc) > 1:
    ssh_con = sys.argv[1]
else:
    print("[HOSTNAME]@[ADDRESS]:[PORT]")
    ssh_con = input()

# activate SSH tunneling with SSH URL, and
# [BEWARE!!!] Change SSH URL and SSH password with yours for this example !!!
options = {
    "ssh_tunnel_mode": ssh_con, # defaults to port 22
    "ssh_tunnel_keyfile":"~/.ssh/id_rsa",
}

# Open live video stream on webcam at first index(i.e. 0) device
stream = VideoGear(source=0).start()

# Define NetGear server at given IP address and define parameters
server = NetGear(
    address="127.0.0.1", # don't change this
    port="5454",
    pattern=1, 
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

        # {do something with the frame here}

        # send frame to server
        server.send(frame)

    except KeyboardInterrupt:
        break

# safely close video stream
stream.stop()

# safely close server
server.close()