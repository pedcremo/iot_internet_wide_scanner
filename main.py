import schedule
import time
from scanner_module.scanner import startScanning


def scannerAgent():
    print("I'm scanning...")
    startScanning()

#schedule.every(10).minutes.do(job)
#schedule.every().hour.do(job)
schedule.every().day.at("18:40").do(scannerAgent)

while 1:
    schedule.run_pending()
    time.sleep(1)