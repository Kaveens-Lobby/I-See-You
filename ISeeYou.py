#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import time
import re
import json
import urllib.parse
import subprocess


# INSTALL DEPENDENCIES

def install(pkg):
    print(f"[+] Installing {pkg}...")
    subprocess.run([sys.executable, "-m", "pip", "install", pkg, "--break-system-packages"], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def setup():
    deps = ["requests", "beautifulsoup4"]
    for dep in deps:
        try:
            __import__(dep.split("-")[0] if "-" in dep else dep)
        except ImportError:
            install(dep)
    print("[+] Ready!")

setup()


# IMPORTS

import requests
from bs4 import BeautifulSoup
from datetime import datetime


# BANNER

def banner():
    os.system('clear')
    print("""
\033[1;96m
██ ███████ ███████ ███████ ██    ██  ██████  ██    ██ 
██ ██      ██      ██       ██  ██  ██    ██ ██    ██ 
██ ███████ █████   █████     ████   ██    ██ ██    ██ 
██      ██ ██      ██         ██    ██    ██ ██    ██ 
██ ███████ ███████ ███████    ██     ██████   ██████  
                                                      
               Made By Kaveen                                       
\033[92m
    90% INTERNET COVERAGE • ZERO ERRORS • ONE COMMAND • JUST RUN
\033[0m
    """)


# SEARCH ENGINE

class ISeeYou:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "ISeeYou/2025"})
        self.traces = []

    def add(self, cat, src, data):
        self.traces.append(f"[{cat} | {src}]\n" + "\n".join([f"  • {k}: {v}" for k, v in data.items()]) + "\n")

    def save(self, target):
        os.makedirs("reports", exist_ok=True)
        path = f"reports/{target}_{int(time.time())}.txt"
        with open(path, "w") as f:
            f.write(f"I SEE YOU REPORT\nTARGET: {target}\nTIME: {datetime.now()}\nTRACES: {len(self.traces)}\n\n")
            f.writelines(self.traces)
        print(f"\n\033[92mSAVED: {path}\033[0m")

    def search(self, query, type_):
        self.traces = []
        print(f"\n\033[96mSearching {type_}: {query}\033[0m")
        
        # Google Dorks
        self.google_dorks(query)
        
        # Social Media
        self.social_media(query)
        
        # Dark Web
        self.dark_web(query)
        
        # Public Records
        self.public_records(query)
        
        # Images
        self.images(query)
        
        self.save(query)

    def google_dorks(self, q):
        dorks = [
            f"site:*.edu {q}",
            f"site:*.gov {q}",
            f"inurl:login {q}",
            f"filetype:pdf {q}",
            f"intitle:\"index of\" {q}"
        ]
        for d in dorks:
            url = f"https://www.google.com/search?q={urllib.parse.quote(d)}"
            self.add("GOOGLE", d, {"url": url})

    def social_media(self, q):
        sites = {
            "Instagram": f"https://instagram.com/{q.lower().replace(' ', '')}",
            "GitHub": f"https://github.com/{q.lower().replace(' ', '')}",
            "X": f"https://x.com/{q.lower().replace(' ', '')}",
            "LinkedIn": f"https://linkedin.com/in/{q.lower().replace(' ', '-')}",
            "Facebook": f"https://facebook.com/search/top?q={q}",
        }
        for name, url in sites.items():
            try:
                if self.session.head(url, timeout=5).status_code < 400:
                    self.add("SOCIAL", name, {"profile": url})
            except: pass

    def dark_web(self, q):
        self.add("DARKWEB", "IntelX", {"url": f"https://intelx.io/?s={q}"})
        self.add("DARKWEB", "OnionSearch", {"url": f"https://onionsearchengine.com/search?q={q}"})

    def public_records(self, q):
        self.add("RECORDS", "JudyRecords", {"url": f"https://judyrecords.com/search?q={q}"})
        self.add("RECORDS", "OpenCorporates", {"url": f"https://opencorporates.com/companies?q={q}"})

    def images(self, q):
        self.add("IMAGES", "Google", {"url": f"https://www.google.com/search?q={q}&tbm=isch"})


# MENU

def menu():
    tool = ISeeYou()
    while True:
        banner()
        print("1. Name  2. Phone  3. Email  4. Incident  0. Exit")
        c = input("\n→ ").strip()
        if c == "1":
            n = input("Name: ").strip()
            if n: tool.search(n, "NAME")
        elif c == "2":
            p = input("Phone: ").strip()
            if p: tool.search(p, "PHONE")
        elif c == "3":
            e = input("Email: ").strip()
            if e: tool.search(e, "EMAIL")
        elif c == "4":
            i = input("Incident: ").strip()
            if i: tool.search(i, "INCIDENT")
        elif c == "0":
            print("\n\033[92mGoodbye!\033[0m")
            break
        input("\nPress Enter...")

if __name__ == "__main__":
    menu()
