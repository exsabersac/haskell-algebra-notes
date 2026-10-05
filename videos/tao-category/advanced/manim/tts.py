"""Generate narration audio per beat with edge-tts; write build/tts/<scene>.json with durations + sentence boundaries."""
import asyncio, json, os, subprocess, sys
import edge_tts
from content import SCENES, tts_text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "audio", "beats")
META = os.path.join(ROOT, "build", "tts")
VOICE = os.environ.get("VOICE", "zh-CN-YunxiNeural")
RATE = os.environ.get("RATE", "-6%")
os.makedirs(OUT, exist_ok=True); os.makedirs(META, exist_ok=True)


def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", path]).decode().strip())


async def one(sid, i, beat, sem):
    mp3 = os.path.join(OUT, f"{sid}_{i:02d}.mp3")
    wav = mp3[:-4] + ".wav"
    jpath = mp3[:-4] + ".json"
    text = tts_text(beat)
    if os.path.exists(jpath):
        j = json.load(open(jpath))
        if j.get("text") == text and j.get("voice") == VOICE and j.get("rate") == RATE and os.path.exists(wav):
            return j
    async with sem:
        for attempt in range(5):
            try:
                comm = edge_tts.Communicate(text, VOICE, rate=RATE)
                bounds = []
                with open(mp3, "wb") as f:
                    async for ch in comm.stream():
                        if ch["type"] == "audio":
                            f.write(ch["data"])
                        elif ch["type"] in ("SentenceBoundary", "WordBoundary"):
                            bounds.append(dict(offset=ch["offset"] / 1e7, duration=ch["duration"] / 1e7, text=ch["text"]))
                break
            except Exception as e:  # retry on network hiccups
                print("retry", sid, i, e, file=sys.stderr)
                await asyncio.sleep(2 + attempt * 2)
        else:
            raise RuntimeError(f"TTS failed {sid} {i}")
    # trim leading/trailing silence lightly, convert to 48k mono wav
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp3, "-ar", "48000", "-ac", "1", wav], check=True)
    j = dict(text=text, say=beat["say"], voice=VOICE, rate=RATE, duration=dur(wav), bounds=bounds)
    json.dump(j, open(jpath, "w"), ensure_ascii=False, indent=1)
    return j


async def main():
    sem = asyncio.Semaphore(4)
    for s in SCENES:
        res = await asyncio.gather(*[one(s["id"], i, b, sem) for i, b in enumerate(s["beats"])])
        meta = dict(id=s["id"], durations=[r["duration"] for r in res])
        json.dump(meta, open(os.path.join(META, s["id"] + ".json"), "w"), indent=1)
        print(s["id"], round(sum(meta["durations"]), 1), "s", [round(d, 1) for d in meta["durations"]])

asyncio.run(main())
