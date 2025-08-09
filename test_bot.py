#!/usr/bin/env python3
"""
Pokemon Bot - Test Version (No OCR)
Tests screen capture without text recognition
"""

import pyautogui
from PIL import Image
import time
import os
from loguru import logger

# Configure pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

# Configure logging
logger.add("pokemon_bot_test.log", rotation="1 MB")

class PokemonBotTest:
    def __init__(self):
        """Initialize the test bot"""
        # Screen region to monitor (adjust these coordinates)
        self.pokemon_name_region = (1490, 85, 150, 50)  # From your screen_helper tests
        
        logger.info("Pokemon Bot Test initialized")
    
    def take_screenshot(self, region=None):
        """Take a screenshot of specified region"""
        try:
            if region:
                screenshot = pyautogui.screenshot(region=region)
            else:
                screenshot = pyautogui.screenshot()
            return screenshot
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return None
    
    def save_screenshot_for_inspection(self):
        """Save screenshot for manual inspection"""
        screenshot = self.take_screenshot(region=self.pokemon_name_region)
        
        if screenshot:
            # Create screenshots folder if it doesn't exist
            os.makedirs("screenshots", exist_ok=True)
            
            # Save with timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshots/pokemon_region_{timestamp}.png"
            screenshot.save(filename)
            logger.info(f"Screenshot saved as '{filename}'")
            print(f"Screenshot saved: {filename}")
            print("Check this image to see if it captures the Pokemon name correctly")
        
        return screenshot is not None
    
    def run_test_cycle(self, duration_seconds=30):
        """Run test for specified duration"""
        logger.info(f"Starting Pokemon Bot Test for {duration_seconds} seconds...")
        print("=== Pokemon Bot Test Mode ===")
        print("This will capture screenshots of your Pokemon name region")
        print("Press Ctrl+C to stop early")
        
        start_time = time.time()
        screenshot_count = 0
        
        try:
            while time.time() - start_time < duration_seconds:
                if self.save_screenshot_for_inspection():
                    screenshot_count += 1
                
                print(f"Screenshots taken: {screenshot_count}")
                time.sleep(5)  # Take screenshot every 5 seconds
                
        except KeyboardInterrupt:
            logger.info("Test stopped by user")
            print("\nTest stopped by user")
        
        print(f"\nTest completed. Total screenshots: {screenshot_count}")
        print("Check the screenshots folder to verify your region captures Pokemon names")

def main():
    """Main function"""
    print("=== Pokemon Bot - Test Mode ===")
    print("This test version captures screenshots without OCR")
    print("Use this to verify your screen region is correct")
    print("\nBefore starting:")
    print("1. Open your Pokemon game")
    print("2. Make sure Pokemon names are visible")
    print("3. The bot will capture the region every 5 seconds")
    print("\nPress Enter to start test (or Ctrl+C to exit)...")
    
    try:
        input()
        bot = PokemonBotTest()
        bot.run_test_cycle(duration_seconds=30)
    except KeyboardInterrupt:
        print("\nTest cancelled by user")

if __name__ == "__main__":
    main()
