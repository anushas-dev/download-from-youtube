from pytube import YouTube

SAVE_PATH="" # path to save the file
LINK=""      # link to youtube video

try:
    yt = YouTube(LINK)
except:
    print("Connection Error")

try:
    stream = yt.streams.filter(progressive=True,file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH)
    print("Video downloaded")
except:
    print("Error: Couldn't download the video")
