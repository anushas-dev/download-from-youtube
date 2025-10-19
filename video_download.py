import os
import os
import certifi
from pytube import YouTube
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def download_video(link, save_path=""):
    """Download video from YouTube.
    
    Args:
        link (str): YouTube video URL
        save_path (str): Path to save the file (default: current directory)
        
    Returns:
        str: Path to downloaded file
        
    Raises:
        ValueError: If link is invalid
        Exception: If download fails
    """
    if not link:
        raise ValueError("Link cannot be empty")
    
    try:
        yt = YouTube(link)
    except Exception as e:
        raise Exception(f"Connection Error: {str(e)}")
    
    try:
        # Create save path if it doesn't exist
        if save_path and not os.path.exists(save_path):
            os.makedirs(save_path)
            
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1]
        filename = stream.download(save_path)
        return filename
    except Exception as e:
        raise Exception(f"Error: Couldn't download the video - {str(e)}")

if __name__ == "__main__":
    LINK = input("Please enter the YouTube URL: ").strip()
    SAVE_PATH = input("Please enter the save path (leave empty for current directory): ").strip()
    
    if not LINK:
        print("Please provide a YouTube link")
    else:
        try:
            download_video(LINK, SAVE_PATH)
            print("Video downloaded successfully")
        except Exception as e:
            print(f"Error: {e}")
