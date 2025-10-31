#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
I SEE YOU v2025 - ULTIMATE OSINT FRAMEWORK
GLOBAL | DARK WEB | SOCIALS | IMAGES | PUBLIC RECORDS | INCIDENTS
100% WORKING • TERMUX/KALI • GITHUB CLONE & RUN
TXT REPORTS • LOADING SCREEN • FREE APIs
"""

import os
import sys
import time
import re
import json
import urllib.parse
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# ================================
# BANNER & COLORS
# ================================
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

C = Colors()

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

def banner():
    clear()
    print(f"""
{C.BOLD}{C.OKCYAN}

██ ███████ ███████ ███████ ██    ██  ██████  ██    ██ 
██ ██      ██      ██       ██  ██  ██    ██ ██    ██ 
██ ███████ █████   █████     ████   ██    ██ ██    ██ 
██      ██ ██      ██         ██    ██    ██ ██    ██ 
██ ███████ ███████ ███████    ██     ██████   ██████  I Always See You
Made by Kaveen the king of Rune                                                      
                                                      
{C.ENDC}{C.OKGREEN}
    ╔════════════════════════════════════════════════════════════════════╗
    ║  GLOBAL OSINT • DARK WEB • SOCIALS • IMAGES • RECORDS • INCIDENTS  ║
    ║  TERMUX/KALI • GITHUB CLONE & RUN • TXT REPORTS • 100% WORKING     ║
    ╚════════════════════════════════════════════════════════════════════╝{C.ENDC}
    """)

# ================================
# LOADING ANIMATION
# ================================
def loading(message, duration=2):
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r{C.OKBLUE}{spinner[i % len(spinner)]} {message}{C.ENDC}", end="", flush=True)
        i += 1
        time.sleep(0.1)
    print(f"\r{' ' * 80}\r", end="")

# ================================
# CORE RESULT MODEL
# ================================
@dataclass
class Trace:
    category: str
    source: str
    data: dict
    raw: str = ""

    def to_txt(self, f):
        f.write(f"[{self.category.upper()} | {self.source}]\n")
        f.write(f"{'─' * 60}\n")
        for k, v in self.data.items():
            if isinstance(v, list):
                f.write(f"{k}:\n")
                for item in v:
                    f.write(f"  • {item}\n")
            else:
                f.write(f"{k}: {v}\n")
        f.write("\n")

# ================================
# I SEE YOU ENGINE
# ================================
class ISeeYou:
    def __init__(self):
        self.traces = []
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36"
        })
        self.target = ""

    def add(self, category, source, data, raw=""):
        self.traces.append(Trace(category, source, data, raw))

    def save_report(self):
        os.makedirs("I_SEE_YOU_Reports", exist_ok=True)
        ts = int(time.time())
        safe_target = re.sub(r'[^\w@.+]', '_', self.target)[:50]
        path = f"I_SEE_YOU_Reports/{safe_target}_{ts}.txt"

        with open(path, "w", encoding="utf-8") as f:
            f.write(f"{'='*80}\n")
            f.write(f"{'I SEE YOU - GLOBAL OSINT REPORT':^80}\n")
            f.write(f"{'='*80}\n\n")
            f.write(f"TARGET: {self.target}\n")
            f.write(f"GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"TOTAL TRACES: {len(self.traces)}\n")
            f.write(f"{'='*80}\n\n")

            for trace in self.traces:
                trace.to_txt(f)

        print(f"{C.OKGREEN}REPORT SAVED: {path}{C.ENDC}")
        return path

    # ================================
    # NAME SEARCH
    # ================================
    def search_name(self, name):
        self.target = name
        print(f"{C.OKCYAN}Searching NAME: {name}{C.ENDC}")
        loading("Scanning social media...", 1.5)
        self._social_scan(name)
        loading("Searching public records...", 1.5)
        self._public_records(name)
        loading("Searching images...", 1.5)
        self._google_images(name)
        loading("Dark web leaks...", 1.5)
        self._intelx(name)
        self.save_report()

    # ================================
    # PHONE SEARCH
    # ================================
    def search_phone(self, phone):
        self.target = phone
        phone_clean = re.sub(r'\D', '', phone)
        print(f"{C.OKCYAN}Searching PHONE: {phone}{C.ENDC}")
        loading("Checking WhatsApp...", 1)
        self.add("PHONE", "WhatsApp", {"profile": f"https://wa.me/{phone_clean}"})
        loading("TrueCaller lookup...", 1.5)
        self._truecaller(phone_clean)
        loading("Epieos reverse...", 1.5)
        self._epieos(phone_clean)
        loading("Dark web exposure...", 1.5)
        self._intelx(phone_clean)
        self.save_report()

    # ================================
    # EMAIL SEARCH
    # ================================
    def search_email(self, email):
        self.target = email
        print(f"{C.OKCYAN}Searching EMAIL: {email}{C.ENDC}")
        loading("HIBP breaches...", 1.5)
        self._hibp(email)
        loading("Epieos services...", 1.5)
        self._epieos(email)
        loading("Holehe 120+ sites...", 2)
        self._holehe(email)
        loading("Dark web leaks...", 1.5)
        self._intelx(email)
        loading("Social username...", 1)
        self._social_from_email(email)
        self.save_report()

    # ================================
    # INCIDENT SEARCH
    # ================================
    def search_incident(self, incident):
        self.target = "INCIDENT"
        print(f"{C.OKCYAN}Searching INCIDENT: {incident[:50]}...{C.ENDC}")
        keywords = " ".join(re.findall(r'\b\w+\b', incident.lower()))
        loading("Google News...", 1.5)
        self._google_news(keywords)
        loading("Twitter/X real-time...", 1.5)
        self._x_search(keywords)
        loading("Dark web forums...", 1.5)
        self._intelx(keywords)
        loading("Public records...", 1)
        self._judyrecords(keywords)
        self.save_report()

    # ================================
    # SOCIAL MEDIA SCAN
    # ================================
    def _social_scan(self, name):
        platforms = {
            "Facebook": f"https://www.facebook.com/search/top?q={urllib.parse.quote(name)}",
            "Instagram": f"https://www.instagram.com/{name.lower().replace(' ', '')}/",
            "Twitter/X": f"https://x.com/{name.lower().replace(' ', '')}",
            "LinkedIn": f"https://www.linkedin.com/search/results/people/?keywords={urllib.parse.quote(name)}",
            "GitHub": f"https://github.com/{name.lower().replace(' ', '')}",
            "OnlyFans": f"https://onlyfans.com/{name.lower().replace(' ', '')}",
        }
        found = []
        for plat, url in platforms.items():
            try:
                r = self.session.head(url, timeout=8, allow_redirects=True)
                if r.status_code < 400:
                    found.append(f"{plat}: {url}")
            except: pass
        self.add("SOCIAL MEDIA", "Profiles", {"found": len(found), "links": found or ["None"]})

    # ================================
    # PUBLIC RECORDS
    # ================================
    def _public_records(self, name):
        parts = name.split()
        if len(parts) >= 2:
            url = f"https://www.judyrecords.com/search?first_name={parts[0]}&last_name={'%20'.join(parts[1:])}"
            self.add("PUBLIC RECORDS", "JudyRecords", {"url": url})

    # ================================
    # IMAGE SEARCH
    # ================================
    def _google_images(self, name):
        url = f"https://www.google.com/search?q={urllib.parse.quote(name)}&tbm=isch"
        self.add("IMAGES", "Google", {"search_url": url, "note": "Open link for photos"})

    # ================================
    # DARK WEB (INTELX)
    # ================================
    def _intelx(self, query):
        url = f"https://intelx.io/?s={urllib.parse.quote(query)}"
        self.add("DARK WEB", "Intelligence X", {
            "search_url": url,
            "note": "Free leak search - check manually"
        })

    # ================================
    # PHONE: TRUECALLER
    # ================================
    def _truecaller(self, phone):
        url = f"https://www.truecaller.com/search/in/{phone}"
        try:
            r = self.session.get(url, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            name = soup.find("span", class_="truncate")
            if name:
                self.add("PHONE", "TrueCaller", {"name": name.text.strip(), "url": url})
        except: pass

    # ================================
    # UNIVERSAL: EPIEOS
    # ================================
    def _epieos(self, query):
        url = f"https://epieos.com/?q={urllib.parse.quote(query)}"
        try:
            r = self.session.get(url, timeout=12)
            soup = BeautifulSoup(r.text, 'html.parser')
            links = [a['href'] for a in soup.select('a[href^="http"]')[:5]]
            self.add("REVERSE LOOKUP", "Epieos", {"links_found": len(links), "urls": links})
        except: pass

    # ================================
    # EMAIL: HIBP
    # ================================
    def _hibp(self, email):
        try:
            r = self.session.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(email)}", timeout=10)
            if r.status_code == 200:
                breaches = [b['Name'] for b in r.json()[:10]]
                self.add("BREACHES", "HIBP", {"count": len(breaches), "sites": breaches})
            elif r.status_code == 404:
                self.add("BREACHES", "HIBP", {"status": "Clean"})
        except: pass

    # ================================
    # EMAIL: HOLEHE
    # ================================
    def _holehe(self, email):
        try:
            import subprocess
            result = subprocess.run(["holehe", email, "--json"], capture_output=True, text=True, timeout=45)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                found = [k for k, v in data.items() if v.get("status") == "Found"][:10]
                self.add("EMAIL SITES", "Holehe", {"found": len(found), "platforms": found})
        except:
            self.add("EMAIL SITES", "Holehe", {"note": "Install: pip install holehe"})

    # ================================
    # EMAIL: SOCIAL FROM USERNAME
    # ================================
    def _social_from_email(self, email):
        username = email.split('@')[0]
        platforms = [f"https://instagram.com/{username}", f"https://github.com/{username}"]
        found = []
        for url in platforms:
            try:
                if self.session.head(url, timeout=5).status_code < 400:
                    found.append(url)
            except: pass
        self.add("SOCIAL", "From Email", {"username": username, "profiles": found})

    # ================================
    # INCIDENT: GOOGLE NEWS
    # ================================
    def _google_news(self, keywords):
        url = f"https://www.google.com/search?q={urllib.parse.quote(keywords)}&tbm=nws"
        self.add("NEWS", "Google", {"search_url": url})

    # ================================
    # INCIDENT: TWITTER/X
    # ================================
    def _x_search(self, keywords):
        url = f"https://x.com/search?q={urllib.parse.quote(keywords)}&f=live"
        self.add("REAL-TIME", "X (Twitter)", {"search_url": url})

    # ================================
    # INCIDENT: JUDYRECORDS
    # ================================
    def _judyrecords(self, keywords):
        url = f"https://www.judyrecords.com/search?q={urllib.parse.quote(keywords)}"
        self.add("LEGAL", "JudyRecords", {"search_url": url})

# ================================
# MAIN MENU
# ================================
def main_menu():
    engine = ISeeYou()
    while True:
        banner()
        print(f"{C.OKGREEN}MENU:{C.ENDC}")
        print(f"  {C.OKCYAN}1.{C.ENDC} Search by Name")
        print(f"  {C.OKCYAN}2.{C.ENDC} Search by Number")
        print(f"  {C.OKCYAN}3.{C.ENDC} Search by Email")
        print(f"  {C.OKCYAN}4.{C.ENDC} Search the Incident")
        print(f"  {C.OKCYAN}0.{C.ENDC} Exit")
        choice = input(f"\n{C.BOLD}Choice → {C.ENDC}").strip()

        if choice == "1":
            name = input(f"{C.OKCYAN}Full Name: {C.ENDC}").strip()
            if name: engine.search_name(name)
        elif choice == "2":
            phone = input(f"{C.OKCYAN}Phone (+123...): {C.ENDC}").strip()
            if phone: engine.search_phone(phone)
        elif choice == "3":
            email = input(f"{C.OKCYAN}Email: {C.ENDC}").strip()
            if email and "@" in email: engine.search_email(email)
            else: print(f"{C.FAIL}Invalid email!{C.ENDC}")
        elif choice == "4":
            print(f"{C.OKCYAN}Describe the incident (e.g., 'bank hack 2025'):{C.ENDC}")
            incident = input("> ").strip()
            if incident: engine.search_incident(incident)
        elif choice == "0":
            print(f"{C.OKGREEN}I SEE YOU — Goodbye!{C.ENDC}")
            break
        else:
            input(f"{C.FAIL}Invalid! Press Enter...{C.ENDC}")
            continue

        input(f"\n{C.WARNING}Press Enter to continue...{C.ENDC}")

# ================================
# RUN
# ================================
if __name__ == "__main__":
    print(f"{C.OKGREEN}Launching I SEE YOU v2025...{C.ENDC}")
    main_menu()
