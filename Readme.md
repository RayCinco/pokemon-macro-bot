# Pokemon Macro Bot

An automated Pokemon catching bot that uses screen capture and OCR to detect Pokemon and execute catch sequences.

## 🚀 Features

- **Smart Attack/Catch System**: Attacks Pokemon first to lower HP, then attempts multiple catches
- **Encounter Tracking**: Avoids repeating attacks on the same Pokemon
- **Anti-Detection**: Randomized timing, rest breaks, and human-like behavior
- **OCR-Based Detection**: Uses screen capture and text recognition (no memory hacking)
- **Comprehensive Statistics**: Track success rates and Pokemon catch counts
- **Configurable**: Easily customize for different games and setups

## 📋 Requirements

- Python 3.11+ (tested with 3.11.9)
- Tesseract OCR
- Required packages (see requirements.txt)

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/YourUsername/pokemon-macro-bot.git
   cd pokemon-macro-bot
   ```

2. **Create virtual environment**

   ```bash
   python -m venv pokemon-macro-env
   # On Windows:
   pokemon-macro-env\Scripts\activate
   # On Linux/Mac:
   source pokemon-macro-env/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Tesseract OCR**
   - Windows: Download from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   - Linux: `sudo apt install tesseract-ocr`
   - Mac: `brew install tesseract`

## ⚙️ Configuration

1. **Copy the configuration template**

   ```bash
   cp config_template.py config.py
   ```

2. **Find your screen coordinates**

   ```bash
   python screen_helper.py
   ```

   Use this tool to find the exact coordinates where Pokemon names appear on your screen.

3. **Customize settings in config.py**
   - Set your target Pokemon list
   - Configure screen coordinates
   - Set key sequences for your game
   - Adjust timing and behavior settings

## 🎮 Usage

1. **Open your Pokemon game**
2. **Position the game window** where the bot can capture Pokemon names
3. **Run the bot**
   ```bash
   python main.py
   ```

## 🔧 Key Files

- `main.py` - Main bot application with smart attack/catch system
- `config_template.py` - Configuration template (copy to config.py)
- `screen_helper.py` - Tool to find screen coordinates
- `requirements.txt` - Python dependencies
- `test_bot.py` - Testing utilities
- `windows_keyboard.py` - Windows-specific keyboard handling

## 📊 Features in Detail

### Smart Combat System

- Attacks Pokemon once to lower HP for better catch rates
- Multiple catch attempts per Pokemon
- Tracks encounters to avoid repeated attacks
- Automatic encounter reset when Pokemon is caught/fled

### Anti-Detection

- Randomized key press timings
- Random rest breaks during operation
- Variable movement patterns
- Human-like inconsistencies in behavior

### Statistics Tracking

- Success rate monitoring
- Individual Pokemon catch counts
- Session time and efficiency metrics
- Detailed end-of-session reports

### OCR Detection

- Real-time screen capture
- Noise filtering for accurate Pokemon name detection
- Comprehensive Pokemon name database
- Smart text recognition with confidence scoring

## ⚠️ Disclaimer

This tool is for educational purposes only. Use responsibly and in accordance with the terms of service of any games you play. The authors are not responsible for any consequences of using this software.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🛡️ Safety Notes

- Always test in a safe environment first
- Don't run for extended periods without breaks
- Monitor the bot's behavior and adjust settings as needed
- Use reasonable session times to avoid detection
- Configure appropriate rest breaks and randomization
