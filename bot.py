import requests
import json
from colorama import init, Fore, Style
import time
import datetime
import random
import os
init(autoreset=True)

# Define color variables
RED = Fore.RED + Style.BRIGHT
GREEN = Fore.GREEN + Style.BRIGHT
YELLOW = Fore.YELLOW + Style.BRIGHT
BLUE = Fore.BLUE + Style.BRIGHT
MAGENTA = Fore.MAGENTA + Style.BRIGHT
CYAN = Fore.CYAN + Style.BRIGHT
WHITE = Fore.WHITE + Style.BRIGHT
 

def get_headers(access_token=None):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128", "Microsoft Edge WebView2";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "Referer": "https://major.glados.app/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
    }
    if access_token:
        headers["authorization"] = f"Bearer {access_token}"
    return headers

def auth(init_data, retries=3, delay=2):
    url = "https://major.glados.app/api/auth/tg/"
    headers = get_headers()
    body = {
        "init_data": init_data
    }
    
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(body))
            response.raise_for_status()
            response_json = response.json()
            if response.status_code == 200:
                return response_json
            else:
                print(f"{RED}Error: QUERY INVALID / MATI", flush=True)
                return None
        except (requests.RequestException, ValueError) as e:
            print(f"{RED}Error getting token: {e}", flush=True)
            if attempt < retries - 1:
                print(f"{YELLOW}Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
                time.sleep(delay)
            else:
                return None

def user_detail(access_token, user_id,retries=3,delay=2):
    url = f"https://major.glados.app/api/users/{user_id}/"
    headers = get_headers(access_token)
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            if response.status_code == 200:
                return response_json
            else:
                print(f"{RED}[  Rating  ] : Error: Gagal mendapatkan balance", flush=True)
                return None
        except (requests.RequestException, ValueError) as e:
            if attempt < retries - 1:
                print(f"{YELLOW}[ Balance] : Error Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
                time.sleep(delay)
            else:
                return None
    
def daily_login(access_token,retries=3,delay=2):
    url = f"https://major.glados.app/api/user-visits/streak/"
    headers = get_headers(access_token)
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            if response.status_code == 200:
                return response_json
            else:
                print(f"{RED}[  Streak  ] : Error: Gagal mendapatkan data", flush=True)
                return None
        except (requests.RequestException, ValueError) as e:
            if attempt < retries - 1:
                print(f"{RED}[  Streak  ] : Error Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
                time.sleep(delay)
            else:
                return None
     
def play_spin(access_token, retries=3, delay=2):
    url = f"https://major.glados.app/api/roulette/"
    headers = get_headers(access_token)
    
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers)
            try:
                response_json = response.json()
            except ValueError:
                print(f"{RED}[ Spin ] : Error: Response is not valid JSON", flush=True)
                return None, None

            if response.status_code in [201, 400]:
                return response_json, response.status_code
            else:
                print(f"{RED}[ Spin ] : Error: Unexpected status code {response.status_code}", flush=True)
                return None, None
        except (requests.RequestException) as e:
            print(f"{RED}[ Spin ] : Error: {e}. Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
            time.sleep(delay)
    return None, None

def play_hold(access_token, coins, retries=3, delay=2):
    url = f"https://major.glados.app/api/bonuses/coins/"
    headers = get_headers(access_token)
    body = {"coins": coins}
    
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(body))
            try:
                response_json = response.json()
            except ValueError:
                print(f"{RED}[ Hold ] : Error: Response is not valid JSON", flush=True)
                return None, None

            if response.status_code in [201, 400]:
                return response_json, response.status_code
            else:
                print(f"{RED}[ Hold ] : Error: Unexpected status code {response.status_code}", flush=True)
                return None, None
        except (requests.RequestException) as e:
            print(f"{RED}[ Hold ] : Error: {e}. Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
            time.sleep(delay)
    return None, None

def play_swipe(access_token, coins, retries=3, delay=2):
    url = f"https://major.glados.app/api/swipe_coin/"
    headers = get_headers(access_token)
    body = {"coins": coins}
    
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(body))
            try:
                response_json = response.json()
            except ValueError:
                print(f"{RED}[ Swipe ] : Error: Response is not valid JSON", flush=True)
                return None, None

            if response.status_code in [201, 400]:
                return response_json, response.status_code
            else:
                print(f"{RED}[ Swipe ] : Error: Unexpected status code {response.status_code}", flush=True)
                return None, None
        except (requests.RequestException) as e:
            print(f"{RED}[ Swipe ] : Error: {e}. Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
            time.sleep(delay)
    return None, None

def play_puzzle(access_token, choice_1, choice_2, choice_3, choice_4, retries=3, delay=2):
    url = f"https://major.bot/api/durov/"
    headers = get_headers(access_token)
    body = {
        "choice_1": choice_1,
        "choice_2": choice_2,
        "choice_3": choice_3,
        "choice_4": choice_4
    }
    
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(body))
            try:
                response_json = response.json()
            except ValueError:
                print(f"{RED}[ Puzzle ] : Error: Response is not valid JSON", flush=True)
                return None, None

            if response.status_code in [201, 400]:
                return response_json, response.status_code
            else:
                print(f"{RED}[ Puzzle ] : Error: Unexpected status code {response.status_code}", flush=True)
                return None, None
        except (requests.RequestException) as e:
            print(f"{RED}[ Puzzle ] : Error: {e}. Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
            time.sleep(delay)
    return None, None

def join_squads(access_token, retries=3, delay=2):
    url = f"https://major.glados.app/api/squads/1182619094/join/"
    headers = get_headers(access_token)
    
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers)
            response_json = response.json()
            if response.status_code == 201:
                return response_json, response.status_code
            elif response.status_code == 400:
                return response_json, response.status_code
            else:
                print(f"{RED}[  Squads  ] : Error: Gagal mendapatkan data", flush=True)
                return None, None
        except (requests.RequestException, ValueError) as e:
            if attempt < retries - 1:
                print(f"{RED}[  Squads  ] : Error Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
                time.sleep(delay)
            else:
                return None, None

def check_in(access_token, retries=3, delay=2):
    url = f"https://major.glados.app/api/user-visits/visit/"
    headers = get_headers(access_token)
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers)
            response_json = response.json()
            if response.status_code == 200:
                return response_json
            elif response.status_code == 400:
                return response_json
            else:
                print(f"{RED}[ Check-in ] : Error: Gagal mendapatkan data", flush=True)
                return None
        except (requests.RequestException, ValueError) as e:
            if attempt < retries - 1:
                print(f"{RED}[ Check-in ] : Error Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
                time.sleep(delay)
            else:
                return None
    
def get_tasks(access_token, is_daily,retries=3,delay=2):
    url = f"https://major.glados.app/api/tasks/?is_daily={str(is_daily).lower()}"
    headers = get_headers(access_token)
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            if response.status_code == 200:
                return response_json
            else:
                print(f"{RED}[ Task ] : Error: Gagal mendapatkan data", flush=True)
                return None
        except (requests.RequestException, ValueError) as e:
            if attempt < retries - 1:
                print(f"{RED}[ Task ] : Error  Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
                time.sleep(delay)
            else:
                return None
            
def get_squad(access_token, squad_id,retries=3,delay=2):
    url = f"https://major.glados.app/api/squads/{squad_id}"
    headers = get_headers(access_token)
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            if response.status_code == 200:
                return response_json
            else:
                print(f"{RED}[  Squads  ] : Error: Gagal mendapatkan data", flush=True)
                return None
        except (requests.RequestException, ValueError) as e:
            if attempt < retries - 1:
                print(f"{RED}[  Squads  ] : Error  Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
                time.sleep(delay)
            else:
                return None
        
   
def process_task(access_token, task_id,retries=3,delay=2):
    url = "https://major.glados.app/api/tasks/"
    headers = get_headers(access_token)
    body = json.dumps({"task_id": task_id})
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, data=body)
            response_json = response.json()
            if response.status_code == 201:
                return response_json, response.status_code
            elif response.status_code == 400:
        
                return response_json, response.status_code
            else:
                print(f"{RED}[ Clear Task ] : Error: Gagal mendapatkan data", flush=True)
                return None, None
        except (requests.RequestException, ValueError) as e:
            print(f"{RED}[ Clear Task ] Error : {e}", flush=True)
            if attempt < retries - 1:
                print(f"{RED}[ Clear Task ] : Retrying... ({attempt + 1}/{retries})",end="\r",  flush=True)
                time.sleep(delay)
            else:
                return None, None
 
def print_welcome_message():
    print(Fore.WHITE + r"""
🆂 🅸 🆁 🅺 🅴 🅻
          
█▀▀ █▀▀ █▄░█ █▀▀ █▀█ █▀█ █░█ █▀
█▄█ ██▄ █░▀█ ██▄ █▀▄ █▄█ █▄█ ▄█
          """)
    print(Fore.GREEN + Style.BRIGHT + "Major BOT")
    print(Fore.YELLOW + Style.BRIGHT + "Free Konsultasi Join Telegram Channel: https://t.me/ghalibie")
    print(Fore.BLUE + Style.BRIGHT + "Buy me a coffee :) 0823 2367 3487 GOPAY / DANA")
    print(Fore.RED + Style.BRIGHT + "NOT FOR SALE ! Ngotak dikit bang. Ngoding susah2 kau tinggal rename :)\n")   

def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        go_puzzle = input(Fore.YELLOW + f"Apakah kamu ingin memainkan puzzle? (y/n): ").strip().upper()
        if go_puzzle in ['Y', 'N']:
            break
        else:
            print(Fore.RED + "Masukan tidak valid. Harap masukkan 'y' untuk ya atau 'n' untuk tidak.")

    if go_puzzle == 'Y':
        print(Fore.YELLOW + f"Masukkan 4 angka combo (contoh: 1,2,3,4): ")
        while True:
            try:
                choices = input(Fore.CYAN + "Masukkan angka combo: ").strip()
                combo = [int(x) for x in choices.split(',')]
                
                if len(combo) == 4:
                    break
                else:
                    print(Fore.RED + "Harus memasukkan tepat 4 angka.")
            except ValueError:
                print(Fore.RED + "Masukan harus berupa angka yang dipisahkan oleh koma.")
    clear_terminal()
    time.sleep(1)
    print_welcome_message()
                
    while True:                
        total_balance = 0 
        with open('query.txt', 'r') as file:
            init_data_lines = file.readlines()
        
        for index, init_data in enumerate(init_data_lines, start=1):
            init_data = init_data.strip()
            if not init_data:
                continue
            print(f"{YELLOW}Getting access token...", end="\r", flush=True)
            data = auth(init_data)
            time.sleep(1)
            if data is not None:
                access_token = data.get('access_token')
                user_data = data.get('user', {})
                user_id = user_data.get('id')
                username = user_data.get('username')
                first_name = user_data.get('first_name')
                last_name = user_data.get('last_name')

                print(f"{CYAN}====== Akun ke - {index} | {username} =======            ", flush=True)
                print(f"{CYAN}[    ID    ] : {user_id}", flush=True)
                print(f"{CYAN}[   Name   ] : {first_name} {last_name}", flush=True)

                print(f"{YELLOW}[  Rating  ] : Getting Rating...", end="\r", flush=True)
                user = user_detail(access_token,user_id)
                time.sleep(1)
                if user is not None:
                    rating = user.get('rating')
                    squad = user.get('squad_id')
                    total_balance += rating
                    if squad is not None:
                        cek_sq = get_squad(access_token, squad)
                        if cek_sq is not None:
                            name = cek_sq.get('name')
                            print(f"{GREEN}[  Squads  ] : {name}                   ", flush=True)
                    else:
                        print(f"{YELLOW}[  Squads  ] : Try to Join Sirkel...", end="\r", flush=True)
                        join_sq, status_code = join_squads(access_token)
                        time.sleep(1)
                        if join_sq is not None:
                            if status_code == 201:
                                print(f"{GREEN}[  Squads  ] : Join Sirkel Success!                   ", flush=True)
                            else:
                                error = join_sq.get('detail')
                                print(f"{RED}[  Squads  ] : {error}               ", flush=True)
                    print(f"{GREEN}[  Rating  ] : {rating}                         ", flush=True)
                    
                print(f"{YELLOW}[ Check-in ] : Try to check-in...", end="\r", flush=True)
                get_checkin = check_in(access_token)
                time.sleep(1)
                if get_checkin is not None:
                    status = get_checkin['is_increased']
                    day = get_checkin['streak']
                    if status:
                        print(f"{GREEN}[ Check-in ] : Success | Day {day}                              ", flush=True)
                    else:
                        print(f"{RED}[ Check-in ] : Already | Day {day}                              ", flush=True)

                print(f"{YELLOW}[  Streak  ] : Getting info...", end="\r", flush=True)
                time.sleep(1)
                get_streak = daily_login(access_token)
                if get_streak is not None:
                    streak = get_streak.get('streak')
                    print(f"{GREEN}[  Streak  ] : {streak}                             ", flush=True)

                print(f"{YELLOW}[ Spin ] : Getting info...", end="\r", flush=True)
                spin, status_code = play_spin(access_token)
                time.sleep(1)
                if spin is not None:
                    if status_code == 201:
                        result = spin.get('result')
                        rating_rewards = spin.get('rating_award')
                        print(f"{GREEN}[ Spin ] : Result {result} | GOT {rating_rewards}                       ", flush=True)
                    elif status_code == 400:
                        waktu = spin.get('detail', {}).get('blocked_until')
                        if waktu:
                            waktu_diff = waktu - time.time()
                            hours = int(waktu_diff // 3600)
                            minutes = int((waktu_diff % 3600) // 60)
                            print(f"{RED}[ Spin ] : Already Spin. Next in {hours} hours {minutes} minutes.  ", flush=True)
                else:
                    print(f"{RED}[ Spin ] : Error: Gagal mendapatkan data", flush=True)

                print(f"{YELLOW}[ Hold ] : Getting info...", end="\r", flush=True)
                coins = random.randint(900, 915)
                hold, status_code = play_hold(access_token, coins)
                time.sleep(1)
                if hold is not None:
                    if status_code == 201:
                        print(f"{GREEN}[ Hold ] : You Got {coins} Rating                      ", flush=True)
                    elif status_code == 400:
                        waktu = hold.get('detail', {}).get('blocked_until')
                        if waktu:
                            waktu_diff = datetime.datetime.fromtimestamp(waktu) - datetime.datetime.now()
                            hours = int(waktu_diff.total_seconds() // 3600)
                            minutes = int((waktu_diff.total_seconds() % 3600) // 60)
                            print(f"{RED}[ Hold ] : Already Hold. Next in {hours} hours {minutes} minutes.  ", flush=True)
                else:
                    print(f"{RED}[ Hold ] : Error: Gagal mendapatkan data", flush=True)

                print(f"{YELLOW}[ Swipe ] : Getting info...", end="\r", flush=True)
                coins = random.randint(2900, 3000)
                swipe, status_code = play_swipe(access_token, coins)
                time.sleep(1)
                if swipe is not None:
                    if status_code == 201:
                        print(f"{GREEN}[ Swipe ] : You Got {coins} Rating                       ", flush=True)
                    elif status_code == 400:
                        waktu = swipe.get('detail', {}).get('blocked_until')
                        if waktu:
                            waktu_diff = waktu - time.time()
                            hours = int(waktu_diff // 3600)
                            minutes = int((waktu_diff % 3600) // 60)
                            print(f"{RED}[ Swipe ] : Already Swipe. Next in {hours} hours {minutes} minutes.  ", flush=True)
                else:
                    print(f"{RED}[ Swipe ] : Error: Gagal mendapatkan data", flush=True)

                if go_puzzle == 'Y':
                    print(f"{YELLOW}[ Puzzle ] : Try to play puzzle...", end="\r", flush=True)
                    puzzle, status_code = play_puzzle(access_token, combo[0], combo[1], combo[2], combo[3])
                    time.sleep(1)
                    if puzzle is not None:
                        if status_code == 201:
                            correct_combo = puzzle.get('correct', [])
                            if sorted(correct_combo) == sorted(combo):
                                print(f"{GREEN}[ Puzzle ] : Combo {combo} is correct | Got 5000 Rating", flush=True)
                            else:
                                print(f"{RED}[ Puzzle ] : Combo {combo} is wrong, Nice Try.", flush=True)
                        elif status_code == 400:
                            detail = puzzle.get('detail')
                            if isinstance(detail, dict):
                                blocked_until = detail.get('blocked_until')
                                if blocked_until:
                                    waktu_diff = blocked_until - time.time()
                                    hours = int(waktu_diff // 3600)
                                    minutes = int((waktu_diff % 3600) // 60)
                                    print(f"{RED}[ Puzzle ] : Already play puzzle. Coba lagi dalam {hours} jam {minutes} menit.", flush=True)
            
                            else:
                                print(f"{RED}[ Puzzle ] : Already play puzzle. Coba lagi dalam {hours} jam {minutes} menit.", flush=True)
                    else:
                        print(f"{RED}[ Puzzle ] : Error: Gagal mendapatkan data", flush=True)
                else:
                    print(f"{YELLOW}[ Puzzle ] : Play puzzle skipped", flush=True)

                tasks = get_tasks(access_token, True)
                print(f"{YELLOW}[ Daily Task ] : Getting info...", end="\r", flush=True)
                time.sleep(1)
                if tasks is not None:
                    print(f"{YELLOW}[ Daily Task ] : List Task                  ", flush=True)
                    for task in tasks:
                        task_id = task.get('id')
                        title = task.get('title')
                        award = task.get('award')
                    # Skip specific tasks
                        if title in ["Stars Purchase", "Extra Stars Purchase","Promote TON blockchain","Boost Major channel","Donate rating"]:
                            print(f"{YELLOW}    -> {title} - {Style.RESET_ALL}{Fore.YELLOW}Award: {award} {MAGENTA}Skipped {Style.RESET_ALL}          ", flush=True)
                            continue
        
                        # Process other tasks
                        tasks, status_code = process_task(access_token, task_id)
                        print(f"{YELLOW}    -> {title} - Award: {award} Clearing...{Style.RESET_ALL} ", end="\r", flush=True)
                        time.sleep(1)
                        
                        if tasks is not None:
                            if status_code == 201:
                                complete = tasks['is_completed']
                                if not complete:
                                    print(f"{YELLOW}    -> {title} -{Style.RESET_ALL}{Fore.YELLOW} Award: {award} {RED}Failed{Style.RESET_ALL}                 ", flush=True)
                                else:
                                    print(f"{YELLOW}    -> {title} -{Style.RESET_ALL}{Fore.YELLOW} Award: {award} {GREEN}Completed{Style.RESET_ALL}           ", flush=True)
                            elif status_code == 400:
                                complete = tasks['detail']
                                if complete == 'Task is already completed':
                                    print( f"{YELLOW}    -> {title} -{Style.RESET_ALL}{Fore.YELLOW} Award: {award} {GREEN}Completed{Style.RESET_ALL}                 ", flush=True)
                                else:
                                    print( f"{YELLOW}    -> {title} -{Style.RESET_ALL}{Fore.YELLOW} Award: {award} {RED}{tasks}{Style.RESET_ALL}                 ", flush=True)
                tasks = get_tasks(access_token, False)
                print(f"{YELLOW}[ Basic Task ] : Getting info...", end="\r", flush=True)
                time.sleep(1)
                if tasks is not None:
                    print(f"{YELLOW}[ Basic Task ] : List Task                  ", flush=True)
            
                    for task in tasks:
                        task_id = task.get('id')
                        title = task.get('title')
                        award = task.get('award')
                    # Skip specific tasks
                        if task_id in [26,33,21,20]:
                            print(f"{YELLOW}    -> {title} - {Style.RESET_ALL}{Fore.YELLOW}Award: {award} {MAGENTA}Skipped {Style.RESET_ALL}          ", flush=True)
                            continue
        
                        tasks, status_code = process_task(access_token, task_id)
                        print(f"{YELLOW}    -> {title} - Award: {award} Clearing...{Style.RESET_ALL} ", end="\r", flush=True)
                        time.sleep(1)
                        
                        if tasks is not None:
                            if status_code == 201:
                                complete = tasks['is_completed']
                                if not complete:
                                    print(f"{YELLOW}    -> {title} -{Style.RESET_ALL}{Fore.YELLOW} Award: {award} {RED}Failed{Style.RESET_ALL}                 ", flush=True)
                                else:
                                    print(f"{YELLOW}    -> {title} -{Style.RESET_ALL}{Fore.YELLOW} Award: {award} {GREEN}Completed{Style.RESET_ALL}           ", flush=True)
                            elif status_code == 400:
                                complete = tasks['detail']
                                if complete == 'Task is already completed':
                                    print( f"{YELLOW}    -> {title} -{Style.RESET_ALL}{Fore.YELLOW} Award: {award} {GREEN}Completed{Style.RESET_ALL}                 ", flush=True)
                                else:
                                    print( f"{YELLOW}    -> {title} -{Style.RESET_ALL}{Fore.YELLOW} Award: {award} {RED}{tasks}{Style.RESET_ALL}                 ", flush=True)

        print(f"\n{GREEN}Total Balance from all accounts: {total_balance}{Style.RESET_ALL}")
        print(Fore.BLUE + Style.BRIGHT + f"\n==========SEMUA AKUN TELAH DIPROSES==========\n", flush=True)
        animated_loading(3)

def animated_loading(duration):
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        for frame in frames:
            print(f"\rMenunggu waktu claim berikutnya {frame} - Tersisa {remaining_time} detik         ", end="", flush=True)
            time.sleep(0.25)
    print("\rMenunggu waktu claim berikutnya selesai.                            ", flush=True)

if __name__ == "__main__":
    main()
