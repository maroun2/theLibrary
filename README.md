# The Library for EmuDeck Emulation Station

You must have Emulation Station installed first. You can find guides on Youtube and Google on how to install EmuDeck.

### Prerequisites before running the python script:
1. Go to Desktop mode
2. Open Konsole
3. Check that Python is installed:
```
python -V
```

Install packages: 

1. execute "sudo steamos-readonly disable"

2. remove the pgp check in /etc/pacman.conf with this guide: https://www.archlinuxuser.com/2012/06/ignore-signature-check-when-doing.html?m=1

3. Install packages: 
```
sudo pacman -S python-requests
sudo pacman -S python-beautifulsoup4
sudo pacman -S python-py7zr
```

### Once the libraries are successfully installed, you can run the python script in Konsole.
```
/usr/bin/python3 path/to/script.py
```

After running the script, open Steam in Desktop mode or go back to Game mode, then run Emulation Station. You will now see "The Library" in the main menu.<br />
<br />
NOTE: Make sure to change the "XXXXXX" with the correct URLs and strings in the python script. Running the script as is will not succeed. Due to legal concerns, I chose not to share the URLs I used to download roms. It's fairly easy to find the URLs on Google. Just make sure it's safe.
