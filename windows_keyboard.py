#!/usr/bin/env python3
"""
Alternative Key Sender using Windows API
More reliable for games that don't respond to pyautogui
"""

import ctypes
from ctypes import wintypes
import time

# Windows API constants
VK_CODE = {
    'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45, 'f': 0x46, 'g': 0x47,
    'h': 0x48, 'i': 0x49, 'j': 0x4A, 'k': 0x4B, 'l': 0x4C, 'm': 0x4D, 'n': 0x4E,
    'o': 0x4F, 'p': 0x50, 'q': 0x51, 'r': 0x52, 's': 0x53, 't': 0x54, 'u': 0x55,
    'v': 0x56, 'w': 0x57, 'x': 0x58, 'y': 0x59, 'z': 0x5A,
    'space': 0x20, 'enter': 0x0D, 'tab': 0x09, 'esc': 0x1B,
    '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34, '5': 0x35,
    '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39, '0': 0x30
}

class WindowsKeyboard:
    def __init__(self):
        self.user32 = ctypes.windll.user32
        
    def press_key(self, key):
        """Press and release a key using Windows API"""
        key = key.lower()
        if key not in VK_CODE:
            print(f"Key '{key}' not supported")
            return False
            
        vk_code = VK_CODE[key]
        
        # Key down
        self.user32.keybd_event(vk_code, 0, 0, 0)
        time.sleep(0.05)
        
        # Key up
        self.user32.keybd_event(vk_code, 0, 2, 0)
        return True
    
    def press_sequence(self, keys, delay=0.3):
        """Press a sequence of keys"""
        for key in keys:
            print(f"Pressing key: {key}")
            if self.press_key(key):
                time.sleep(delay)
            else:
                print(f"Failed to press key: {key}")

def test_keys():
    """Test the key pressing"""
    keyboard = WindowsKeyboard()
    
    print("Testing Windows API key pressing...")
    print("This will press 'I' and 'C' keys in 3 seconds...")
    time.sleep(3)
    
    keyboard.press_sequence(['i', 'c'])
    print("Key test completed!")

if __name__ == "__main__":
    test_keys()
