import asyncio
import json
import assemblyai
import twilio
import websockets

from flask import Flask, request, Response
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from twilio import twiml
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather, Say, Dial, Play


def main():
    assembly = None
    chunks = []


async def connection(websockets, path):
    print("New Connection Initiated")
    # You can add more logic here to handle messages from the client or other tasks


start_server = websockets.serve(connection, "localhost", 8090)  # You can change the host and port as needed

#asyncio.get_event_loop().run_until_complete(start_server)

assembly = None


async def handler(websocket, path):
    async for message in websocket:
        if not assembly:
            print("AssemblyAI's WebSocket must be initialized.")
            return


async def handler(websocket, path):
    message = await websocket.recv()
    msg = json.loads(message)

    if msg["event"] == "connected":
        print("A new call has connected.")

        texts = {}

        async def assembly_message_handler(assembly_msg, connected_clients=None):
            res = json.loads(assembly_msg.data)
            texts[res["audio_start"]] = res["text"]
            keys = sorted(texts.keys())
            msg_text = ' '.join([texts[key] for key in keys if texts[key]])
            print(msg_text)

            # Send the message to all connected clients
            for client in connected_clients:  # You need to maintain a list of connected clients
                if client.open:
                    await client.send(json.dumps({
                        "event": "interim-transcription",
                        "text": msg_text
                    }))
                else:
                    break

            if event == "start":
                stream_sid = msg.get('streamSid')
                if stream_sid:
                    print(f"Starting Media Stream {stream_sid}")
                    assembly = assemblyai.Client(token)
                else:
                    print("streamSid not found in msg")



def index():
    assembly_url = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=8000"
    headers = {
        "authorization": "my key"
    }
    assembly = websocket.create_connection(assembly_url, header=headers)

    response_content = """
    <Response>
        <Start>
            <Stream url='wss://{}' />
        </Start>
        <Say>
            Start speaking to see your audio transcribed in the console
        </Say>
        <Pause length='30' />
    </Response>
    """.format(request.headers['host'])

    response = Response(response_content, content_type="text/xml")
    return response

app = Flask(__name__)


@app.route('/')
def index():
    return "Program is running"


if __name__ == '__main__':
    http_server = WSGIServer(('', 8090), app, handler_class=WebSocketHandler)
    app.run(port=8020)

print('all good')
