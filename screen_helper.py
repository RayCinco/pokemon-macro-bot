#!/usr/bin/env python3
"""
Screen Region Finder - Helper script to find coordinates
Run this to help you identify the Pokemon name region on your screen
"""

import pyautogui
import time
import os
from PIL import Image

def show_mouse_position():
    """Show current mouse position - useful for finding coordinates"""
    print("=== Mouse Position Finder ===")
    print("Move your mouse to the corners of the Pokemon name area")
    print("Press Ctrl+C to stop")
    print()
    
    try:
        while True:
            x, y = pyautogui.position()
            print(f"Mouse position: ({x}, {y})", end='\r')
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nDone!")

def test_screen_region():
    """Test a specific screen region"""
    print("=== Screen Region Tester ===")
    
    # Get region coordinates from user
    try:
        left = int(input("Enter left coordinate (x): "))
        top = int(input("Enter top coordinate (y): "))
        width = int(input("Enter width: "))
        height = int(input("Enter height: "))
        
        region = (left, top, width, height)
        print(f"Testing region: {region}")
        
        # Take screenshot of region
        screenshot = pyautogui.screenshot(region=region)
        
        # Create screenshots folder if it doesn't exist
        os.makedirs("screenshots", exist_ok=True)
        
        # Save screenshot for inspection
        filename = "screenshots/test_region.png"
        screenshot.save(filename)
        print(f"Screenshot saved as '{filename}'")
        print("Check the image to see if it captures the Pokemon name area correctly")
        
    except ValueError:
        print("Invalid input. Please enter numbers only.")
    except Exception as e:
        print(f"Error: {e}")

def take_full_screenshot():
    """Take a full screenshot for reference"""
    print("Taking full screenshot in 3 seconds...")
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    
    screenshot = pyautogui.screenshot()
    
    # Create screenshots folder if it doesn't exist
    os.makedirs("screenshots", exist_ok=True)
    
    filename = "screenshots/full_screenshot.png"
    screenshot.save(filename)
    print(f"Full screenshot saved as '{filename}'")
    print("Use this to identify coordinates for the Pokemon name area")

def main():
    """Main function"""
    print("=== Pokemon Bot - Screen Setup Helper ===")
    print()
    print("Choose an option:")
    print("1. Show mouse position (to find coordinates)")
    print("2. Test a specific screen region")
    print("3. Take full screenshot for reference")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                show_mouse_position()
            elif choice == "2":
                test_screen_region()
            elif choice == "3":
                take_full_screenshot()
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
