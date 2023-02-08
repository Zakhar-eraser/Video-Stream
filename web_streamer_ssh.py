from vidgear.gears import NetGear
from vidgear.gears.asyncio import WebGear
from vidgear.gears.asyncio.helper import reducer
import asyncio
import uvicorn
import cv2

client = NetGear(
    address="127.0.0.1",
    port=5454,
    receive_mode=True,
    pattern=2,
    logging=True
)

async def my_frame_producer():
    while True:
        frame = client.recv()
        if frame is not None:
            encodedImage = cv2.imencode(".jpg", frame)[1].tobytes()
            # yield frame in byte format
            yield (b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + encodedImage + b"\r\n")
            await asyncio.sleep(0)

def main():
    # initialize WebGear app without any source
    web = WebGear(logging=True, enable_infinite_frames = True)

    # add your custom frame producer to config with adequate IP address
    web.config["generator"] = my_frame_producer

    # run this app on Uvicorn server at address http://localhost:8000/
    uvicorn.run(web(), host="78.140.241.126", port=8000)

    # safely close client
    client.close()

    # close app safely
    web.shutdown()

if __name__ == '__main__':
    main()