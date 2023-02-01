# import required libraries
from vidgear.gears import NetGear
from vidgear.gears import WriteGear
from time import strftime
import cv2

# Define NetGear Client at given IP address and define parameters 
client = NetGear(
    address="127.0.0.1", # don't change this
    port="5454",
    pattern=1,
    receive_mode=True,
    logging=True,
)

writer = WriteGear(output="{}.mp4".format(strftime("%Y%m%d_%H%M%S")))

# loop over
while True:
    # receive frames from network
    frame = client.recv()

    # check for received frame if Nonetype
    if frame is None:
        break

    # {do something with the frame here}

    # Show output window
    cv2.imshow("Output Frame", frame)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# safely close client
client.close()