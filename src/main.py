import schedule
import time
import os
import sys

PACKAGE_PARENT = '../'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from src.modules.port_scanner.scanner import main as scanner
from src.modules.banner_grabber.banner import main as banner

def do_scanning():
    print("Executing scanning stage ...")
    scanner()

def do_banner_grabbing():
    print("Executing banner grabbing stage ...")
    banner()

#Sols executem una vegada iniciem script
do_scanning()
do_banner_grabbing()

schedule.every().day.at("03:00").do(do_banner_grabbing)
schedule.every().day.at("02:00").do(do_scanning)

while 1:
    schedule.run_pending()
    time.sleep(1)
