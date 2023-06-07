#!/bin/sh

curl https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer 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" \
  -H "Content-Type: multipart/form-data" \
  -F file="@/home/work/data/voice/Bayan3.wav" \
  -F model="whisper-1" \
  -F language="zh"