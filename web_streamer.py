from vidgear.gears.asyncio import NetGear_Async
from vidgear.gears.asyncio import WebGear
from vidgear.gears.asyncio.helper import reducer
import asyncio, cv2

import uvicorn

client = NetGear_Async(
    address="78.140.241.126",
    port=80,
    receive_mode=True,
    pattern=1,
    logging=True
).launch()

async def my_frame_producer():

    async for frame in client.recv_generator():

        frame = await reducer(
            frame, percentage=50, interpolation=cv2.INTER_AREA
        )  # reduce frame by 30%

        # handle JPEG encoding
        encodedImage = cv2.imencode(".jpg", frame)[1].tobytes()
        # yield frame in byte format
        yield (b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + encodedImage + b"\r\n")
        await asyncio.sleep(0)

def main():
    asyncio.set_event_loop(client.loop)

    # initialize WebGear app without any source
    web = WebGear(logging=True, enable_infinite_frames = True)

    # add your custom frame producer to config with adequate IP address
    web.config["generator"] = my_frame_producer

    # run this app on Uvicorn server at address http://localhost:8000/
    uvicorn.run(web(), host="0.0.0.0", port=8000)

    # safely close client
    client.close()

    # close app safely
    web.shutdown()

if __name__ == '__main__':
    main()