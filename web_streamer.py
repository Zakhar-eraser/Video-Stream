from vidgear.gears import NetGear
from vidgear.gears.asyncio import WebGear
import asyncio
import uvicorn
import cv2

client = NetGear(
    address="10.8.0.1",
    port=5454,
    receive_mode=True,
    pattern=1,
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
        else:
            break

def main():
    # initialize WebGear app without any source
    options = {"jpeg_compression_quality": 10, "frame_size_reduction": 10}
    web = WebGear(logging=True, enable_infinite_frames = True, **options)
    web.config["generator"] = my_frame_producer

    uvicorn.run(web(), host="10.8.0.1", port=8000)

    # safely close client
    client.close()

    # close app safely
    web.shutdown()

if __name__ == '__main__':
    main()