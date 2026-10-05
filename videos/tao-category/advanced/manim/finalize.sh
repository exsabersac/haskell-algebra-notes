#!/usr/bin/env bash
# Final mux: concat scenes -> multiply paper -> burn subtitles; loudness-normalised narration (AAC).
set -euo pipefail
cd "$(dirname "$0")/.."
ffmpeg -y -v error -f concat -safe 0 -i build/concat_hq.txt -c copy build/video_raw.mp4
ffmpeg -y -v error -i build/narration_raw_hq.wav -af "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000" -ar 48000 -ac 1 build/narration.wav
FILT="[1:v]format=gbrp[p];[0:v]format=gbrp[v];[v][p]blend=all_mode=multiply:shortest=1,format=yuv420p"
ffmpeg -y -v error -i build/video_raw.mp4 -loop 1 -framerate 30 -i build/paper.png -i build/narration.wav \
  -filter_complex "${FILT},ass=build/subs_hq.ass[o]" -map "[o]" -map 2:a \
  -c:v libx264 -preset slow -crf 18 -profile:v high -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart -shortest final/tao-category.mp4
# clean (no burned subs) version with a soft Chinese subtitle track
ffmpeg -y -v error -i build/video_raw.mp4 -loop 1 -framerate 30 -i build/paper.png -i build/narration.wav -i final/tao-category.srt \
  -filter_complex "${FILT}[o]" -map "[o]" -map 2:a -map 3:s \
  -c:v libx264 -preset slow -crf 18 -profile:v high -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -c:s mov_text -metadata:s:s:0 language=chi -movflags +faststart final/tao-category-nosubs.mp4
echo finalize-done
