import time
import os
import random
import string
import requests
import re
import undetected_chromedriver as uc
import winsound
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, init
from datetime import datetime

init(autoreset=True)

def gradient_ascii_art(ascii_art, start_rgb, end_rgb):
    lines = ascii_art.split('\n')
    max_width = max(len(line) for line in lines)
    for line in lines:
        for i, char in enumerate(line):
            ratio = i / max_width if max_width > 0 else 0
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
            print(f"\033[38;2;{r};{g};{b}m{char}\033[0m", end='')
        print()

ascii_art = r"""


 █    ██  ██▓  ▄▄▄█████▓ ██▓ ███▄ ▄███▓ ▄▄▄     ▄▄▄█████▓▓█████
 ██  ▓██▒▓██▒  ▓  ██▒ ▓▒▓██▒▓██▒▀█▀ ██▒▒████▄   ▓  ██▒ ▓▒▓█   ▀
▓██  ▒██░▒██░  ▒ ▓██░ ▒░▒██▒▓██    ▓██░▒██  ▀█▄ ▒ ▓██░ ▒░▒███
▓▓█  ░██░▒██░  ░ ▓██▓ ░ ░██░▒██    ▒██ ░██▄▄▄▄██░ ▓██▓ ░ ▒▓█  ▄
▒▒█████▓ ░██████▒▒██▒ ░ ░██░▒██▒   ░██▒ ▓█   ▓██▒ ▒██▒ ░ ░▒████▒
░▒▓▒ ▒ ▒ ░ ▒░▓  ░▒ ░░   ░▓  ░ ▒░   ░  ░ ▒▒   ▓▒█░ ▒ ░░   ░░ ▒░ ░
░░▒░ ░ ░ ░ ░ ░  ░  ░     ▒ ░░  ░      ░  ▒   ▒▒ ░   ░     ░ ░  ░
 ░░░ ░ ░   ░ ░   ░       ▒ ░░      ░     ░   ▒    ░         ░
   ░         ░  ░        ░         ░         ░  ░           ░  ░ v1.1(almost manual because its free)
     made by @Balrampreet1/@balramog                
                           
        Fully automatic and thread supported  gen also available         https://ultimatetools.mysellauth.com/
"""

# made by balrampreet1
os.system("cls" if os.name == "nt" else "clear")
os.system("title ULTIMATE BALRAMOG")
gradient_ascii_art(ascii_art, (255, 16, 240), (16, 200, 255))

API_BASE_URL = "https://api.tempmail.lol/v2"

def create_temp_email():
    try:
        response = requests.post(f"{API_BASE_URL}/inbox/create")
        if response.status_code == 201:
            data = response.json()
            email, token = data.get("address"), data.get("token")
            print(Fore.GREEN + f"✅ Temporary Email Created: {email}")
            return email, token
        else:
            print(Fore.RED + f"❌ Failed to create email. Response: {response.text}")
    except Exception as e:
        print(Fore.RED + f"❌ Error creating email: {e}")
    return None, None

def check_inbox(token):
    try:
        response = requests.get(f"{API_BASE_URL}/inbox", params={"token": token})
        if response.status_code == 200:
            data = response.json()
            if not data.get("emails"):
                print(Fore.YELLOW + "📭 Inbox is empty.")
                return []
            return data["emails"]
        else:
            print(Fore.RED + f"❌ Failed to check inbox. Response: {response.text}")
    except Exception as e:
        print(Fore.RED + f"❌ Error checking inbox: {e}")
    return []

def save_email_html(email_data, idx):
    html = email_data.get("html", "No HTML content available")
    filename = f"htmlcode_{idx}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(Fore.GREEN + f"✅ HTML content saved to {filename}")
    return filename

def extract_otp_from_html(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        match = re.search(r'<tr>\s*<td[^>]*?>\s*(\d+)\s*<br>', html)
        if match:
            otp = match.group(1)
            print(Fore.CYAN + f"🔑 OTP Extracted: {otp}")
            return otp
    except Exception as e:
        print(Fore.RED + f"❌ Error extracting OTP: {e}")
    print(Fore.RED + "❌ No OTP found.")
    return None

def delete_file(path):
    try:
        os.remove(path)
        print(Fore.GREEN + f"✅ File {path} deleted.")
    except Exception as e:
        print(Fore.RED + f"❌ Could not delete file: {e}")

def save_email_token(email, token):
    with open("saved.txt", "a", encoding="utf-8") as f:
        f.write(f"Email: {email}, Token: {token}\n")
    print(Fore.GREEN + "✅ Saved email and token.")

def input_verification_code(driver, code):
    for i in range(6):
        box = driver.find_element(By.NAME, f"code-input-{i}")
        box.clear()
        box.send_keys(code[i])

def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

def extract_promo_link_from_html(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            html = file.read()
        match = re.search(r'link="([^"]+)"', html)
        if match:
            link = match.group(1)
            print(Fore.CYAN + f"🔗 Promo Link: {link}")
            return link
    except Exception as e:
        print(Fore.RED + f"❌ Error extracting promo link: {e}")
    print(Fore.RED + "❌ No promo link found.")
    return None

# Start Process
email, token = create_temp_email()
if email and token:
    input(Fore.YELLOW + "\n📋 Copy the email above, then press ENTER to open Chrome... or just buy automatic from @balrampreet1 on discord in cheap or full src https://ultimatetools.mysellauth.com/")
    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = uc.Chrome(options=options)

    driver.get("https://www.epicgames.com/id/register/date-of-birth?lang=en-US&redirect_uri=https%3A%2F%2Fstore.epicgames.com%2Fen-US%2Fp%2Fdiscord--discord-nitro&client_id=875a3b57d3a640a6b7f9b4e883463ab4")
    print(Fore.GREEN + f"({get_current_time()}) | Opened Epic Games registration page.")
    wait = WebDriverWait(driver, 10)
    print(Fore.RED + f"({get_current_time()}) | 🚨 Solve CAPTCHA manually.")

    idx = 1
    otp_verified = False
    while not otp_verified:
        print(Fore.BLUE + f"🔍 Checking inbox for OTP at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
        emails = check_inbox(token)
        if emails:
            for email_data in emails:
                file_path = save_email_html(email_data, idx)
                otp = extract_otp_from_html(file_path)
                if otp:
                    input_verification_code(driver, otp)
                    verify_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='continue'][@aria-label='Verify email']")))
                    verify_btn.click()
                    print(Fore.GREEN + "✅ Email Verified!")
                    delete_file(file_path)
                    save_email_token(email, token)
                    otp_verified = True
                    break
        else:
            print(Fore.YELLOW + "🔄 Waiting for OTP...")
        time.sleep(10)

    time.sleep(5)
    try:
        get_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='purchase-cta-button' and .//span/span[text()='Get']]")))
        get_btn.click()
        print(Fore.GREEN + "✅ 'Get' button clicked.")
    except:
        print(Fore.RED + "❌ Failed to click 'Get' button.")

    # Promo Link Monitor
    while otp_verified:
        print(Fore.BLUE + f"🔍 Checking inbox for promo link at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
        emails = check_inbox(token)
        if emails:
            for email_data in emails:
                file_path = save_email_html(email_data, idx)
                idx += 1
                promo_link = extract_promo_link_from_html(file_path)
                if promo_link:
                    with open("promo.txt", "a", encoding="utf-8") as promo_file:
                        promo_file.write(f"{promo_link}\n")
                    print(Fore.GREEN + "✅ Promo link saved to promo.txt. buy automatic tool at https://ultimatetools.mysellauth.com/ ")
        else:
            print(Fore.YELLOW + "🔄 Still checking inbox...")
        time.sleep(10)

    driver.quit()
else:
    print(Fore.RED + "❌ Could not create temp email. Exiting...")
