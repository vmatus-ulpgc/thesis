#!/bin/bash

#Authors: Vicente Matus vmatus@idetic.eu

echo 'This is RaspiCamera Capture Maker v0.000000001 by V. Matus (vmatus@idetic.eu)' #Please keep credits to the autors somewhere :)
echo 'You are about to make a capture!! Please type a name for it and hit [ENTER]: '

read capname

echo `date '+%Y-%m-%d %H:%M:%S'`

time=3333	#milliseconds
fps=30		#frames per second
#sh_speed=85 	#microseconds

echo 'OK. Name chosen is '$capname'. Note I will add labels in the final name of videos and photos taken.' 

#echo 'Now enter the Shutter Speed for this capture'

#read sh_speed 

echo 'Lights, Camera, Action!! (Runing the command)'

#mkdir ${capname}


echo `date '+%Y-%m-%d %H:%M:%S'`

sh_speed=85
vidname=vid_${capname}_${sh_speed}us.h264
raspivid -o $vidname -t ${time} -fps ${fps} -ss ${sh_speed} -ex night #-ex fixedfps
picname=pic_${capname}_${sh_speed}us.jpeg
raspistill -o $picname -ss ${sh_speed} --raw --nopreview --timeout 0

echo `date '+%Y-%m-%d %H:%M:%S'`
sh_speed=160
vidname=vid_${capname}_${sh_speed}us.h264
raspivid -o $vidname -t ${time} -fps ${fps} -ss ${sh_speed} -ex night #-ex fixedfps
picname=pic_${capname}_${sh_speed}us.jpeg
raspistill -o $picname -ss ${sh_speed} --raw --nopreview --timeout 0

echo `date '+%Y-%m-%d %H:%M:%S'`
sh_speed=293
vidname=vid_${capname}_${sh_speed}us.h264
raspivid -o $vidname -t ${time} -fps ${fps} -ss ${sh_speed} -ex night #-ex fixedfps
picname=pic_${capname}_${sh_speed}us.jpeg
raspistill -o $picname -ss ${sh_speed} --raw --nopreview --timeout 0

echo `date '+%Y-%m-%d %H:%M:%S'`
sh_speed=633
vidname=vid_${capname}_${sh_speed}us.h264
raspivid -o $vidname -t ${time} -fps ${fps} -ss ${sh_speed} -ex night #-ex fixedfps
picname=pic_${capname}_${sh_speed}us.jpeg
raspistill -o $picname -ss ${sh_speed} --raw --nopreview --timeout 0

echo `date '+%Y-%m-%d %H:%M:%S'`
sh_speed=1000
vidname=vid_${capname}_${sh_speed}us.h264
raspivid -o $vidname -t ${time} -fps ${fps} -ss ${sh_speed} -ex night #-ex fixedfps
picname=pic_${capname}_${sh_speed}us.jpeg
raspistill -o $picname -ss ${sh_speed} --raw --nopreview --timeout 0


 #-ex fixedfps

echo `date '+%Y-%m-%d %H:%M:%S'`
echo 'Ready!'

echo `date '+%Y-%m-%d %H:%M:%S'`
#echo 'Summary of the actions taken:'

#echo 'Video Capture Time was '${time}' milliseconds'
#echo 'Frame Rate was '${fps}' fps'
#echo 'Shutter Speed was '${sh_speed}' microseconds'

#echo 'Filename for video: ' $vidname'.'

echo `date '+%Y-%m-%d %H:%M:%S'`
echo 'Bye :)'


#CONVERSION TO MPEG

#ffmpeg -r 30 -i $vidname -vcodec copy converted_${vidname}.mp4


