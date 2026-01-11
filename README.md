# The Library for EmuDeck / ES-DE

Browse and download ROMs directly from your Steam Deck's Emulation Station interface.

## Installation (Steam Deck)

1. Open Desktop mode and Konsole

2. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/theLibrary.git ~/theLibrary
   cd ~/theLibrary
   ```

3. Run the install script:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

4. Run the library generator:
   ```bash
   ~/theLibrary/venv/bin/python3 theLibrary.py
   ```

## Testing

Test the connection and parsing before generating the full library:
```bash
~/theLibrary/venv/bin/python3 theLibrary.py --test
```

## Usage

After running the script:
1. Open ES-DE (Emulation Station)
2. You'll see "The Library" in the main menu
3. Browse consoles and select a game
4. The game will download automatically and be ready to play

## Supported Consoles

- SNES (Super Nintendo)
- NES (Nintendo Entertainment System)
- N64 (Nintendo 64)
- Game Boy / Game Boy Color / Game Boy Advance
- Sega Genesis / Master System / Game Gear
- PlayStation / PS2 / PSP

## Troubleshooting

**"Module not found" errors:**
Make sure you ran `./install.sh` and are using the venv Python:
```bash
~/theLibrary/venv/bin/python3 theLibrary.py
```

**Downloads not working:**
Test the connection first:
```bash
~/theLibrary/venv/bin/python3 theLibrary.py --test
```

**Regenerate library after updates:**
Simply run the script again to update the game list:
```bash
~/theLibrary/venv/bin/python3 theLibrary.py
```

## Uninstall

To completely remove The Library:
```bash
# Remove launcher files
rm -rf ~/Emulation/roms/thelibrary

# Remove the project and venv
rm -rf ~/theLibrary
```

Then manually remove the Library entry from `~/ES-DE/custom_systems/es_systems.xml` (delete the `<system>` block with `<name>Library</name>`).
