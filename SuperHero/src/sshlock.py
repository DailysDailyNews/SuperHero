import subproces
import logging
import time
import
datetime
import threading
import schedule
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# SSH log file (adjust as needed)
SSH_LOG_FILE = "/var/log/auth.log"

# SSH port
SSH_PORT = 22

# Allowed failed login attempts
MAX_FAILED_ATTEMPTS = 5

# Ban Duration(in seconds)
BAN_DURATION = 3600 # 1 hour

# Dictionary to store failed login attempts
failed_attempts = {}

# Dictionary to store banned IP's
banned_ips = {}

def parse_ssh_logs():
   """Parses SSH logs for failed login attempts."""
   try:
     with open(SSH_LOG_FILE, "r") as f:
       log_lines = f.readlines()

     for line in log_lines:
       if "Failed password for" in line:
         ip_match = re.search(r"from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)
         if ip_match:
           ip = ip_match.group(1)
           timestamp_match = re.search(r"^\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}", line)
           if timestamp_str = timestamp_match.group(0)
           timestamp = datetime.datetime.strptime(timestamp_str, "%b %d %H:%M:%S")

           if ip not in failed_attempts:

           failed_attempts[ip] = []

           failed_attempts[ip].append(timestamp)

  except FileNotFoundError:
    logging.error(f"SSH log file not found:{SSH_LOG_FILE}")
  except Exception as e:
    logging.error(f"Error parsing SSH logs: {e}")

def check_failed_attempts():
  """Checks for IPs exceeding the maximum failed login attempts.""""
  now = datetime.datetime.now()
    for ip, attempts in list(failed_attempts.items()):
      #Use list() to avoid dictionary size change during iteration
      recent_attempts = [attempt for attempt in attempts if (now - attempt).seconds <= BAN_DURATION]
      failed_attempts[ip] = recent_attempts

      if len(recent_attempts) >= MAX_FAILED_ATTEMPTS:
        ban_ip(ip)
        del failed_attempts[ip]

def ban_ip(ip):
   """Bans the IP address using iptables."""
   if ip not in banned_ips:
     try:

subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
       banned_ips[ip] = datetime.datetime.now() + datetime.timedelta(seconds=BAN_DURATION)
       logging.warning(f"Banned IP: {ip}")
     except Exception as e:
     logging.error(f"An unexpected error occured during IP ban: {e}")

def unban_ips():
  """ Unbans expiered IPs."""
  now = datetime.datetime.now()
  for ip, ban_time in list(banned_ips.items()):
    if now >= unban_time:
      try:
        
subprocess.run(["iptables", "-D", "INPUT, "-s", ip, "-j", "DROP"], check=True)
        del banned_ips[ip]
        logging.info(f"Unbanned IP: {ip}")
      except 
subprocess.CalledProcessError as e:
        logging.error(f"An unexpected error occured during IP unban: {e}")
      except FileNotFoundError:
        logging.error(f"iptables not founf. Ensurenit is installed and in your PATH.")
        logging.error(f"An unexpected error occurred during IP unban: {e}")

def scheduled_tasks():
  """Schedule here."""
  schedule.every(1).minutes.do(parse_ssh_logs)
  schedule.every(1).minutes.do(check_failed_attempts)
  schedule.every(1).minutes.do(unban_ips)

  while True:
    schedule.run_pending()
    time.sleep(60)

def runn_ssh_protection():
  """Runs the SSH protection."""
  scheduled_thread = threading.Thread(target=scheduled_tasks)

if __name__ == "__main__":
  run_ssh_protection()
