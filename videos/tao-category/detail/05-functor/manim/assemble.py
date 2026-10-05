"""Assemble: concat scene videos, place narration clips at recorded beat times, build SRT/ASS, multiply paper, burn subs."""
import json, os, re, subprocess, sys
import numpy as np
from content import SCENES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
FIN = os.path.join(ROOT, "final")
SR = 48000
MODE = sys.argv[1] if len(sys.argv) > 1 else "hq"      # hq | lq
os.makedirs(FIN, exist_ok=True)


def vpath(sid):
    if MODE == "hq":
        return f"{B}/hq/{sid}/videos/scenes/1080p30/{sid}.mp4"
    return f"{B}/lq/{sid}/videos/scenes/480p15/{sid}.mp4"


def probe_dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
                                          "-show_entries", "stream=nb_read_packets,r_frame_rate", "-of", "json", p]).decode() and
                 _frames(p))


def _frames(p):
    j = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
                                            "-show_entries", "stream=nb_read_packets,r_frame_rate", "-of", "json", p]))
    st = j["streams"][0]
    num, den = map(int, st["r_frame_rate"].split("/"))
    return int(st["nb_read_packets"]) * den / num


def load_wav(p):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, np.float32)


def fmt_srt(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def fmt_ass(t):
    cs = int(round(t * 100)); h, cs = divmod(cs, 360000); m, cs = divmod(cs, 6000); s, cs = divmod(cs, 100)
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"


SENT_RE = re.compile(r"[^。！？]*[。！？]?")
MAXC = 21


def split_sentences(t):
    return [x for x in SENT_RE.findall(t) if x.strip()]


def chunk(sent):
    """Split a sentence into display chunks <= MAXC chars at soft punctuation."""
    parts = re.findall(r"[^，、：；——]*(?:——|[，、：；])?", sent)
    parts = [p for p in parts if p]
    out, cur = [], ""
    for p in parts:
        if len(cur) + len(p) <= MAXC or not cur:
            cur += p
        else:
            out.append(cur); cur = p
    if cur:
        out.append(cur)
    # merge very short fragments into a neighbour
    merged = []
    for c in out:
        if merged and (len(c) < 7 or len(merged[-1]) < 7) and len(merged[-1]) + len(c) <= MAXC + 5:
            merged[-1] += c
        else:
            merged.append(c)
    out = merged
    res = []
    for c in out:   # hard-wrap anything still too long
        while len(c) > MAXC + 4:
            res.append(c[:MAXC]); c = c[MAXC:]
        res.append(c)
    return res


def clean(c):
    c = c.strip()
    c = re.sub(r"[，。；：、]+$", "", c)
    c = c.replace("，", " ").replace("；", " ").replace("。", " ")
    return re.sub(r"\s+", " ", c).strip()


def beat_cues(beat_json, t0):
    """Cues for one beat; uses edge-tts sentence boundaries when they line up with the display sentences."""
    say = beat_json["say"]
    dur = beat_json["duration"]
    sents = split_sentences(say)
    bounds = [b for b in beat_json["bounds"]]
    spans = []
    if len(bounds) == len(sents):
        for i, b in enumerate(bounds):
            st = b["offset"]
            en = bounds[i + 1]["offset"] if i + 1 < len(bounds) else min(dur, b["offset"] + b["duration"] + 0.25)
            spans.append((st, en))
    else:
        tot = sum(len(s) for s in sents)
        lead = bounds[0]["offset"] if bounds else 0.1
        end = (bounds[-1]["offset"] + bounds[-1]["duration"]) if bounds else dur
        acc = lead
        for s in sents:
            d = (end - lead) * len(s) / tot
            spans.append((acc, acc + d)); acc += d
    cues = []
    for s, (st, en) in zip(sents, spans):
        chs = chunk(s)
        tot = sum(len(c) for c in chs)
        acc = st
        for c in chs:
            d = (en - st) * len(c) / tot
            txt = clean(c)
            if txt:
                cues.append([t0 + acc, t0 + acc + d, txt])
            acc += d
    return cues


def main():
    offsets, total = {}, 0.0
    lst = open(f"{B}/concat_{MODE}.txt", "w")
    for s in SCENES:
        p = vpath(s["id"])
        d = _frames(p)
        offsets[s["id"]] = (total, d)
        total += d
        lst.write(f"file '{p}'\n")
    lst.close()
    print("total video", round(total, 2))
    audio = np.zeros(int((total + 1) * SR), np.float32)
    cues = []
    chapters = []
    for s in SCENES:
        sid = s["id"]
        off, d = offsets[sid]
        chapters.append((off, sid, s["title"]))
        tm = json.load(open(f"{B}/timings/{sid}.json"))
        assert abs(tm["total"] - d) < 0.2, (sid, tm["total"], d)
        for k, st in enumerate(tm["starts"]):
            bj = json.load(open(f"{ROOT}/audio/beats/{sid}_{k:02d}.json"))
            w = load_wav(f"{ROOT}/audio/beats/{sid}_{k:02d}.wav")
            fade = int(0.008 * SR)
            w = w.copy(); w[:fade] *= np.linspace(0, 1, fade); w[-fade:] *= np.linspace(1, 0, fade)
            i0 = int(round((off + st) * SR))
            audio[i0:i0 + len(w)] += w
            cues += beat_cues(bj, off + st)
    audio = audio[:int(total * SR)]
    raw = f"{B}/narration_raw_{MODE}.wav"
    import wave
    with wave.open(raw, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
        wf.writeframes((np.clip(audio, -1, 1) * 32767).astype(np.int16).tobytes())
    # de-overlap cues
    cues.sort()
    for i in range(len(cues) - 1):
        if cues[i][1] > cues[i + 1][0] - 0.02:
            cues[i][1] = cues[i + 1][0] - 0.02
    srt = "".join(f"{i + 1}\n{fmt_srt(a)} --> {fmt_srt(b)}\n{t}\n\n" for i, (a, b, t) in enumerate(cues))
    srt_path = f"{FIN}/tao-category-detail-05.srt" if MODE == "hq" else f"{B}/preview.srt"
    open(srt_path, "w").write(srt)
    ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1080", "WrapStyle: 0",
           "ScaledBorderAndShadow: yes", "", "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
           "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           "Style: Ink,LXGW WenKai,52,&H00242A30,&H00242A30,&H00DCE8F0,&H00000000,0,0,0,0,100,100,1,0,1,2.6,0,2,120,120,44,1",
           "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for a, b, t in cues:
        ass.append(f"Dialogue: 0,{fmt_ass(a)},{fmt_ass(b)},Ink,,0,0,0,,{{\\fad(120,120)}}{t}")
    open(f"{B}/subs_{MODE}.ass", "w").write("\n".join(ass) + "\n")
    json.dump(dict(total=total, chapters=chapters, offsets=offsets, n_cues=len(cues)),
              open(f"{B}/assembly_{MODE}.json", "w"), ensure_ascii=False, indent=1)
    print("cues", len(cues), "max len", max(len(c[2]) for c in cues))
    for off, sid, t in chapters:
        m, sec = divmod(int(off), 60)
        print(f"{m:02d}:{sec:02d} {sid} {t}")


if __name__ == "__main__":
    main()
