import av
import cv2

input_file = "/home/michal/dev/FaceAnimizerBackend/app/temp_videos/2b4350e0-219a-45d6-8842-3861e411f1f7/2b4350e0-219a-45d6-8842-3861e411f1f7.mp4"
output_file = "/home/michal/dev/FaceAnimizerBackend/app/temp_videos/output_processed.mp4"

# --------------------------
# Otwieramy kontenery
# --------------------------
input_av = av.open(input_file)
output_av = av.open(output_file, mode='w')

# Strumienie
input_video_stream = next(s for s in input_av.streams if s.type == 'video')
input_audio_stream = next(s for s in input_av.streams if s.type == 'audio')

# Strumień audio pozostawiamy przez template (passthrough)
output_audio_stream = output_av.add_stream_from_template(template=input_audio_stream)

# Wideo musimy enkodować, żeby móc modyfikować klatki
output_video_stream = output_av.add_stream(
    codec_name='libx264',
    rate=round(input_video_stream.average_rate) if input_video_stream.average_rate else 30
)
output_video_stream.width = input_video_stream.width
output_video_stream.height = input_video_stream.height
output_video_stream.pix_fmt = 'yuv420p'

# --------------------------
# Wideo + audio
# --------------------------
for packet in input_av.demux([input_video_stream, input_audio_stream]):
    if packet.dts is None:
        continue

    if packet.stream == input_video_stream:
        # dekodujemy klatki wideo
        for frame in packet.decode():
            # tu możesz użyć frame.to_ndarray()
            img = frame.to_ndarray(format='bgr24')

            # przykład: prosty blur
            processed_img = cv2.GaussianBlur(img, (25,25), 0)

            # zamiana na VideoFrame i konwersja do YUV
            new_frame = av.VideoFrame.from_ndarray(processed_img, format='bgr24')
            new_frame = new_frame.reformat(format='yuv420p', width=frame.width, height=frame.height)
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base

            # enkodowanie i muxowanie
            for out_packet in output_video_stream.encode(new_frame):
                output_av.mux(out_packet)

    elif packet.stream == input_audio_stream:
        # kopiujemy pakiety audio bez dekodowania
        packet.stream = output_audio_stream
        output_av.mux(packet)

# flush video encoder
for out_packet in output_video_stream.encode():
    output_av.mux(out_packet)

input_av.close()
output_av.close()
