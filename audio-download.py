import pafy

url="" # youtube link 
video= pafy.new(url)

bestaudio = video.getbestaudio()
bestaudio.download() # will save file in current directory