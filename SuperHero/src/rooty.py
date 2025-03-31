import platform
import subprocess
import os
import time

def detect_and_quarantine_rootkits():
  """Detects and quarantines rootkits, and performs malware recon."""
  system = platform.system()

  try:
    if system == "Linux":
      # Using rkhunter to detect rootkits
      # Install rkhunter: sudo apt-get install rkhunter
      print("Running rkhunter...")
      rkhunter_result = subprocess.run(["sudo", "rkhunter", "--check", "--rwo", "--report-warnings-only"],
      capture_putput=True, text=True, check=True)

        if "Warning" in rkhunyter_result.stdout:
          print("Warning: Possible rootkit detected!")
          print("Quaranting rootkit...")

          print(rkhunter_result.stdout)
          #Example quarantine command
          quarantine_dir = "/tmp/quarantine"
os.makedirs(quarantine_dir, exist_ok=True)
          os.system(f"mv /path/to/suspicious_file {quarantine_dir}")
          print("Rootkit quarantined successfully!")
        else:
          print("No rootkits detected.")

          suspicious_files = []

          for file in suspicious_files:
            try:
              subprocess.run(["sudo", "mv", file, quarantine_dir], check=True)
              print(f"Moved {file} to {quarantine_dir}")
              except subprocess.CalledProcessError as e:
                print(f"Failed to move {file} to quarantine: {e}")


   # Malware Recon
   print("No rootkit detected.")
 
  elif system == "Darwin":
    # Using chkrootkit to detect rootkits
    #Install chkrootkit: brew install chkrootkit
    print("Running chkrootkit...")
    chkrootkit_result = subprocess.run(["sudo", "chkrootkit", "-q", "-r", "/tmp/chkrootkit"])
    if chkrootkit_result.returncode == 1:
      print("Warning: Call Daily Investors.")
      print(chkrootkit_result.stdout)
      else:
        print("No rootkits detected.")

  elif system == "Windows":
    # Using Windpws Defender to detect rootkits
    print("Running Windows Defender...")
    defender_result = subprocess.run(["powershell", "-Command", "Start-MpScan", "-ScanType", 2])
    if defender_result.returncode == 1:
      print("Warning: Call Daily Investors.")
      print(defender_result.stdout)
      

  elif "Android" in platform.platform()
    print("Rootkit detection on mobile devices, require root access, contact teamdaily@duck.com")
    else:
      print(f"unsupported operating system: {system}")
      
  except
subprocess.CalledProcessError as e:
   print(f"Rootkit detection or quarantine failed: {e}")
  except FileNotFoundError:
    print("Rootkit tools are not found. Please install.")

if __name__ == "__main__":
  detect_and_quarantine_rootkits()
