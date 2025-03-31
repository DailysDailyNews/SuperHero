import random
import time
import schedule
import threading
import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# List of Fake Agents
USER_AGENTS = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
  "Mozilla/5.0 (Windows NT 6.1; Win32; x32) Gecko/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
  "Googlebot/2.1 (http://www.googlebot.com/bot.html)",
  "DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)",
  "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
  "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
  "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
]

# List of Fake IP addresses (IPv4)
FAKE_IPS = [
  "555.237.1.456",
  "777.643.6.000",
  "10.0.100.700",
  "8.8.8.8"
  "1.1.1.1"
  "0.0.0.0"
  "203.0.113.1"
  "111.111.1.111"
]

current_user_agent_and_ip():
   """Changes the User-Agent and Ip address"""
   global current_user-agent, current_ip = random.choice(USER_AGENTS), random.choice(FAKE_IPS)
   logging.info(f"User-Agent changed to: {current_user_agent}")
   logging.info(f"IP address changed to: {curret_ip}")

def get_headers():
   """Returns the current headers."""
   return {
     "User-Agent": current_user_agent,
     "X-Forwarded-For": current_ip,
}

def scheduled_changed():
   """Schedules the User-Agent and IP change every 5 minutes."""
   logging.info(f"Scheduleing User-Agent and IP change every five minutes.")
   schedule.every(5).minutes.do(change_user_agent_and_ip)

   while True:
     schedule.run_pending()
     time.sleep(60) # Checks every minute

def run_protection():
   """Runs the protection."""
   logging.info("Starting the protection.")
   current_user_agent, current_ip = random.choice(USER_AGENTS), random.choice(FAKE_IPS)
   change_thread = threading.Thread(target=scheduled_changed)
   change_thread.start()

def make_request():
  """Makes a request with the current headers."""
   try:
     headers = get_headers()
     response = requests.get(url, headers=headers)
     logging.info(f"Request to {url} was successful. Status code: {response.status_code}")
     #Process the response as needed
   except requests.exceptions.RequestException as e:
     logging.error(f"Request to {url} failed: {e}")

if __name__ == "__main__":
  run_protection()
   make_request("localhost:8080")
  while True:
    time.sleep(1000) # Sleeps
