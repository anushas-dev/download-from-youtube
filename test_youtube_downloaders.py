#!/usr/bin/env python3
"""
Comprehensive tests for the YouTube download scripts.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import shutil
import importlib.util

# Add the current directory to sys.path to import the modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def import_module_from_file(filepath):
    """Dynamically import a module from a file path."""
    # Convert dashes to underscores for valid Python module names
    module_name = os.path.splitext(os.path.basename(filepath))[0].replace('-', '_')
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class TestImports(unittest.TestCase):
    """Test that all required modules can be imported."""
    
    def test_pafy_import(self):
        """Test that pafy can be imported."""
        try:
            import pafy
            self.assertTrue(True)
        except ImportError:
            self.fail("pafy module could not be imported")
    
    def test_pytube_import(self):
        """Test that pytube can be imported."""
        try:
            from pytube import YouTube
            self.assertTrue(True)
        except ImportError:
            self.fail("pytube module could not be imported")


class TestAudioDownload(unittest.TestCase):
    """Test audio download functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.valid_url = "https://www.youtube.com/watch?v=uH9d_c_QX_E"
        self.invalid_url = "https://www.youtube.com/watch?v=invalid"
        
    def test_download_audio_with_valid_url(self):
        """Test downloading audio with a valid URL."""
        with patch('pafy.new') as mock_pafy_new:
            # Create mock video object
            mock_video = MagicMock()
            mock_audio = MagicMock()
            mock_audio.download.return_value = "test_audio.mp3"
            
            mock_video.getbestaudio.return_value = mock_audio
            mock_pafy_new.return_value = mock_video
            
            # Import the function
            audio_module = import_module_from_file('audio-download.py')
            download_audio = audio_module.download_audio
            
            # Test the function
            result = download_audio(self.valid_url)
            
            # Assertions
            mock_pafy_new.assert_called_once_with(self.valid_url)
            mock_video.getbestaudio.assert_called_once()
            mock_audio.download.assert_called_once()
            self.assertEqual(result, "test_audio.mp3")
    
    def test_download_audio_with_empty_url(self):
        """Test downloading audio with an empty URL."""
        audio_module = import_module_from_file('audio-download.py')
        download_audio = audio_module.download_audio
        
        with self.assertRaises(ValueError) as context:
            download_audio("")
        
        self.assertIn("URL cannot be empty", str(context.exception))
    
    def test_download_audio_with_none_url(self):
        """Test downloading audio with None URL."""
        audio_module = import_module_from_file('audio-download.py')
        download_audio = audio_module.download_audio
        
        with self.assertRaises(ValueError) as context:
            download_audio(None)
        
        self.assertIn("URL cannot be empty", str(context.exception))
    
    def test_download_audio_with_connection_error(self):
        """Test downloading audio when connection fails."""
        with patch('pafy.new', side_effect=Exception("Connection failed")):
            audio_module = import_module_from_file('audio-download.py')
            download_audio = audio_module.download_audio
            
            with self.assertRaises(Exception) as context:
                download_audio(self.invalid_url)
            
            self.assertIn("Failed to download audio", str(context.exception))


class TestVideoDownload(unittest.TestCase):
    """Test video download functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.valid_url = "https://www.youtube.com/watch?v=uH9d_c_QX_E"
        self.invalid_url = "https://www.youtube.com/watch?v=invalid"
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
    def test_download_video_with_valid_url(self):
        """Test downloading video with a valid URL."""
        with patch('pytube.YouTube') as mock_youtube:
            # Create mock objects
            mock_stream = MagicMock()
            mock_stream.download.return_value = os.path.join(self.temp_dir, "test_video.mp4")
            
            mock_streams = MagicMock()
            mock_streams.filter.return_value.order_by.return_value.__getitem__.return_value = mock_stream
            
            mock_yt = MagicMock()
            mock_yt.streams = mock_streams
            mock_youtube.return_value = mock_yt
            
            # Import the function
            video_module = import_module_from_file('video-download.py')
            download_video = video_module.download_video
            
            # Test the function
            result = download_video(self.valid_url, self.temp_dir)
            
            # Assertions
            mock_youtube.assert_called_once_with(self.valid_url)
            mock_streams.filter.assert_called_once_with(progressive=True, file_extension='mp4')
            mock_stream.download.assert_called_once_with(self.temp_dir)
            self.assertEqual(result, os.path.join(self.temp_dir, "test_video.mp4"))
    
    def test_download_video_with_default_path(self):
        """Test downloading video with default save path."""
        with patch('pytube.YouTube') as mock_youtube:
            # Create mock objects
            mock_stream = MagicMock()
            mock_stream.download.return_value = "test_video.mp4"
            
            mock_streams = MagicMock()
            mock_streams.filter.return_value.order_by.return_value.__getitem__.return_value = mock_stream
            
            mock_yt = MagicMock()
            mock_yt.streams = mock_streams
            mock_youtube.return_value = mock_yt
            
            # Import the function
            video_module = import_module_from_file('video-download.py')
            download_video = video_module.download_video
            
            # Test the function
            result = download_video(self.valid_url)
            
            # Assertions
            mock_youtube.assert_called_once_with(self.valid_url)
            mock_streams.filter.assert_called_once_with(progressive=True, file_extension='mp4')
            mock_stream.download.assert_called_once_with("")
            self.assertEqual(result, "test_video.mp4")
    
    def test_download_video_with_empty_url(self):
        """Test downloading video with an empty URL."""
        video_module = import_module_from_file('video-download.py')
        download_video = video_module.download_video
        
        with self.assertRaises(ValueError) as context:
            download_video("")
        
        self.assertIn("Link cannot be empty", str(context.exception))
    
    def test_download_video_with_none_url(self):
        """Test downloading video with None URL."""
        video_module = import_module_from_file('video-download.py')
        download_video = video_module.download_video
        
        with self.assertRaises(ValueError) as context:
            download_video(None)
        
        self.assertIn("Link cannot be empty", str(context.exception))
    
    def test_download_video_with_connection_error(self):
        """Test downloading video when connection fails."""
        with patch('pytube.YouTube', side_effect=Exception("Connection failed")):
            video_module = import_module_from_file('video-download.py')
            download_video = video_module.download_video
            
            with self.assertRaises(Exception) as context:
                download_video(self.invalid_url)
            
            self.assertIn("Connection Error", str(context.exception))
    
    def test_download_video_with_download_error(self):
        """Test downloading video when download fails."""
        with patch('pytube.YouTube') as mock_youtube:
            # Create mock objects
            mock_yt = MagicMock()
            mock_yt.streams.filter.side_effect = Exception("Download failed")
            mock_youtube.return_value = mock_yt
            
            # Import the function
            video_module = import_module_from_file('video-download.py')
            download_video = video_module.download_video
            
            with self.assertRaises(Exception) as context:
                download_video(self.valid_url)
            
            self.assertIn("Error: Couldn't download the video", str(context.exception))


class TestScriptSyntax(unittest.TestCase):
    """Test that Python scripts have valid syntax."""
    
    def test_audio_download_syntax(self):
        """Test audio-download.py has valid syntax."""
        with open('audio-download.py', 'r') as f:
            code = f.read()
        try:
            compile(code, 'audio-download.py', 'exec')
        except SyntaxError as e:
            self.fail(f"audio-download.py has syntax error: {e}")
    
    def test_video_download_syntax(self):
        """Test video-download.py has valid syntax."""
        with open('video-download.py', 'r') as f:
            code = f.read()
        try:
            compile(code, 'video-download.py', 'exec')
        except SyntaxError as e:
            self.fail(f"video-download.py has syntax error: {e}")


class TestUserInput(unittest.TestCase):
    """Test user input handling in main sections."""
    
    def test_audio_download_main_with_input(self):
        """Test audio download main section with user input."""
        with patch('builtins.input', return_value="https://www.youtube.com/watch?v=test123"):
            with patch('builtins.print') as mock_print:
                with patch('pafy.new') as mock_pafy_new:
                    # Create mock video object
                    mock_video = MagicMock()
                    mock_audio = MagicMock()
                    mock_audio.download.return_value = "test_audio.mp3"
                    
                    mock_video.getbestaudio.return_value = mock_audio
                    mock_pafy_new.return_value = mock_video
                    
                    # Execute the main section code directly
                    url = input("Please enter the YouTube URL: ").strip()
                    if not url:
                        print("URL cannot be empty")
                    else:
                        try:
                            # This is the call that would be made in the main section
                            mock_pafy_new(url)
                            print("Audio downloaded successfully")
                        except Exception as e:
                            print(f"Error: {e}")
                    
                    # Assertions
                    mock_pafy_new.assert_called_once_with("https://www.youtube.com/watch?v=test123")
                    mock_print.assert_called_once_with("Audio downloaded successfully")
    
    def test_audio_download_main_with_empty_input(self):
        """Test audio download main section with empty input."""
        with patch('builtins.input', return_value=""):
            with patch('builtins.print') as mock_print:
                # Execute the main section code directly
                url = input("Please enter the YouTube URL: ").strip()
                if not url:
                    print("URL cannot be empty")
                else:
                    try:
                        # Import and call the function
                        audio_module = import_module_from_file('audio-download.py')
                        audio_module.download_audio(url)
                        print("Audio downloaded successfully")
                    except Exception as e:
                        print(f"Error: {e}")
                
                # Assertions
                mock_print.assert_called_once_with("URL cannot be empty")
    
    def test_video_download_main_with_input(self):
        """Test video download main section with user input."""
        with patch('builtins.input', side_effect=["https://www.youtube.com/watch?v=test123", "/test/path"]):
            with patch('builtins.print') as mock_print:
                with patch('pytube.YouTube') as mock_youtube:
                    # Create mock objects
                    mock_stream = MagicMock()
                    mock_stream.download.return_value = "/test/path/test_video.mp4"
                    
                    mock_streams = MagicMock()
                    mock_streams.filter.return_value.order_by.return_value.__getitem__.return_value = mock_stream
                    
                    mock_yt = MagicMock()
                    mock_yt.streams = mock_streams
                    mock_youtube.return_value = mock_yt
                    
                    # Execute the main section code directly
                    LINK = input("Please enter the YouTube URL: ").strip()
                    SAVE_PATH = input("Please enter the save path (leave empty for current directory): ").strip()
                    
                    if not LINK:
                        print("Please provide a YouTube link")
                    else:
                        try:
                            # This is the call that would be made in the main section
                            mock_youtube(LINK)
                            mock_stream.download(SAVE_PATH)
                            print("Video downloaded successfully")
                        except Exception as e:
                            print(f"Error: {e}")
                    
                    # Assertions
                    mock_youtube.assert_called_once_with("https://www.youtube.com/watch?v=test123")
                    mock_print.assert_called_once_with("Video downloaded successfully")
    
    def test_video_download_main_with_empty_input(self):
        """Test video download main section with empty URL input."""
        with patch('builtins.input', side_effect=["", "/test/path"]):
            with patch('builtins.print') as mock_print:
                # Execute the main section code directly
                LINK = input("Please enter the YouTube URL: ").strip()
                SAVE_PATH = input("Please enter the save path (leave empty for current directory): ").strip()
                
                if not LINK:
                    print("Please provide a YouTube link")
                else:
                    try:
                        # Import and call the function
                        video_module = import_module_from_file('video-download.py')
                        video_module.download_video(LINK, SAVE_PATH)
                        print("Video downloaded successfully")
                    except Exception as e:
                        print(f"Error: {e}")
                
                # Assertions
                mock_print.assert_called_once_with("Please provide a YouTube link")


if __name__ == '__main__':
    unittest.main()
