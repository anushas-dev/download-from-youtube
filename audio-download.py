import pafy

url="https://www.youtube.com/watch?v=uH9d_c_QX_E" # youtube link 
video= pafy.new(url)

bestaudio = video.getbestaudio()
bestaudio.download() # will save file in current directory