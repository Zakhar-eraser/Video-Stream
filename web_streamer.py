from vidgear.gears import NetGear
from vidgear.gears.asyncio import WebGear_RTC
from time import sleep
import uvicorn

class CustomStreamer:
    """Custom Streaming using frames recieved via SSH"""

    def __init__(self):
        self._client = None
        self._running = True
    
    def read(self):
        frame = None
        if self._running:
            while frame is None:
                print("(re)starting connection with streamer")
                sleep(3)
                self._client.close()
                self._client = self._create_client()
                frame = self._client.recv()
            
        return frame
            
    def _create_client():
        return NetGear(
            address="127.0.0.1",
            port="5454",
            pattern=1,
            receive_mode=True,
            logging=True,
        )
    
    def stop(self):
        self._running = False
        self._client.close()
        
def main():
    options = {
        "custom_stream": CustomStreamer()
    }
    web = WebGear_RTC(logging=True, **options)

    uvicorn.run(web(), host="0.0.0.0", port=8000)
    web.shutdown()

if __name__ == '__main__':
    main()