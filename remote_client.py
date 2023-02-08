# import required libraries
from vidgear.gears import NetGear
from vidgear.gears import WriteGear
from time import strftime    

def create_client(): 
    return NetGear(
        address="127.0.0.1", # don't change this
        port="5454",
        pattern=1,
        receive_mode=True,
        logging=True,
    )

writer = None
frame = None
client = None
while True:
    try:
        if client is None:
            client = create_client()
        frame = client.recv()
        if writer is None:
            writer = WriteGear(output="{}.mp4".format(strftime("%Y%m%d_%H%M%S")))

        # check for received frame if Nonetype
        if frame is None:
            writer.close()
            client.close()
            writer = None
            client = None
            continue

        writer.write(frame)
    except KeyboardInterrupt:
        if writer is not None: writer.close()
        if client is not None: client.close()
        break
