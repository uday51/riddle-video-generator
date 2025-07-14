import cv2
import textwrap
import requests
import numpy as np
import os
import pyttsx3
import os
import random
from gtts import gTTS
import re
import boto3



#Get one Riddle
response= requests.get("http://127.0.0.1:5000/get-riddle")
if response.status_code==200:
  riddle_data=response.json()
text=riddle_data["riddle"]
speech_text=text.strip()
id=riddle_data["id"]


elevn_api_key=""
random_number=random.randrange(1,4)





if random_number==1:
  #TTS
  engine=pyttsx3.init()
  audio_file="riidle_audio.mp3"
  engine.save_to_file(speech_text,audio_file)
  engine.runAndWait()


if random_number==2:
   pronunciation_fixes = {
    r'\bdebut\b': "day-byoo",        
    r'\bdebuted\b': "day-byood",     
    r'\bdebuting\b': "day-byoo-ing", 
    r'\bODI\b': "O D I",
    }
   for word, pronunciation in pronunciation_fixes.items():
    
      speech_text = speech_text.replace(word.lower(), pronunciation).replace(word.capitalize(), pronunciation.capitalize())

  #TTS
   audio_file = "riidle_audio.mp3"
   tts = gTTS(text=speech_text, lang='en-in', slow=False)
   tts.save(audio_file)
   
if random_number==3
  polly=boto3.client('polly',aws_access_key_id="",aws_secret_access_key="",region_name='')
  
  response=polly.synthesize_speech(
    Text=speech_text,
    OutputFormat='mp3',
    VoiceId='Raveena')
    
  audio_file="riidle_audio.mp3"
  with open(audio_file,'wb') as f:
    f.write(response['AudioStream'].read())
    
if random_number==4:
  elevenlabs_voice_id = "21m00Tcm4TlvDq8ikWAM"
  headers = {
        "xi-api-key": elevn_api_key,
        "Content-Type": "application/json"
    }
  data = {
        "text": speech_text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
  url = f"https://api.elevenlabs.io/v1/text-to-speech/{elevenlabs_voice_id}"
  response = requests.post(url, headers=headers, json=data)

  if response.status_code == 200:
        audio_file = "riidle_audio.mp3"
        with open(audio_file, "wb") as f:
            f.write(response.content)
       
  else:
        
        print(response.text)
        exit()
  
  

#Video Parameters
width,height=720, 1280
fps=30
duration=10
total_frames=fps*duration


#Video Writer
fourcc=cv2.VideoWriter_fourcc(*'mp4v')
out=cv2.VideoWriter('final_video.mp4',fourcc,fps,(width,height))


#selecting one bg color and font color
color_pairs = [
    ((0, 51, 102), (255, 223, 102)),     # Dark Blue & Light Yellow
    ((34, 139, 34), (255, 255, 255)),    # Forest Green & White
    ((75, 0, 130), (224, 255, 255)),     # Indigo & Light Cyan
    ((139, 0, 0), (220, 220, 220)),      # Dark Red & Light Gray

    ((25, 25, 112), (240, 248, 255)),    # Midnight Blue & Alice Blue
    ((0, 100, 0), (255, 250, 240)),      # Dark Green & Floral White
    ((47, 79, 79), (255, 255, 224)),     # Dark Slate Gray & Light Yellow
    ((72, 61, 139), (245, 245, 245)),    # Dark Slate Blue & White Smoke

    ((0, 0, 0), (255, 255, 255)),        # Black & White (classic)
    ((255, 140, 0), (0, 0, 0)),          # Dark Orange & Black
    ((128, 0, 128), (255, 255, 255)),    # Purple & White
    ((210, 105, 30), (255, 255, 240)),   # Chocolate Brown & Ivory

    ((70, 130, 180), (255, 255, 255)),   # Steel Blue & White
    ((0, 128, 128), (255, 248, 220)),    # Teal & Cornsilk
    ((60, 179, 113), (0, 0, 0)),         # Medium Sea Green & Black
    ((25, 25, 25), (173, 255, 47)),      # Near Black & Green Yellow
]


background_color,font_color=random.choice(color_pairs)


font = cv2.FONT_HERSHEY_SIMPLEX
font_scale=1
thickness=3
shadow_color = (0, 0, 0)

wrapped_text=textwrap.wrap(text,width=40)


(text_width,text_height), baseline=cv2.getTextSize(text,font,font_scale,thickness)
line_spacing=text_height+15


x=42
y_start=(height-(line_spacing*len(wrapped_text)))//2


for _ in range(total_frames):
  frame=np.full((height,width,3),background_color,dtype=np.uint8)
  y=y_start
  for line in wrapped_text:
    cv2.putText(frame,line,(x,y),font,font_scale,font_color,thickness,cv2.LINE_AA)
    y+=line_spacing
  out.write(frame)
out.release()

with open('title_count.txt','r') as f:
  last_number=int(f.read().strip())


output_video=f'Cricket_Riddle_{last_number}.mp4'
print(output_video)
os.system(f"ffmpeg -i final_video.mp4 -i {audio_file} -c:v copy -c:a aac -strict experimental {output_video}")
current_number=last_number+1
with open('title_count.txt','w') as f:
  f.write(str(current_number))



riddle_id=riddle_data["id"]
url=f"http://127.0.0.1:5000/update-riddle/{riddle_id}"
payload = {"processed": "yes"}
  
response= requests.put(url,json=payload)






