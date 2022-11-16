#! /bin/sh -e
# framegrab v0.1

frames="$1"
filename="$2"
printf '%s' "$frames" |
sed 's:\[\|\]::g; s:[, ]\+:\n:g' |
xargs printf '%03d\n' |
xargs -IFRAME ffmpeg -i "$filename" -vf "select=eq(n\,FRAME)" -vframes 1 out_imageFRAME.jpg


framegrab '[100, 110, 127, 270, 300]' test_video.mp4