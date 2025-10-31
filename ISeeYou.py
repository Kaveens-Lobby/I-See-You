#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
I SEE YOU - Ultimate OSINT Framework (2025)
KALI LINUX + VENV = 100% WORKING
SAVES REPORTS AS .txt FILES
"""

import os
import sys
import json
import re
import time
import urllib.parse
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass

# ================================
# BANNER & COLORS
# ================================
class Colors:
    OKGREEN = '\033[92m'
    OKCYAN = '\033[96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

C = Colors()

def banner():
    print(f"""
{C.BOLD}{C.OKCYAN}
    ███████╗ ███████╗ ███████╗     ██╗   ██╗ ██████╗  ██╗   ██╗
    ██╔════╝ ██╔════╝ ██╔════╝     ╚██╗ ██╔╝██╔═══██╗ ╚██╗ ██╔╝
    ███████╗ █████╗   █████╗        ╚████╔╝ ██║   ██║  ╚████╔╝ 
    ╚════██║ ██╔══╝   ██╔══╝         ╚██╔╝  ██║   ██║   ╚██╔╝  
    ███████║ ███████╗ ███████╗        ██║   ╚██████╔╝    ██║   
    ╚══════╝ ╚══════╝ ╚══════╝        ╚═╝    ╚═════╝     ╚═╝   
{C.ENDC}{C.OKGREEN}
    ╔═══════════════════════════════════════════════════════╗
    ║  KALI LINUX • VENV • SAVES .txt REPORTS • JUST RUN!   ║
    ╚═══════════════════════════════════════════════════════╝{C.ENDC}
    """)

# ================================
# CORE ENGINE
# ================================
@dataclass
class Result:
    source: str
    data: dict
    raw: str = ""

class ISeeYou:
    def __init__(self):
        self.results = []
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "ISeeYou/2025"})
        self.target = ""

    def add(self, source, data, raw=""):
        self.results.append(Result(source, data, raw))

    def save_txt(self):
        os.makedirs("reports", exist_ok=True)
        ts = int(time.time())
        base = re.sub(r'[^\w]', '_', self.target or "target")
        file_path = f"reports/{base}_{ts}.txt"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"I SEE YOU - OSINT REPORT\n")
            f.write(f"Target: {self.target}\n")
            f.write(f"Generated: {time.ctime()}\n")
            f.write(f"Total Traces: {len(self.results)}\n")
            f.write("="*60 + "\n\n")

            for i, r in enumerate(self.results, 1):
                f.write(f"[{i}] SOURCE: {r.source}\n")
                f.write("-" * 50 + "\n")
                for k, v in r.data.items():
                    f.write(f"  {k}: {v}\n")
                f.write("\n")

        print(f"{C.OKGREEN}REPORT SAVED: {file_path}{C.ENDC}")

    def search_name(self, name):
        self.target = name
        print(f"{C.OKCYAN}Searching NAME: {name}{C.ENDC}")
        self._epieos(name)
        self._social(name)
        self.save_txt()

    def search_phone(self, phone):
        self.target = phone
        phone_clean = re.sub(r'\D', '', phone)
        print(f"{C.OKCYAN}Searching PHONE: {phone}{C.ENDC}")
        self.add("Phone (Clean)", {"number": phone_clean})
        self.add("WhatsApp", {"url": f"https://wa.me/{phone_clean}"})
        self._epieos(phone_clean)
        self.save_txt()

    def search_email(self, email):
        self.target = email
        print(f"{C.OKCYAN}Searching EMAIL: {email}{C.ENDC}")
        self._hibp(email)
        self._epieos(email)
        self.save_txt()

    def _epieos(self, query):
        url = f"https://epieos.com/?q={urllib.parse.quote(query)}"
        try:
            r = self.session.get(url, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            links = []
            for a in soup.select('a[href^="http"]')[:5]:
                href = a.get('href')
                text = a.get_text(strip=True)
                if href and text:
                    links.append(f"{text}: {href}")
            self.add("Epieos", {"search_url": url, "found_links": links or "None"})
        except Exception as e:
            self.add("Epieos", {"error": str(e)})

    def _social(self, name):
        platforms = [
            ("Instagram", f"https://instagram.com/{name.lower()}"),
            ("GitHub", f"https://github.com/{name.lower()}"),
            ("X (Twitter)", f"https://x.com/{name.lower()}"),
            ("LinkedIn", f"https://linkedin.com/in/{name.lower().replace(' ', '-')}")
        ]
        found = []
        for plat, url in platforms:
            try:
                if self.session.head(url, timeout=6).status_code < 400:
                    found.append(f"{plat}: {url}")
            except:
                pass
        self.add("Social Media", {"profiles_found": found or "None"})

    def _hibp(self, email):
        try:
            r = self.session.get(
                f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(email)}",
                headers={"hibp-api-key": "dev-only"}, timeout=10
            )
            if r.status_code == 200:
                breaches = [b['Name'] for b in r.json()[:5]]
                self.add("HIBP Breaches", {"breached": True, "sites": breaches})
            elif r.status_code == 404:
                self.add("HIBP", {"status": "Clean - No breaches found"})
            else:
                self.add("HIBP", {"status": f"HTTP {r.status_code}"})
        except:
            self.add("HIBP", {"status": "Check failed"})

# ================================
# MENU
# ================================
def menu():
    os.system('clear')
    banner()
    tool = ISeeYou()
    while True:
        print(f"{C.OKGREEN}1. Name    2. Phone    3. Email    0. Exit{C.ENDC}")
        choice = input(f"\n{C.BOLD}Choice → {C.ENDC}").strip()

        if choice == "1":
            name = input(f"{C.OKCYAN}Full Name: {C.ENDC}").strip()
            if name: tool.search_name(name)
        elif choice == "2":
            phone = input(f"{C.OKCYAN}Phone (+123...): {C.ENDC}").strip()
            if phone: tool.search_phone(phone)
        elif choice == "3":
            email = input(f"{C.OKCYAN}Email: {C.ENDC}").strip()
            if email: tool.search_email(email)
        elif choice == "0":
            print(f"{C.OKGREEN}I SEE YOU — Session Ended.{C.ENDC}")
            break
        else:
            input(f"{C.FAIL}Invalid choice! Press Enter...{C.ENDC}")
            continue

        input(f"\n{C.WARNING}Press Enter to continue...{C.ENDC}")
        os.system('clear')
        banner()

if __name__ == "__main__":
    menu()
