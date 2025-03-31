import os
import platform
import logging

class LocalStorageBlocker:
    def __init__(self, log_file="local_storage_blocker.log"):
        self.log_file = log_file
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger("LocalStorageBlocker")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def block_local_storage(self):
        """Blocks local storage access from Browsers."""
        system = platform.system()

        if system == "Windows":
            self._block_windows()
        elif system == "Darwin":  # macOS
            self._block_macos()
        elif system == "Linux":
            self._block_linux()
        else:
            self.logger.warning(f"Unsupported operating system: {system}")

    def _block_windows(self):
        """Blocks local storage on Windows."""
        try:
            user_profile = os.environ["USERPROFILE"]
            browser_storage_paths = [
                os.path.join(user_profile, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Local Storage"),
                os.path.join(user_profile, "AppData", "Roaming", "Mozilla", "Firefox", "Profiles"),
                os.path.join(user_profile, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Local Storage"),
                # Add more paths if needed
            ]

            for path in browser_storage_paths:
                if os.path.exists(path):
                    os.chmod(path, 0o000)  # Removes all permissions
                    self.logger.info(f"Blocked local storage access: {path}")

        except Exception as e:
            self.logger.error(f"Error blocking Windows local storage: {e}")

    def _block_linux(self):
        """Blocks local storage on Linux."""
        try:
            home_dir = os.path.expanduser("~")
            browser_storage_paths = [
                os.path.join(home_dir, ".config", "google-chrome", "Default", "Local Storage"),
                os.path.join(home_dir, ".mozilla", "firefox"),
                os.path.join(home_dir, ".config", "microsoft-edge", "Default", "Local Storage"),
                # Add more paths if needed, such as for Chromium
            ]

            for path in browser_storage_paths:
                if os.path.exists(path):
                    os.chmod(path, 0o000)  # Removes all permissions
                    self.logger.info(f"Blocked local storage access: {path}")

        except Exception as e:
            self.logger.error(f"Error blocking Linux local storage: {e}")

    def _block_macos(self):
        """Blocks local storage on macOS."""
        try:
            home_dir = os.path.expanduser("~")
            browser_storage_paths = [
                os.path.join(home_dir, "Library", "Application Support", "Firefox", "Profiles"),
                os.path.join(home_dir, "Library", "Application Support", "Microsoft Edge", "Default", "Local Storage"),
                # Add more paths if necessary
            ]

            for path in browser_storage_paths:
                if os.path.exists(path):
                    os.chmod(path, 0o000)  # Removes all permissions
                    self.logger.info(f"Blocked local storage access: {path}")

        except Exception as e:
            self.logger.error(f"Error blocking macOS local storage: {e}")

if __name__ == "__main__":
    blocker = LocalStorageBlocker()
    blocker.block_local_storage()
