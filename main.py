from core import Logger
from core import AccountManager
from core import Banner
from colorama import Fore, Style
import os
import argparse

parser = argparse.ArgumentParser(description="SpotiTransfer settings")
parser.add_argument('-nls', '--no-log-stream', action='store_true', help='Disable logging on terminal')
parser.add_argument('-lf', '--log-file', type=str, help='Create a file with logs')
parser.add_argument('-ncs', '--no-color-stream', action='store_true', help='Disable color on log stream')
parser.add_argument('-scd', '--spotify-client-id', type=str, help='Set spotify client ID; if not set, it will be taken from the SPOTIPY_CLIENT_ID environment variable')
parser.add_argument('-scs', '--spotify-client-secret', type=str, help='Set spotify client secret; if not set, it will be taken from the SPOTIPY_CLIENT_SECRET environment variable')
parser.add_argument('-sru', '--spotify-redirect-uri', type=str, help='Set spotify redirect uri; if not set, it will be taken from the SPOTIPY_REDIRECT_URI environment variable')
parser.add_argument('-s', '--scope', type=str, nargs='+', help='Set scope on Spotify Auth to regulate account access')
args = parser.parse_args()


UNDERLINE = '\033[4m'
RESET = '\033[0m'


def clean() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def setup(log: Logger) -> (AccountManager | None):
    log.info('Authenticating ⌛')
    
    try:
        am = AccountManager(client_id=args.spotify_client_id, client_secret=args.spotify_client_secret, redirect_uri=args.spotify_redirect_uri, scope=args.scope)
        log.success('Authenticated ✅')
        return am

    except EnvironmentError as ex:
        log.error(f"Error reading settings: {ex}")
        return None

    except:
        log.error('Error authenticating ⛔')
        return None


def menu() -> None:
    print(Fore.CYAN + "1. View your playlists" + Style.RESET_ALL)
    print(Fore.YELLOW + "2. View account info" + Style.RESET_ALL)
    print(Fore.GREEN + "3. Clone playlist" + Style.RESET_ALL)
    # New functions incoming...


def main() -> None:
    banner = Banner()
    log = Logger(name=None, filename=args.log_file, stream=(not args.no_log_stream), color=(not args.no_color_stream))

    print(banner)
    root_am = setup(log)

    if root_am is None:
        return

    log.info(f"User ID 🪪: {root_am.user_id}")
    log.info(f"Username 👤: {root_am.username}")
    log.info(f"Country 🏠: {root_am.country}")
    log.info(f"Email ✉️: {root_am.email}")
    log.info(f"User Type: {root_am.user_type}")

    input("\nPress enter to continue...")
    
    while True:
        clean()
        print(Fore.LIGHTGREEN_EX + banner.__repr__())
        menu()

        try:
            choice = input("\n => ")
        except KeyboardInterrupt:
            exit(1)

        if choice.isdigit():
            choice = int(choice)
            print("\n")
            
            if choice == 1:
                playlists = root_am.get_playlists()

                if playlists is None:
                    print("No playlist found")

                else:
                    for playlist in playlists:
                        print(Fore.CYAN + Style.BRIGHT + "\nName: " + Style.RESET_ALL + Fore.GREEN + Style.BRIGHT + playlist['name'])
                        print(Fore.CYAN + Style.BRIGHT + "ID: " + Style.RESET_ALL + Fore.YELLOW + Style.DIM + playlist['id'])
                        print(Fore.CYAN + Style.BRIGHT + "URI: " + Style.RESET_ALL + Fore.MAGENTA + UNDERLINE + playlist['uri'])
                        print(Fore.CYAN + Style.BRIGHT + "Public: " + Style.RESET_ALL + Fore.RED + Style.BRIGHT + str(playlist['public']))
            
            elif choice == 2:
                print(Fore.CYAN + Style.BRIGHT + "User ID 🪪: " + Style.RESET_ALL + Fore.GREEN + root_am.user_id + Fore.RESET)
                print(Fore.CYAN + Style.BRIGHT + "Username 👤: " + Style.RESET_ALL + Fore.YELLOW + root_am.username + Fore.RESET)
                print(Fore.CYAN + Style.BRIGHT + "Country 🏠: " + Style.RESET_ALL + Fore.MAGENTA + root_am.country + Fore.RESET)
                print(Fore.CYAN + Style.BRIGHT + "Email ✉️: " + Style.RESET_ALL + Fore.RED + root_am.email + Fore.RESET)
                print(Fore.CYAN + Style.BRIGHT + "User Type: " + Style.RESET_ALL + Fore.BLUE + root_am.user_type + Fore.RESET)
            
            elif choice == 3:
                playlist_id = input("Enter the playlist id: ")
                new_name = input("Playlist name: ")
                log.info("Cloning playlist")
                if (result := root_am.clone_playlist(playlist_id, new_name)) is None:
                    log.error("Error cloning playlist")
                
                else:
                    log.success("Playlist cloned successfully")
                    log.info("Playlist name: " + new_name)
                    log.info("Playlist ID: " + result['id'])
                    log.info("Playlist URL: " + result['url'])
                
            else:
                log.error("Invalid choice")

            input("\nPress enter to continue...")


if __name__ == "__main__":
    main()