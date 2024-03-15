from dataclasses import dataclass, field
from fastapi import FastAPI, HTTPException, Response
import json

app = FastAPI()


@dataclass
class Channel:
    id: str
    name: str
    tags: list[str] = field(default_factory=list)
    description: str = ""


@app.get("/")
def read_root() -> Response:
    return Response("FastAPI is running")


channels: dict[str, Channel] = {}
with open("./db.json", encoding="utf8") as file:
    channels_raw = json.load(file)
    for channel_raw in channels_raw:
        channel = Channel(**channel_raw)
        channels[channel.id] = channel


@app.get("/channels/{channel_id}")
def read_channels(channel_id: str) -> Channel:
    if channel_id not in channels:
        raise HTTPException(status_code=404, detail="Channel not found")
    return channels[channel_id]
