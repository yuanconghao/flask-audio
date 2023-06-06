#!/bin/sh

curl https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer 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" \
  -H "Content-Type: multipart/form-data" \
  -F file="@/home/work/data/voice/jfk.wav" \
  -F model="whisper-1" \
  -F language="zh"