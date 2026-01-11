import os
import argparse
import requests
from bs4 import BeautifulSoup


# Console configuration: maps console name to its ROM source URL (Myrient)
CONSOLES = {
    'snes': 'https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Super%20Nintendo%20Entertainment%20System/',
    'nes': 'https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20Entertainment%20System%20(Headered)/',
    'n64': 'https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%2064%20(BigEndian)/',
    'gb': 'https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy/',
    'gbc': 'https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Color/',
    'gba': 'https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Advance/',
    'genesis': 'https://myrient.erista.me/files/No-Intro/Sega%20-%20Mega%20Drive%20-%20Genesis/',
    'mastersystem': 'https://myrient.erista.me/files/No-Intro/Sega%20-%20Master%20System%20-%20Mark%20III/',
    'gamegear': 'https://myrient.erista.me/files/No-Intro/Sega%20-%20Game%20Gear/',
    'psx': 'https://myrient.erista.me/files/No-Intro/Non-Redump%20-%20Sony%20-%20PlayStation/',
    'ps2': 'https://myrient.erista.me/files/No-Intro/Non-Redump%20-%20Sony%20-%20PlayStation%202/',
    'psp': 'https://myrient.erista.me/files/No-Intro/Sony%20-%20PlayStation%20Portable%20(PSN)%20(Decrypted)/',
}


def parse_arguments():
    parser = argparse.ArgumentParser(description='ROM Library Manager')
    parser.add_argument('--test', '-t', action='store_true',
                        help='Test URL connection and parsing')
    return parser.parse_args()


def fetch_and_parse_games(url):
    """Fetch URL and parse games list. Returns (success, games_list, error_message)."""
    try:
        response = requests.get(url)
    except requests.RequestException as e:
        return (False, [], f"Request failed: {e}")

    if response.status_code != 200:
        return (False, [], f"Request failed with status code: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=True)

    usaTag = '(USA'
    excludedWords = ['(Beta)', '(Beta 1)', '(Beta 2)', '(Beta 3)', '(Rev 1)', '(Arcade)', '(Proto)', '(Proto 1)', '(Proto 2)', '(Sample)', '(Rev 2)', '(Rev 3)', '(Competition Cart', '(Pirate)', '(Demo)']

    zip_links = []
    for link in links:
        if link['href'].endswith('.zip') and usaTag in link.text:
            zip_links.append(link.text)
        elif link['href'].endswith('.7z') and usaTag in link.text:
            zip_links.append(link.text)

    cleaned_list = []
    for link in zip_links:
        if not any(w in link for w in excludedWords):
            if '.7z' in link:
                link = link.rstrip('.7z')
                cleaned_list.append(link)
            elif '.zip' in link:
                link = link.rstrip('.zip')
                cleaned_list.append(link)

    return (True, cleaned_list, None)


def read_files(console_name):
    """Process a console and create .py launcher files for each game."""
    if console_name not in CONSOLES:
        print(f"Console '{console_name}' not found in CONSOLES config.")
        return

    url = CONSOLES[console_name]
    if url == 'XXXXXXX':
        print(f"Skipping {console_name}: URL not configured.")
        return

    # Use shared parsing function
    success, cleaned_list, error = fetch_and_parse_games(url)

    if not success:
        print(error)
        return

    theLibraryPath = os.path.expanduser('~/Emulation/roms/thelibrary')
    if not os.path.exists(theLibraryPath):
        os.makedirs(theLibraryPath)
    else:
        print("Library path (/roms/thelibrary) already set.")

    print(f"Processing {console_name}: {url}")

    consolePath = theLibraryPath + '/' + console_name
    print(consolePath)

    if not os.path.exists(consolePath):
        os.makedirs(consolePath)
    else:
        print("Console path already exists.")

    # Generate the .py launcher files
    for title in cleaned_list:
        with open(consolePath + '/' + title + '.py', 'w') as f:
            f.write(generate_launcher_script(console_name, title))


def generate_launcher_script(console_name, title):
    """Generate the content for a game launcher .py file."""
    url = CONSOLES.get(console_name, '')
    file_path = f"~/Emulation/roms/{console_name}"

    return f'''#!/home/deck/theLibrary/venv/bin/python3
import os
import requests
from bs4 import BeautifulSoup
import zipfile
import py7zr

url = '{url}'
file_path = os.path.expanduser('{file_path}')

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=True)

    zip_links = []
    for link in links:
        if link['href'].endswith('.zip') or link['href'].endswith('.7z'):
            zip_links.append(link)

    for link in zip_links:
        if link.text.endswith('.zip'):
            link_text = link.text.rstrip('.zip')
        elif link.text.endswith('.7z'):
            link_text = link.text.rstrip('.7z')

        if link_text in str(os.path.basename(__file__)).rstrip('.py'):
            full_url = url + '/' + link['href']
            download_response = requests.get(full_url)
            if download_response.status_code == 200:
                with open(file_path + '/' + link.text, 'wb') as f:
                    f.write(download_response.content)
                print("Download successful.")

                downloaded_file = file_path + '/' + link.text
                if downloaded_file.endswith('.zip'):
                    with zipfile.ZipFile(downloaded_file, 'r') as f:
                        f.extractall(file_path)
                    os.remove(downloaded_file)
                elif downloaded_file.endswith('.7z'):
                    with py7zr.SevenZipFile(downloaded_file, mode='r') as f:
                        f.extractall(path=file_path)
                    os.remove(downloaded_file)
                break
            else:
                print("Failed to download.")
                break
else:
    print("Game not found in HTML.")
'''


def run_test(console_name):
    """Test URL connection and parsing for a console."""
    if console_name not in CONSOLES:
        print(f"Console '{console_name}' not found in CONSOLES config.")
        return False

    url = CONSOLES[console_name]
    if url == 'XXXXXXX':
        print(f"Console '{console_name}' URL not configured.")
        return False

    print(f"Testing URL for {console_name}: {url}")
    print("-" * 50)

    success, games_list, error = fetch_and_parse_games(url)

    if not success:
        print(f"FAILED: {error}")
        return False

    print(f"SUCCESS: Connection OK")
    print(f"Total games found: {len(games_list)}")
    print("-" * 50)

    if games_list:
        print("Sample games (first 10):")
        for i, game in enumerate(games_list[:10], 1):
            print(f"  {i}. {game}")
        if len(games_list) > 10:
            print(f"  ... and {len(games_list) - 10} more")
    else:
        print("No games found matching criteria.")

    return True


def addLibrary():
    xmlPath = os.path.expanduser('~/ES-DE/custom_systems/es_systems.xml')
    with open(xmlPath, 'r') as xml_file:
        xml_content = xml_file.read()

    libraryContent = """  <system>
    <name>Library</name>
    <fullname>The Library</fullname>
    <path>~/Emulation/roms/thelibrary</path>
    <extension>.py</extension>
    <command>/home/deck/theLibrary/venv/bin/python3 %ROM%</command>
    <theme>library</theme>
  </system>
"""

    libraryContent = libraryContent.replace('~', os.path.expanduser('~'))

    startTag = xml_content.find('<systemList>')
    endTag = xml_content.find('</systemList>')

    if libraryContent not in xml_content:
        if startTag != -1 and endTag != -1:
            xml_content_modified = xml_content[:endTag] + libraryContent + xml_content[endTag:]
            with open(xmlPath, 'w') as xml_file:
                xml_file.write(xml_content_modified)
        else:
            print("<systemList> and </systemList> tags were not found.")
    else:
        print("Library is already added to es_systems.xml.")


if __name__ == '__main__':
    args = parse_arguments()

    if args.test:
        # Test the first configured console
        for console_name, url in CONSOLES.items():
            if url != 'XXXXXXX':
                run_test(console_name)
                break
    else:
        addLibrary()
        for console_name in CONSOLES:
            read_files(console_name)
