import av

input_file = "/home/michal/dev/FaceAnimizerBackend/app/temp_videos/2b4350e0-219a-45d6-8842-3861e411f1f7/2b4350e0-219a-45d6-8842-3861e411f1f7.mp4"
output_file = "/home/michal/dev/FaceAnimizerBackend/app/temp_videos/output_processed.mp4"

# --------------------------
# Otwieramy kontenery
# --------------------------
input_av = av.open(input_file)
output_av = av.open(output_file, mode='w')

# Wideo
input_video_stream = next(s for s in input_av.streams if s.type == 'video')
output_video_stream = output_av.add_stream_from_template(template=input_video_stream)

input_audio_stream = next(s for s in input_av.streams if s.type == 'audio')
output_audio_stream = output_av.add_stream_from_template(template=input_audio_stream)

for packet in input_av.demux([input_video_stream, input_audio_stream]):
    if packet.dts is None:
        continue
    
    if packet.stream == input_video_stream:
        packet.stream = output_video_stream

    if packet.stream == input_audio_stream:
        packet.stream = output_audio_stream

    output_av.mux(packet)

input_av.close()
output_av.close()