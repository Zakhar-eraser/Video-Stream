# import required libraries
from vidgear.gears import NetGear
from vidgear.gears import WriteGear
from time import strftime
import cv2

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
running = True
while running:
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
        cv2.namedWindow("Output Frame")
        cv2.moveWindow("Output Frame", 0, 0)
        cv2.imshow("Output Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            raise KeyboardInterrupt()
        writer.write(frame)
    except KeyboardInterrupt:
        running = False
        if writer is not None: writer.close()
        if client is not None: client.close()
    
    cv2.destroyAllWindows()
