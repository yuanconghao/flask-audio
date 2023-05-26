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
  CURLOPT_POSTFIELDS => array('file'=> new CURLFILE('/home/work/data/voice/168.wav'),'model' => 'whisper-1','language' => 'zh'),
  CURLOPT_HTTPHEADER => array(
    'Authorization: Bearer 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'
  ),
));

$response = curl_exec($curl);

curl_close($curl);
echo $response;

