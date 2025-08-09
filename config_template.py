# Pokemon Macro Bot Configuration Template
# Copy this file to 'config.py' and customize your settings

# Target Pokemon (customize these)
TARGET_POKEMON = [
    "growlithe",
    "charmander"
    # Add your target Pokemon here
]

# Screen coordinates for Pokemon name detection
# Use screen_helper.py to find the correct coordinates for your setup
POKEMON_NAME_REGION = (1495, 85, 150, 40)  # (left, top, width, height)

# Key sequences (customize for your game)
CATCH_SEQUENCE = ['f', 'e']     # Keys to catch Pokemon
ATTACK_SEQUENCE = ['e', 'e']    # Keys to attack Pokemon
ESCAPE_SEQUENCE = ['g']         # Keys to escape from unwanted Pokemon

# Timing settings (adjust for your game's responsiveness)
LONG_PRESS_DURATION = 0.2       # How long to hold movement keys
MAX_ENCOUNTER_TIME = 60          # Max time per Pokemon encounter (seconds)
ENABLE_ESCAPE = True             # Whether to escape from unwanted Pokemon

# Anti-detection settings
ENABLE_RANDOMIZATION = True      # Enable random timing variations
REST_CHANCE = 0.02              # Chance to take a break each cycle (2%)
MIN_REST_DURATION = 1.0         # Minimum rest time (seconds)
MAX_REST_DURATION = 5.0         # Maximum rest time (seconds)

# Session settings
DEFAULT_SESSION_TIME = 1200     # Default session time (20 minutes)
