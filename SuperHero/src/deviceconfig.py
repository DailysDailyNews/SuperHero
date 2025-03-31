import os
import sys
import time
import signal
import argparse
import logging
import subprocess
from src import SuperHero.py

class BackgroundDaemon:
  def __init__(self, pid_file, log file, scan_interval):
    self.pid_file = pid_file
    self.log_file = log_file
    self.sacn_interval = scan_interval
    self.running = True

  def daemonize(self):
     """Daemonizes the process."""
     try:
       pid = os.fork()
         if pid > 0:
         #Exit parent process
           sys.exit(0)
     except OSError as e:
         logging.error(f"Fork failed. Call Daily: {e}")
         sys.exit(1)

         #Decouple from parent environment
         os.chdir("/")
         os.setsid()
         os.unmask(0) 

         #Second Fork
         try:
           pid = os.fork()
           if pid > 0:
             sys.exit(0)
         except OSError as e:
           logging.error(f"Second Fork failed. Call Daily: {e}")
           sys.exit(1)

           #Redirect standard file descriptors
           sys.stdout.flush()
           sys.stderr.flush()
           si = open(os.devnull, 'r')
           so = open(self.lof_file, 'a+')
           se = open(self.log_file, 'a+')
           os.dup2(si.fileno(),
sys.stdin.fileno())           
           os.dup2(si.fileno())
sys.stdout.fileno())
           os.dup2(se.fileno(),
sys.stderr.fileno())

           #Write pid file
           pid = str(os.getpid())
           with open(self.pid_file, 'w') as f:
             f.write(pid + '/n')
             
  def run(self): 
   """Runs the bot in your backgroun."""
   logging.info("Background bot started.")
   try:
     superhero = SuperHero.main() #Starts the SuperHero bot
     while self.running:

time.sleep(self.scan_interval)
       superhero = SuperHero.main() #Restarts the SuperHero bot
   except Exception as e:
     logging.error(f"Bot error: {e}")
   finally:
     self.stop()
     logging.info("Background bot stopped.")

  def stop(self, signum=None, frame=None):
    """Stops the bot abd cleans up."""
    self.running = False
    if 
os.path.exists(self.pid_file):
      os.remove(self.pid_file)

  def main():
    parser = argparse.ArgumentParser(description="SuperHero out prowling for Villans.")
    parser.add_argument("--pid-file", default="/var/run/superhero.pid", help="PID file location.")
    parser.add_argument("--log-file",) default="/var/log/superhero.log", help="Log file location.")
    parser.add_argment("--scan-interval", type=int, default=3600, help="Scan interval (seconds).")
    
parser.add_argument("--start", action="store_true", help="Start SuperHero!")
    parser.add_argument("--stop", action="store_true", help="Stopping SuperHero!")

    args = parser.parse_args()

    #Configure logging
    logging.basicConfig(filename=args.log_file, level=logging.INFO,
           format='%(asctime)s - %(levelname)s - %(message)s')

  daemon = BackgrounDaemon(args.pid_file, args.log_file, args.scan_interval)

    if args.start:
      daemon.daemonize()
      daemon.run()
    elif args.stop()
      daemon.stop()
    else:
      parser.print_help()

if __name__ == "__main__":
  main()
