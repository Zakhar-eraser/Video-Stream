# import required libraries
from vidgear.gears import NetGear
from vidgear.gears import CamGear

def run():
    # Open live video stream on webcam at first index(i.e. 0) device
    cam_opts = {"CAP_PROP_FPS": 30}
    stream = CamGear(source=6, **cam_opts).start()

    # Define NetGear server at given IP address and define parameters
    net_opts = {"jpeg_compression": True, "jpeg_compression_quality": 10}
    server = NetGear(
        address="10.8.0.1",
        port="5454",
        pattern=1,
        logging=True,
        **net_opts
    )

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
