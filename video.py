import cv2
import textwrap
import requests
import numpy as np
import os
import pyttsx3
import os
import random




response= requests.get("http://127.0.0.1:5000/get-riddle")
if response.status_code==200:
  riddle_data=response.json()

text=riddle_data["riddle"]
id=riddle_data["id"]
engine=pyttsx3.init()
audio_file="riidle_audio.mp3"
engine.save_to_file(text,audio_file)
engine.runAndWait()

width,height=720, 1280
fps=30
duration=10
total_frames=fps*duration


fourcc=cv2.VideoWriter_fourcc(*'mp4v')
out=cv2.VideoWriter('final_video.mp4',fourcc,fps,(width,height))

color_pairs = [
    ((0, 51, 102), (255, 223, 102)),  # Dark Blue & Light Yellow
    ((34, 139, 34), (255, 255, 255)),  # Dark Green & White
    ((75, 0, 130), (224, 255, 255)),  # Deep Purple & Light Cyan
    ((139, 0, 0), (220, 220, 220)),  # Dark Red & Light Gray
]

background_color,font_color=random.choice(color_pairs)


font = cv2.FONT_HERSHEY_SIMPLEX
font_scale=1
thickness=3
shadow_color = (0, 0, 0)

wrapped_text=textwrap.wrap(text,width=40)


(text_width,text_height), baseline=cv2.getTextSize(text,font,font_scale,thickness)
line_spacing=text_height+15


x=50
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






