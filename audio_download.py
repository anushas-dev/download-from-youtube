import os
import certifi
import pafy
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def download_audio(url):
    """Download audio from a YouTube video.
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        str: Path to downloaded file
        
    Raises:
        ValueError: If URL is invalid
        Exception: If download fails
    """
    if not url:
        raise ValueError("URL cannot be empty")
    
    try:
        video = pafy.new(url)
        bestaudio = video.getbestaudio()
        filename = bestaudio.download()  # will save file in current directory
        return filename
    except Exception as e:
        raise Exception(f"Failed to download audio: {str(e)}")

if __name__ == "__main__":
    url = input("Please enter the YouTube URL: ").strip()
    if not url:
        print("URL cannot be empty")
    else:
        try:
            download_audio(url)
            print("Audio downloaded successfully")
        except Exception as e:
            print(f"Error: {e}")
