<?php

$curl = curl_init();

curl_setopt_array($curl, array(
  CURLOPT_URL => 'https://api.openai.com/v1/audio/transcriptions',
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => '',
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 0,
  CURLOPT_FOLLOWLOCATION => true,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => 'POST',
  CURLOPT_POSTFIELDS => array('file'=> new CURLFILE('/data/audio-core/data/Bayan课后.wav'),'model' => 'whisper-1','language' => 'zh'),
  CURLOPT_HTTPHEADER => array(
    'Authorization: Bearer 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'
  ),
));

$response = curl_exec($curl);

curl_close($curl);
echo $response;