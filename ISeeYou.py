#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
I SEE YOU v2025 - OFFLINE OSINT TOOL
AUTO-CREATES venv + INSTALLS deps
NO curl • NO GitHub • NO INTERNET NEEDED
KALI / TERMUX / ANY LINUX • 100% WORKING
"""

import os
import sys
import subprocess
import time


# AUTO-CREATE VENV + INSTALL

def run(cmd):
    print(f"[*] {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[!] FAILED: {result.stderr}")
        if "python3-venv" in result.stderr:
            sys.exit("[!] Install: sudo apt install python3-venv -y")
        return False
    return True

def setup():
    print("[*] Setting up I SEE YOU...")
    
    # Create venv
    if not os.path.exists("venv"):
        if not run("python3 -m venv venv"):
            sys.exit("[!] Failed to create venv")
    
    pip = "venv/bin/pip"
    python = "venv/bin/python"
    
    # Upgrade pip
    run(f"{pip} install --upgrade pip")
    
    # Install deps
    for pkg in ["requests", "beautifulsoup4"]:
        if not run(f"{pip} install {pkg}"):
            sys.exit(f"[!] Failed to install {pkg}")
    
    # Optional: holehe
    if not run(f"{pip} install holehe"):
        print("[!] holehe skipped (optional)")
    
    # Restart in venv
    if not os.getenv("ISEEYOU_ACTIVE"):
        os.environ["ISEEYOU_ACTIVE"] = "1"
        os.execv(python, [python] + sys.argv)

setup()


# IMPORTS

import re
import json
import urllib.parse
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from datetime import datetime


# BANNER

class Colors:
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

C = Colors()

def clear():
    os.system('clear')

def banner():
    clear()
    print(f"""
{C.BOLD}{C.OKCYAN}
██ ███████ ███████ ███████ ██    ██  ██████  ██    ██ 
██ ██      ██      ██       ██  ██  ██    ██ ██    ██ 
██ ███████ █████   █████     ████   ██    ██ ██    ██ 
██      ██ ██      ██         ██    ██    ██ ██    ██ 
██ ███████ ███████ ███████    ██     ██████   ██████  I can See anything
     Made by Kaveen Mithsaka                                                 
                                                      
{C.ENDC}{C.OKGREEN}
    ╔════════════════════════════════════════════════════════════════════╗
    ║                   • KALI/TERMUX • TXT REPORTS                      ║
    ╚════════════════════════════════════════════════════════════════════╝{C.ENDC}
    """)


# LOADING

def loading(msg, t=1.0):
    spinner = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for _ in range(int(t * 10)):
        for c in spinner:
            print(f"\r{C.OKBLUE}{c} {msg}{C.ENDC}", end="", flush=True)
            time.sleep(0.1)
    print("\r" + " " * 80 + "\r", end="")


# RESULT & SAVE

@dataclass
class Trace:
    category: str
    source: str
    data: dict

    def write(self, f):
        f.write(f"[{self.category.upper()} | {self.source}]\n")
        f.write(f"{'─' * 60}\n")
        for k, v in self.data.items():
            if isinstance(v, list):
                f.write(f"{k}:\n")
                for i in v: f.write(f"  • {i}\n")
            else:
                f.write(f"{k}: {v}\n")
        f.write("\n")

class ISeeYou:
    def __init__(self):
        self.traces = []
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "ISeeYou/2025"})
        self.target = ""

    def add(self, cat, src, data):
        self.traces.append(Trace(cat, src, data))

    def save(self):
        os.makedirs("reports", exist_ok=True)
        ts = int(time.time())
        safe = re.sub(r'[^\w@.+]', '_', self.target or "target")[:50]
        path = f"reports/{safe}_{ts}.txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"{'='*80}\n{'I SEE YOU OSINT REPORT':^80}\n{'='*80}\n\n")
            f.write(f"TARGET: {self.target}\n")
            f.write(f"TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"TRACES FOUND: {len(self.traces)}\n{'='*80}\n\n")
            for t in self.traces: t.write(f)
        print(f"{C.OKGREEN}SAVED: {path}{C.ENDC}")

    def search_name(self, name):
        self.target = name
        loading("Social scan")
        self._social(name)
        loading("Images")
        self.add("IMAGES", "Google", {"url": f"https://www.google.com/search?q={name}&tbm=isch"})
        loading("Dark web")
        self.add("DARKWEB", "IntelX", {"url": f"https://intelx.io/?s={name}"})
        self.save()

    def search_phone(self, phone):
        self.target = phone
        p = re.sub(r'\D', '', phone)
        loading("WhatsApp")
        self.add("PHONE", "WhatsApp", {"url": f"https://wa.me/{p}"})
        loading("Epieos")
        self._epieos(p)
        self.save()

    def search_email(self, email):
        self.target = email
        loading("HIBP")
        self._hibp(email)
        loading("Epieos")
        self._epieos(email)
        self.save()

    def search_incident(self, text):
        self.target = "INCIDENT"
        loading("News")
        self.add("NEWS", "Google", {"url": f"https://www.google.com/search?q={text}&tbm=nws"})
        self.save()

    def _social(self, name):
        sites = ["instagram.com", "github.com", "x.com"]
        found = []
        for s in sites:
            url = f"https://{s}/{name.lower().replace(' ', '')}"
            try:
                if self.session.head(url, timeout=5).status_code < 400:
                    found.append(url)
            except: pass
        self.add("SOCIAL", "Profiles", {"found": found or ["None"]})

    def _epieos(self, q):
        url = f"https://epieos.com/?q={urllib.parse.quote(q)}"
        try:
            r = self.session.get(url, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            links = [a['href'] for a in soup.select('a[href^="http"]')[:3]]
            self.add("REVERSE", "Epieos", {"links": links or ["None"]})
        except:
            self.add("REVERSE", "Epieos", {"error": "Failed"})

    def _hibp(self, email):
        try:
            r = self.session.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", timeout=10)
            status = "BREACHED" if r.status_code == 200 else "CLEAN"
            self.add("BREACH", "HIBP", {"status": status})
        except:
            self.add("BREACH", "HIBP", {"status": "Check failed"})


# MENU

def menu():
    engine = ISeeYou()
    while True:
        banner()
        print(f"{C.OKGREEN}1. Name  2. Phone  3. Email  4. Incident  0. Exit{C.ENDC}")
        c = input(f"\n{C.BOLD}→ {C.ENDC}").strip()
        if c == "1":
            n = input(f"{C.OKCYAN}Name: {C.ENDC}").strip()
            if n: engine.search_name(n)
        elif c == "2":
            p = input(f"{C.OKCYAN}Phone: {C.ENDC}").strip()
            if p: engine.search_phone(p)
        elif c == "3":
            e = input(f"{C.OKCYAN}Email: {C.ENDC}").strip()
            if "@" in e: engine.search_email(e)
        elif c == "4":
            i = input(f"{C.OKCYAN}Incident: {C.ENDC}").strip()
            if i: engine.search_incident(i)
        elif c == "0":
            print(f"{C.OKGREEN}Goodbye!{C.ENDC}")
            break
        input(f"\n{C.WARNING}Press Enter...{C.ENDC}")

if __name__ == "__main__":
    menu()
