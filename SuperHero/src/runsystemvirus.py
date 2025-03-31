import platform
import subprocess
import time
import os

def run_anti_virus_scan():
  """Runs the system anti-virus scan."""
  system = platform.system()

  try:
    if system == "Windows":
      subprocess.run(["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe", "Start-MpScan", "-ScanType",
"FullScan"], check=True)
    print("Windows Defender scan initiated.")

    elif system == "Darwin": #macOS
      subprocess.run(["/usr/bin/mdfind", "kMDItemKind=Application"], check=True, stdout=subprocess.PIPE)
      print("Spotlight search initiated.")

      #You may need to install ClamAV into your system to run this command.
      elif system == "Linux":
        subprocess.run(["sudo", "clamscan", "-r", "/"], check=True)
        print("ClamAV scan initiated.")

    elif "Android" in platform.platform(): # Android Devices
      subprocess.run(["/system/bin/cmd", "package", "list", "packages"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      print("Package list initiated.")
      print("Please note that Android does not have a factory -installed anti-virus software.")

    elife system == "iOS": # iOS Devices
      print("iOS does not have a factory-installed anti-virus software, contact teamdaily@duck.com
      for further assistance.")
      else:
        print("Unsupported system.")

   except subprocess.CalledProcessError as e:
     print(f"An unexpected error occured: {e}")

def scheduled_scan():
  """Runs the anti-virus scan every 24 hours."""
  while True:
    run_anti_virus_scan()
    time.sleep(24 * 60 * 60) #24 hours

if __name__ == "__main__":
  scheduled_scan()
