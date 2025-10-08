#!/usr/bin/env python3
"""
Simple tests for the YouTube download scripts.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock


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


if __name__ == '__main__':
    unittest.main()