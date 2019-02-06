#!/usr/bin/env bash

# Sync
scp pi@${1}:/videos/* .

# Convert H264 to MP4
for f in *.h264; do ffmpeg -i "file:${f}" -c copy "file:${f%.*}.mp4"; done

# Delete H264 locally
rm *.h264
