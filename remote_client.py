# import required libraries
from vidgear.gears import NetGear
from vidgear.gears import WriteGear
from time import strftime

# Define NetGear Client at given IP address and define parameters 
client = NetGear(
    address="127.0.0.1", # don't change this
    port="5454",
    pattern=1,
    receive_mode=True,
    logging=True,
)

writer = None
frame = None
# loop over
while True:
    try:
        # receive frames from network
        frame = client.recv()

        # check for received frame if Nonetype
        if frame is None:
            if writer is not None: writer.close()
            continue

        if writer is None:
            writer = WriteGear(output="{}.mp4".format(strftime("%Y%m%d_%H%M%S")))
        # {do something with the frame here}

        writer.write(frame)
    except KeyboardInterrupt:
        break


# safely close client
client.close()