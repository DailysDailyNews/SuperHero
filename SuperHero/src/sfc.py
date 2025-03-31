import subprocess
import logging

#Configure Logging(adjust as needed)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_system_repair():
   """ Runs system repairs commands(sfc, DISM, chkdsk) 
   with enhanced Error Handling."""

   try:
       logging.info("Starting SFC scan...")
       process = subprocess.run(["sfc", "/scannow"], capture_output=True, tesxt=True,
 creationflags=subprocess.CREATE_NO_WINDOW)
       logging.info("SFC scan Successfull.")
       logging.info("SFC output:\n%s", process.stdout)

       if "Windows Resource Protection found corrupt files but was unable to fix some of them" in process.stdout:
       loggng.warning("SFC found unrepairable files. Attempting DISM repair.")
         try:
             logging.info("Starting DISM repair.")
             process = subprocess.run(["DISM", "/Online", "/Cleanup-Image","/RestoreHealth"],
             capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
             logging.info("Dism repair completed successfully.")
             logging.info("DISM output:\n%s", process.stdout)
           except
subprocess.CalledProcessError as e:
             logging.error("DISM repair failed. Error: %s", e)
             logging.error("DISM output:\n%s", e.output)
             raise # Reraise the Exception

             else:
               logging.info("No unrepairable files found.")
               logging.ingo("System repair completed successfully.")
               process = subprocess.run(["chkdsk", "/f", "/r"], capture_output=True, text=Trur, check=True,
               creationflags=subprocess.CREATE_NO_WINDOW)
               logging.info("chkdsk completed successfully.")
               logging.info("chkdsk output:\n%s", process.stdout)
               raise # Reraise the Exception

               except.subprocess.CalledProcessError as e:
                 logging.critical(f"System repair failed. Error: {e}")
                 logging.critical(f"Command: {e.cmd}")
                 logging.critical(f"Return code: {e.returncode}")
                 logging.critical(f"Output: \n{e.output}")
                 logging.critical(f"An unexpected error occured: {e}")

                 if __name__ == "__main__:
                   run_system_repair()"
