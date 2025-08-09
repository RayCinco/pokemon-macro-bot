#!/usr/bin/env python3
"""
Pokemon Macro Bot - Main Scr        # Key sequence to catch Pokemon        # Long press settings
        self.use_long_press = True  # Enable long press for movement
        self.long_press_duration = 1.0  # How long to hold each key (in seconds)
        self.currently_pressed_key = None  # Track which key is currently held down
        self.movement_start_time = 0  # Track when current movement started
        self.continuous_movement = True  # Enable continuous movement without gapsstomize as needed)
        self.catch_sequence = ['I', 'C']  # Example: spacebar then enter
        
Detects Pokemon names on screen and automates catching
"""

import pyautogui
import pytesseract
from PIL import Image
import time
import cv2
import numpy as np
import os
import ctypes
import random
from loguru import logger

# Configure pyautogui
pyautogui.FAILSAFE = True  # Move mouse to top-left corner to stop
pyautogui.PAUSE = 0.1  # Small pause between actions

# Configure Tesseract path (fallback if not in PATH)
try:
    # Try to find tesseract
    import shutil
    if not shutil.which("tesseract"):
        # Common installation paths
        possible_paths = [
            r"C:\Tesseract\tesseract.exe",  # Your portable installation
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                logger.info(f"Found Tesseract at: {path}")
                break
        else:
            logger.error("Tesseract not found! Please install it.")
except Exception as e:
    logger.warning(f"Could not configure Tesseract path: {e}")

# Configure logging
logger.add("pokemon_bot.log", rotation="1 MB")



class PokemonBot:
    def __init__(self):
        """Initialize the Pokemon Bot"""
        # Pokemon names you want to catch (add more as needed)
        self.target_pokemon = [
           "growlithe","charmander",
        ]
        
        # Comprehensive list of Pokemon names for detection (add more as needed)
        self.all_pokemon_names = [
            # Your targets
            "pikachu", "charizard", "blastoise", "venusaur", "mew", "mewtwo", "dragonite", "gyarados", "oddish", "pidgey",
            # Common unwanted Pokemon (add more as you encounter them)
            "rattata", "zubat", "caterpie", "weedle", "spearow", "ekans", "sandshrew", "nidoran",
            "clefairy", "vulpix", "jigglypuff", "golbat", "psyduck", "golduck", "mankey", "primeape",
            "growlithe", "arcanine", "poliwag", "poliwhirl", "poliwrath", "abra", "kadabra", "alakazam",
            "machop", "machoke", "machamp", "bellsprout", "weepinbell", "victreebel", "tentacool", "tentacruel",
            "geodude", "graveler", "golem", "ponyta", "rapidash", "slowpoke", "slowbro", "magnemite",
            "magneton", "farfetchd", "doduo", "dodrio", "seel", "dewgong", "grimer", "muk",
            "shellder", "cloyster", "gastly", "haunter", "gengar", "onix", "drowzee", "hypno",
            "krabby", "kingler", "voltorb", "electrode", "exeggcute", "exeggutor", "cubone", "marowak",
            "hitmonlee", "hitmonchan", "lickitung", "koffing", "weezing", "rhyhorn", "rhydon", "chansey",
            "tangela", "kangaskhan", "horsea", "seadra", "goldeen", "seaking", "staryu", "starmie",
            "scyther", "jynx", "electabuzz", "magmar", "pinsir", "tauros", "magikarp", "lapras",
            "ditto", "eevee", "vaporeon", "jolteon", "flareon", "porygon", "omanyte", "omastar",
            "kabuto", "kabutops", "aerodactyl", "snorlax", "articuno", "zapdos", "moltres", "dratini",
            "dragonair", "squirtle", "wartortle","charmeleon", "bulbasaur", "ivysaur","raticate","ninetales","arcanine","ponyta","rapidash","muk","koffing","weezing","magmar","grimer"
        ]
        
        # Screen region to monitor (you'll need to adjust these coordinates)
        # Format: (left, top, width, height)
        self.pokemon_name_region = (1485, 40, 150, 50)  # Adjust this!
        
        # Key sequence to catch Pokemon (customize as needed)
        self.catch_sequence = ['f', 'e']  # Example: spacebar then enter
        
        # Key sequence to attack Pokemon before catching (customize as needed)
        self.attack_sequence = ['e', 'e']  # Example: attack moves to lower HP
        
        # Pokemon encounter tracking for attack/catch logic
        self.current_pokemon_encounter = None  # Currently engaged Pokemon
        self.attack_used_on_current = False    # Whether we've attacked this Pokemon
        self.consecutive_noise_count = 0       # Count consecutive noise detections
        self.max_noise_before_reset = 3        # Reset encounter after X noise detections
        self.last_valid_detection = None       # Last valid Pokemon name detected
        self.previous_detection = None         # Previous cycle's detection
        self.encounter_start_time = 0          # When current encounter started
        self.max_encounter_time = 60           # Max time for one encounter (seconds)
        
        # Success tracking
        self.successful_catches = 0            # Total successful target Pokemon catches
        self.total_catch_attempts = 0          # Total catch attempts made
        self.pokemon_catch_log = {}            # Track catches by Pokemon name
        self.session_start_time = time.time()  # Track session duration
        
        # Key sequence to escape from unwanted Pokemon (customize as needed)
        self.escape_sequence = ['g']  # Example: ESC then ENTER to flee
        self.enable_escape = True  # Set to False to disable escaping from unwanted Pokemon
        
        # Movement keys for running animation
        # Choose your movement style:
        self.movement_keys = ['a', 'd']  # WASD movement
        self.current_direction = 0  # Index for current movement direction
        self.steps_in_direction = 0  # How many steps taken in current direction
        self.max_steps_per_direction = 1  # Change direction every 2 steps (faster direction changes)
        
        # Long press settings with randomization
        self.use_long_press = True  # Enable long press for movement
        self.base_long_press_duration = 0.2  # Base duration (will be randomized)
        self.long_press_duration = 0.2  # Current duration (randomized each time)
        self.currently_pressed_key = None  # Track which key is currently held down
        self.movement_start_time = 0  # Track when current movement started
        self.continuous_movement = True  # Enable continuous movement without gaps
        
        # Anti-detection randomization settings
        self.enable_randomization = True  # Master switch for all randomization
        self.rest_chance = 0.02  # 2% chance to take a break each cycle (adjust as needed)
        self.min_rest_duration = 1.0  # Minimum rest time in seconds
        self.max_rest_duration = 30.0  # Maximum rest time in seconds
        self.last_rest_time = time.time()  # Track when we last rested
        self.min_time_between_rests = 30  # Minimum 30 seconds between forced rests
        
        # Movement randomization
        self.min_press_duration = 0.1  # Minimum key press duration
        self.max_press_duration = 0.4  # Maximum key press duration
        self.direction_change_variance = 0.3  # ±30% variance in direction changes
        
        # Action timing randomization
        self.min_action_delay = 0.3  # Minimum delay between actions
        self.max_action_delay = 0.6  # Maximum delay between actions
        self.min_key_delay = 0.05  # Minimum delay between key presses
        self.max_key_delay = 0.1  # Maximum delay between key presses
        
        # Windows API key codes
        self.vk_codes = {
            'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45, 'f': 0x46, 'g': 0x47,
            'h': 0x48, 'i': 0x49, 'j': 0x4A, 'k': 0x4B, 'l': 0x4C, 'm': 0x4D, 'n': 0x4E,
            'o': 0x4F, 'p': 0x50, 'q': 0x51, 'r': 0x52, 's': 0x53, 't': 0x54, 'u': 0x55,
            'v': 0x56, 'w': 0x57, 'x': 0x58, 'y': 0x59, 'z': 0x5A,
            'space': 0x20, 'enter': 0x0D, 'tab': 0x09, 'esc': 0x1B,
            'up': 0x26, 'down': 0x28, 'left': 0x25, 'right': 0x27  # Arrow keys
        }
        self.user32 = ctypes.windll.user32
        
        logger.info("Pokemon Bot initialized with randomization features")
    
    def configure_randomization(self, enabled=True, rest_chance=0.02, min_rest=1.0, max_rest=5.0, 
                              min_press=0.1, max_press=0.4):
        """Configure randomization settings for anti-detection"""
        self.enable_randomization = enabled
        self.rest_chance = rest_chance
        self.min_rest_duration = min_rest
        self.max_rest_duration = max_rest
        self.min_press_duration = min_press
        self.max_press_duration = max_press
        
        logger.info(f"Randomization configured: enabled={enabled}, rest_chance={rest_chance*100:.1f}%")
    
    def get_random_duration(self, base_duration, variance=0.3):
        """Get a randomized duration with variance"""
        if not self.enable_randomization:
            return base_duration
        
        min_duration = base_duration * (1 - variance)
        max_duration = base_duration * (1 + variance)
        return random.uniform(min_duration, max_duration)
    
    def get_random_press_duration(self):
        """Get a randomized key press duration"""
        if not self.enable_randomization:
            return self.base_long_press_duration
        
        return random.uniform(self.min_press_duration, self.max_press_duration)
    
    def get_random_delay(self, delay_type="action"):
        """Get a randomized delay between actions"""
        if not self.enable_randomization:
            return 0.1
        
        if delay_type == "action":
            return random.uniform(self.min_action_delay, self.max_action_delay)
        elif delay_type == "key":
            return random.uniform(self.min_key_delay, self.max_key_delay)
        else:
            return random.uniform(0.05, 0.2)
    
    def should_take_rest(self):
        """Determine if the bot should take a break"""
        if not self.enable_randomization:
            return False
        
        current_time = time.time()
        
        # Force a rest if it's been too long
        time_since_last_rest = current_time - self.last_rest_time
        if time_since_last_rest > self.min_time_between_rests * 2:  # Double the minimum time = forced rest
            logger.info("Forcing rest break (been too long since last rest)")
            return True
        
        # Random chance for rest (but not too soon after last rest)
        if time_since_last_rest > self.min_time_between_rests:
            return random.random() < self.rest_chance
        
        return False
    
    def take_rest_break(self):
        """Take a randomized rest break"""
        if not self.enable_randomization:
            return
        
        # Stop any current movement
        self.release_current_key()
        
        # Random rest duration
        rest_duration = random.uniform(self.min_rest_duration, self.max_rest_duration)
        
        logger.info(f"Taking rest break for {rest_duration:.1f} seconds...")
        time.sleep(rest_duration)
        
        self.last_rest_time = time.time()
        logger.info("Rest break completed")
    
    def randomize_movement_settings(self):
        """Randomize movement settings for this cycle"""
        if not self.enable_randomization:
            return
        
        # Randomize press duration
        self.long_press_duration = self.get_random_press_duration()
        
        # Sometimes change direction change frequency
        if random.random() < 0.1:  # 10% chance to change pattern
            self.max_steps_per_direction = random.randint(1, 3)
    
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
    
    def save_debug_screenshot(self, image, detected_text="", is_target=False):
        """Save screenshot for debugging purposes"""
        try:
            # Create screenshots folder if it doesn't exist
            os.makedirs("screenshots", exist_ok=True)
            
            # Use fixed filenames that overwrite previous screenshots
            if is_target:
                filename = "screenshots/latest_TARGET_detection.png"
            else:
                filename = "screenshots/latest_detection.png"
            
            image.save(filename)
            
        except Exception as e:
            logger.error(f"Failed to save debug screenshot: {e}")
    
    def extract_text_from_image(self, image):
        """Extract text from image using OCR"""
        try:
            # Convert PIL image to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Convert to grayscale for better OCR
            gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
            
            # Apply some image processing to improve OCR
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            
            # Extract text using pytesseract
            text = pytesseract.image_to_string(gray, config='--psm 8')
            return text.strip().lower()
        
        except Exception as e:
            logger.error(f"Failed to extract text: {e}")
            return ""
    
    def is_target_pokemon(self, detected_text):
        """Check if detected text contains a target Pokemon name"""
        for pokemon in self.target_pokemon:
            if pokemon.lower() in detected_text.lower():
                logger.info(f"Target Pokemon detected: {pokemon}")
                return True, pokemon
        return False, None
    
    def detect_any_pokemon(self, detected_text):
        """Detect if any Pokemon is present (target or unwanted) with smart filtering"""
        # Clean the detected text
        cleaned_text = detected_text.strip().lower()
        
        # Filter out obvious OCR noise
        if not cleaned_text or len(cleaned_text) < 3:
            return "none", None
        
        # Filter out common OCR artifacts
        noise_patterns = [
            # Common OCR mistakes
            "fee ee ee", "ooo", "|||", "...", "---", "___",
            # Repeated characters (likely noise)
            "aaa", "eee", "iii", "ooo", "uuu",
            # Single letters repeated
            "a a a", "e e e", "i i i", "o o o",
            # Numbers (Pokemon names don't contain numbers)
            "123", "456", "789", "000", "111",
            # Special characters only
            "!!!", "???", "@@@", "###", "$$$"
        ]
        
        # Check if it's just noise
        for noise in noise_patterns:
            if noise in cleaned_text or cleaned_text == noise:
                return "none", None
        
        # First check if it's a target Pokemon
        is_target, pokemon_name = self.is_target_pokemon(detected_text)
        if is_target:
            return "target", pokemon_name
        
        # Check if it matches any known Pokemon name (fuzzy matching)
        for pokemon in self.all_pokemon_names:
            # Exact match
            if pokemon in cleaned_text or cleaned_text in pokemon:
                logger.info(f"Unwanted Pokemon detected: '{pokemon}' (from text: '{cleaned_text}')")
                return "unwanted", pokemon
            
            # Fuzzy match (allow for small OCR errors)
            if len(pokemon) >= 4 and len(cleaned_text) >= 4:
                # Check if at least 70% of characters match
                match_score = self.calculate_similarity(pokemon, cleaned_text)
                if match_score > 0.7:
                    logger.info(f"Unwanted Pokemon detected (fuzzy): '{pokemon}' (from text: '{cleaned_text}', similarity: {match_score:.2f})")
                    return "unwanted", pokemon
        
        # If text looks like it could be a Pokemon name but we don't recognize it
        if (len(cleaned_text) >= 4 and 
            cleaned_text.isalpha() and  # Only letters
            not any(char * 3 in cleaned_text for char in 'abcdefghijklmnopqrstuvwxyz')):  # No triple letters
            logger.warning(f"Unknown Pokemon-like text detected: '{cleaned_text}' - Add to pokemon list if this is a real Pokemon")
            return "unknown", cleaned_text
        
        return "none", None
    
    def calculate_similarity(self, str1, str2):
        """Calculate similarity between two strings (simple version)"""
        if not str1 or not str2:
            return 0.0
        
        # Simple character-based similarity
        longer = str1 if len(str1) >= len(str2) else str2
        shorter = str2 if len(str1) >= len(str2) else str1
        
        if len(longer) == 0:
            return 1.0
        
        matches = sum(1 for i, char in enumerate(shorter) if i < len(longer) and char == longer[i])
        return matches / len(longer)
    
    def press_key_windows_api(self, key):
        """Press a key using Windows API (more reliable for games) with randomization"""
        key = key.lower()
        if key not in self.vk_codes:
            logger.error(f"Key '{key}' not supported")
            return False
            
        vk_code = self.vk_codes[key]
        
        # Randomized key press timing
        press_duration = self.get_random_delay("key") if self.enable_randomization else 0.05
        
        # Key down
        self.user32.keybd_event(vk_code, 0, 0, 0)
        time.sleep(press_duration)
        
        # Key up  
        self.user32.keybd_event(vk_code, 0, 2, 0)
        return True

    def hold_key_down(self, key):
        """Hold a key down using Windows API"""
        key = key.lower()
        if key not in self.vk_codes:
            logger.error(f"Key '{key}' not supported for long press")
            return False
            
        vk_code = self.vk_codes[key]
        
        # Key down (and keep it down)
        self.user32.keybd_event(vk_code, 0, 0, 0)
        self.currently_pressed_key = key
        return True
    
    def release_key(self, key):
        """Release a key that was being held down"""
        key = key.lower()
        if key not in self.vk_codes:
            logger.error(f"Key '{key}' not supported for release")
            return False
            
        vk_code = self.vk_codes[key]
        
        # Key up
        self.user32.keybd_event(vk_code, 0, 2, 0)
        self.currently_pressed_key = None
        return True
    
    def release_current_key(self):
        """Release whatever key is currently being held down"""
        if self.currently_pressed_key:
            self.release_key(self.currently_pressed_key)

    def move_character(self):
        """Move character in a pattern with continuous movement and randomization"""
        try:
            # Randomize movement settings occasionally
            self.randomize_movement_settings()
            
            # Get current movement direction
            current_key = self.movement_keys[self.current_direction]
            
            if self.use_long_press and self.continuous_movement:
                # Continuous movement - always keep a key pressed
                current_time = time.time()
                
                # If no key is currently pressed, start pressing one
                if not self.currently_pressed_key:
                    if self.hold_key_down(current_key):
                        self.movement_start_time = current_time
                    else:
                        # Fallback to pyautogui
                        pyautogui.keyDown(current_key)
                        self.currently_pressed_key = current_key
                        self.movement_start_time = current_time
                
                # Check if it's time to switch direction
                elif current_time - self.movement_start_time >= self.long_press_duration:
                    # Time to switch to next direction
                    old_key = self.currently_pressed_key
                    
                    # Change direction
                    self.current_direction = (self.current_direction + 1) % len(self.movement_keys)
                    new_key = self.movement_keys[self.current_direction]
                    
                    # Instantly switch keys (no gap)
                    self.release_key(old_key)  # Release old key
                    if self.hold_key_down(new_key):  # Immediately press new key
                        self.movement_start_time = current_time
                    else:
                        # Fallback to pyautogui
                        pyautogui.keyDown(new_key)
                        self.currently_pressed_key = new_key
                        self.movement_start_time = current_time
                
                # No sleep here! Continuous movement
                return True
                
            elif self.use_long_press:
                # Original long press with gaps
                # Release any currently pressed key if switching directions
                if self.currently_pressed_key and self.currently_pressed_key != current_key:
                    self.release_current_key()
                
                # Hold down the new key
                if not self.currently_pressed_key or self.currently_pressed_key != current_key:
                    if self.hold_key_down(current_key):
                        pass
                    else:
                        # Fallback to pyautogui
                        pyautogui.keyDown(current_key)
                        self.currently_pressed_key = current_key
                
                # Wait for the long press duration
                time.sleep(self.long_press_duration)
                
                # Release the key
                self.release_current_key()
                
                self.steps_in_direction += 1
                
                # Change direction after max steps
                if self.steps_in_direction >= self.max_steps_per_direction:
                    self.current_direction = (self.current_direction + 1) % len(self.movement_keys)
                    self.steps_in_direction = 0
                
            else:
                # Normal single key press
                if self.press_key_windows_api(current_key):
                    pass
                else:
                    pyautogui.press(current_key)
                
                self.steps_in_direction += 1
                
                # Change direction after max steps
                if self.steps_in_direction >= self.max_steps_per_direction:
                    self.current_direction = (self.current_direction + 1) % len(self.movement_keys)
                    self.steps_in_direction = 0
            
            return True
        except Exception as e:
            logger.error(f"Failed to move character: {e}")
            # Make sure to release any stuck keys
            self.release_current_key()
            return False

    def execute_catch_sequence(self):
        """Execute the key sequence to catch Pokemon with randomized timing"""
        try:
            # Stop any movement before catching
            self.release_current_key()
            
            logger.info("Executing catch sequence...")
            
            # Randomized initial delay
            initial_delay = self.get_random_delay("action") if self.enable_randomization else 0.5
            time.sleep(12.0)
            
            for i, key in enumerate(self.catch_sequence):
                # Try Windows API first, fallback to pyautogui
                if not self.press_key_windows_api(key):
                    logger.warning(f"Windows API failed for {key}, trying pyautogui...")
                    pyautogui.press(key)
                
                # Randomized delay between keys (except after last key)
                if i < len(self.catch_sequence) - 1:
                    delay = self.get_random_delay("action") if self.enable_randomization else 0.4
                    time.sleep(delay)
            
            logger.info("Catch sequence completed")
            return True
        except Exception as e:
            logger.error(f"Failed to execute catch sequence: {e}")
            # Make sure to release any stuck keys
            self.release_current_key()
            return False

    def execute_escape_sequence(self):
        """Execute the key sequence to escape from unwanted Pokemon with randomized timing"""
        try:
            # Stop any movement before escaping
            self.release_current_key()
            
            logger.info("Executing escape sequence...")
            
            # Add a small delay to ensure game window is ready
            time.sleep(2)
            logger.info("Executing escape sequence...")
            
            # Randomized initial delay
            initial_delay = self.get_random_delay("action") if self.enable_randomization else 0.5
            time.sleep(initial_delay)
            
            for i, key in enumerate(self.escape_sequence):
                # Try Windows API first, fallback to pyautogui
                if not self.press_key_windows_api(key):
                    logger.warning(f"Windows API failed for {key}, trying pyautogui...")
                    pyautogui.press(key)
                
                # Randomized delay between keys (except after last key)
                if i < len(self.escape_sequence) - 1:
                    delay = self.get_random_delay("action") if self.enable_randomization else 0.4
                    time.sleep(delay)
            
            logger.info("Escape sequence completed")
            return True
        except Exception as e:
            logger.error(f"Failed to execute escape sequence: {e}")
            # Make sure to release any stuck keys
            self.release_current_key()
            return False
    
    def execute_attack_sequence(self):
        """Execute the key sequence to attack Pokemon (lower HP before catching)"""
        try:
            # Stop any movement before attacking
            self.release_current_key()
            
            logger.info("Executing attack sequence to lower Pokemon HP...")
            
            # 5-second delay before attacking
            logger.info("Waiting 5 seconds before attacking...")
            time.sleep(4.0)
            
            # Randomized initial delay
            initial_delay = self.get_random_delay("action") if self.enable_randomization else 0.5
            time.sleep(initial_delay)
            
            for i, key in enumerate(self.attack_sequence):
                # Try Windows API first, fallback to pyautogui
                if not self.press_key_windows_api(key):
                    logger.warning(f"Windows API failed for {key}, trying pyautogui...")
                    pyautogui.press(key)
                
                # Randomized delay between keys (except after last key)
                if i < len(self.attack_sequence) - 1:
                    delay = self.get_random_delay("action") if self.enable_randomization else 0.4
                    time.sleep(delay)
            
            logger.info("Attack sequence completed")
            return True
        except Exception as e:
            logger.error(f"Failed to execute attack sequence: {e}")
            # Make sure to release any stuck keys
            self.release_current_key()
            return False
    
    def reset_encounter(self):
        """Reset the current Pokemon encounter tracking"""
        if self.current_pokemon_encounter:
            logger.info(f"Resetting encounter with {self.current_pokemon_encounter}")
        
        self.current_pokemon_encounter = None
        self.attack_used_on_current = False
        self.consecutive_noise_count = 0
        self.last_valid_detection = None
        self.previous_detection = None
        self.encounter_start_time = 0
    
    def start_new_encounter(self, pokemon_name):
        """Start tracking a new Pokemon encounter"""
        self.current_pokemon_encounter = pokemon_name
        self.attack_used_on_current = False
        self.consecutive_noise_count = 0
        self.last_valid_detection = pokemon_name
        self.encounter_start_time = time.time()
        logger.info(f"Started new encounter with {pokemon_name}")
    
    def should_reset_encounter(self, detected_type, pokemon_name=None):
        """Determine if we should reset the current encounter"""
        current_time = time.time()
        
        # Reset if encounter has been going too long
        if (self.encounter_start_time > 0 and 
            current_time - self.encounter_start_time > self.max_encounter_time):
            logger.info("Resetting encounter due to timeout")
            return True
        
        # Reset if we've had too many consecutive noise detections
        if detected_type == "none":
            self.consecutive_noise_count += 1
            if self.consecutive_noise_count >= self.max_noise_before_reset:
                logger.info("Resetting encounter due to consecutive noise")
                return True
        else:
            self.consecutive_noise_count = 0  # Reset noise counter on valid detection
        
        # Reset if we detect a different Pokemon
        if (detected_type == "target" and pokemon_name and 
            self.current_pokemon_encounter and 
            pokemon_name != self.current_pokemon_encounter):
            logger.info(f"Resetting encounter: different Pokemon detected ({pokemon_name} vs {self.current_pokemon_encounter})")
            return True
        
        return False
    
    def record_successful_catch(self, pokemon_name):
        """Record a successful Pokemon catch"""
        self.successful_catches += 1
        
        # Track by individual Pokemon name
        if pokemon_name in self.pokemon_catch_log:
            self.pokemon_catch_log[pokemon_name] += 1
        else:
            self.pokemon_catch_log[pokemon_name] = 1
        
        logger.success(f"✅ Successfully caught {pokemon_name}! (Total catches: {self.successful_catches})")
        logger.info(f"📊 {pokemon_name} catch count: {self.pokemon_catch_log[pokemon_name]}")
    
    def record_catch_attempt(self):
        """Record a catch attempt"""
        self.total_catch_attempts += 1
    
    def get_catch_statistics(self):
        """Get current catch statistics"""
        session_time = time.time() - self.session_start_time
        hours = int(session_time // 3600)
        minutes = int((session_time % 3600) // 60)
        
        stats = {
            'total_catches': self.successful_catches,
            'total_attempts': self.total_catch_attempts,
            'catch_rate': (self.successful_catches / max(self.total_catch_attempts, 1)) * 100,
            'session_time': f"{hours}h {minutes}m",
            'catches_per_hour': (self.successful_catches / max(session_time / 3600, 0.1)),
            'pokemon_breakdown': self.pokemon_catch_log.copy()
        }
        return stats
    
    def print_catch_statistics(self):
        """Print detailed catch statistics"""
        stats = self.get_catch_statistics()
        
        logger.info("=" * 50)
        logger.info("📈 CATCH STATISTICS")
        logger.info("=" * 50)
        logger.info(f"🎯 Total Successful Catches: {stats['total_catches']}")
        logger.info(f"🎲 Total Catch Attempts: {stats['total_attempts']}")
        logger.info(f"📊 Success Rate: {stats['catch_rate']:.1f}%")
        logger.info(f"⏱️  Session Time: {stats['session_time']}")
        logger.info(f"⚡ Catches per Hour: {stats['catches_per_hour']:.1f}")
        
        if stats['pokemon_breakdown']:
            logger.info("🔥 Pokemon Breakdown:")
            for pokemon, count in sorted(stats['pokemon_breakdown'].items(), key=lambda x: x[1], reverse=True):
                logger.info(f"   • {pokemon}: {count} catches")
        
        logger.info("=" * 50)
    
    def run_detection_cycle(self):
        """Run one detection cycle"""
        # Take screenshot of Pokemon name area
        screenshot = self.take_screenshot(region=self.pokemon_name_region)
        
        if screenshot is None:
            return False
        
        # Extract text from screenshot
        detected_text = self.extract_text_from_image(screenshot)
        # Only log detected text when it's not empty or noise
        if detected_text and len(detected_text.strip()) > 2:
            logger.debug(f"Detected text: '{detected_text}'")
        
        # Check what type of Pokemon (if any) was detected
        pokemon_type, pokemon_name = self.detect_any_pokemon(detected_text)
        
        # Save debug screenshot
        is_target = (pokemon_type == "target")
        self.save_debug_screenshot(screenshot, detected_text, is_target)
        
        # Determine if this is a new encounter based on detection changes
        should_reset = False
        
        if pokemon_type == "none":
            # Noise detected - this means the previous Pokemon was caught/fled
            if self.current_pokemon_encounter:
                logger.info(f"Noise detected - {self.current_pokemon_encounter} was caught/fled!")
                # Record successful catch if it was a target Pokemon
                if self.current_pokemon_encounter in self.target_pokemon:
                    self.record_successful_catch(self.current_pokemon_encounter)
                should_reset = True
        elif pokemon_type == "target":
            # Target Pokemon detected
            if self.current_pokemon_encounter and pokemon_name != self.current_pokemon_encounter:
                # Different Pokemon detected - previous one was caught
                logger.info(f"Different Pokemon detected: {pokemon_name} vs {self.current_pokemon_encounter} - previous was caught!")
                # Record successful catch for the previous Pokemon
                if self.current_pokemon_encounter in self.target_pokemon:
                    self.record_successful_catch(self.current_pokemon_encounter)
                should_reset = True
        
        # Check for timeout
        if (self.current_pokemon_encounter and 
            time.time() - self.encounter_start_time > self.max_encounter_time):
            logger.info("Encounter timeout - resetting")
            should_reset = True
        
        if should_reset:
            self.reset_encounter()
        
        if pokemon_type == "target":
            logger.success(f"Found target Pokemon: {pokemon_name}!")
            
            # Check if this is a new encounter or continuing current one
            if not self.current_pokemon_encounter:
                # New encounter - start tracking
                self.start_new_encounter(pokemon_name)
            
            # Decide whether to attack first or just catch
            if not self.attack_used_on_current:
                # First time seeing this Pokemon - attack to lower HP
                logger.info(f"First encounter with {pokemon_name} - attacking to lower HP")
                if self.execute_attack_sequence():
                    self.attack_used_on_current = True
                    # Wait a bit after attacking before trying to catch
                    attack_wait = self.get_random_duration(2.0, 0.3) if self.enable_randomization else 2.0
                    time.sleep(attack_wait)
                return False  # Don't count as success, continue to catch phase
            else:
                # Already attacked this Pokemon - now try to catch
                logger.info(f"Attempting to catch {pokemon_name} (HP already lowered)")
                self.record_catch_attempt()  # Track the attempt
                self.execute_catch_sequence()
                # Don't reset encounter here - let noise detection handle it
                return False  # Continue checking to see if Pokemon was caught
                
        elif pokemon_type == "unwanted" and self.enable_escape:
            logger.warning(f"Found unwanted Pokemon: {pokemon_name}! Escaping...")
            self.reset_encounter()  # Reset encounter when escaping
            self.execute_escape_sequence()
            return False  # Continue searching after escaping
            
        elif pokemon_type == "unknown":
            logger.info(f"Unknown Pokemon-like text: '{pokemon_name}' - ignoring for now")
            return False
        
        # Update previous detection for next cycle
        self.previous_detection = (pokemon_type, pokemon_name)
        
        # No Pokemon detected or just noise
        return False
    
    def start_bot(self, duration_seconds=60):
        """Start the Pokemon bot for specified duration with anti-detection features"""
        logger.info(f"Starting Pokemon Bot for {duration_seconds} seconds...")
        logger.info(f"Randomization enabled: {self.enable_randomization}")
        logger.info("Move mouse to top-left corner to emergency stop")
        
        start_time = time.time()
        catches = 0
        cycles = 0
        
        try:
            while time.time() - start_time < duration_seconds:
                cycles += 1
                
                # Print statistics every 1000 cycles (roughly every few minutes)
                if cycles % 1000 == 0:
                    logger.info(f"🔄 Cycle {cycles} - Quick Stats: {self.successful_catches} catches, {self.total_catch_attempts} attempts")
                
                # Check if we should take a rest break
                if self.should_take_rest():
                    self.take_rest_break()
                
                detection_result = self.run_detection_cycle()
                
                if detection_result:
                    catches += 1
                    # Randomized delay after catching
                    post_catch_delay = self.get_random_duration(2.0, 0.5) if self.enable_randomization else 2.0
                    logger.debug(f"Waiting {post_catch_delay:.1f}s after catch")
                    time.sleep(post_catch_delay)
                else:
                    # No Pokemon found, move to search for more
                    self.move_character()
                
                # Randomized checking interval
                check_interval = self.get_random_duration(0.01, 0.5) if self.enable_randomization else 0.01
                time.sleep(check_interval)
                
        except pyautogui.FailSafeException:
            logger.warning("Emergency stop activated!")
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        finally:
            # Make sure to release any held keys
            self.release_current_key()
        
        # Print final detailed statistics
        logger.info("🏁 Session Complete!")
        self.print_catch_statistics()
        
        logger.info(f"Bot session ended. Detection cycles: {cycles}")
        if self.enable_randomization:
            logger.info("Anti-detection randomization was active during this session")



def main():
    """Main function"""
    print("=== Pokemon Macro Bot with Smart Attack/Catch System ===")
    print("Before starting:")
    print("1. Open your Pokemon game")
    print("2. Adjust the pokemon_name_region coordinates in the code")
    print("3. Customize target_pokemon list")
    print("4. Set up your attack_sequence and catch_sequence keys")
    print("\n⚔️ Smart Combat Features:")
    print("   - Attacks Pokemon first to lower HP")
    print("   - Tracks encounters to avoid repeated attacks")
    print("   - Multiple catch attempts per Pokemon")
    print("   - Automatic encounter reset after noise/timeout")
    print("\n🔒 Anti-Detection Features Enabled:")
    print("   - Randomized key press timings")
    print("   - Random rest breaks")
    print("   - Variable movement patterns")
    print("   - Randomized action delays")
    print("\nPress Enter to start (or Ctrl+C to exit)...")
    
    try:
        input()
        bot = PokemonBot()
        
        # Optional: Configure randomization (uncomment to customize)
        # bot.configure_randomization(
        #     enabled=True,           # Enable/disable all randomization
        #     rest_chance=0.03,       # 3% chance for rest each cycle
        #     min_rest=2.0,           # Minimum rest time (seconds)
        #     max_rest=8.0,           # Maximum rest time (seconds)
        #     min_press=0.08,         # Minimum key press duration
        #     max_press=0.5           # Maximum key press duration
        # )

        bot.start_bot(duration_seconds=3600)  # Run for 60 minutes initially
    except KeyboardInterrupt:
        print("\nBot cancelled by user")

if __name__ == "__main__":
    main()
