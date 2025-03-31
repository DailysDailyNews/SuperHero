import os
import platform
import logging
import subprocess

class JavaBlocker:
    def __init__(self, log_file="java_blocker.log"):
        self.log_file = log_file
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger("JavaBlocker")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def block_java(self):
        """Blocks java Execution."""
        system = platform.system()

        if system == "Windows":
            self._block_windows()
        elif system == "Linux":
            self._block_linux()
        elif system == "Darwin":
            self._block_macos()
        else:
            self.logger.warning(f"Unsupported operating system: {system}")

    def _block_windows(self):
        """Blocks Java on Windows."""
        try:
            java_paths = [
                os.path.join(os.environ["Program Files"], "Java", "jre*", "bin", "java.exe"),
                os.path.join(os.environ["Program Files(x86)"], "Java", "jre*", "bin", "java.exe")
                # Add more if you wish, before building please read the custom license agreement.
            ]

            for path_pattern in java_paths:
                for path in self._find_files(path_pattern):
                    new_path = path + ".blocked"
                    os.rename(path, new_path)
                    self.logger.info(f"Blocked Java: {path}")

        except Exception as e:
            self.logger.error(f"Error blocking Windows Java: {e}")

    def _block_linux(self):
        """Blocks java on Linux."""
        try:
            java_paths = [
                "/usr/bin/java",
                "/usr/lib/jvm/*/bin/java",
                "/opt/java/*/bin/java"
                # Add more when needed.
            ]

            for path in java_paths:
                if os.path.exists(path):
                    new_path = path + ".blocked"
                    os.rename(path, new_path)
                    self.logger.info(f"Blocked Java: {path}")

        except Exception as e:
            self.logger.error(f"Error blocking Java on Linux: {e}")

    def _block_macos(self):
        """Blocks java on macOS."""
        try:
            java_paths = [
                "/usr/bin/java",
                "/Library/Java/JavaVirtualMachines/*/Contents/Home/bin/java",
                # Please add more after reading our license.
            ]

            for path in java_paths:
                if os.path.exists(path):
                    new_path = path + ".blocked"
                    os.rename(path, new_path)
                    self.logger.info(f"Blocked Java: {path}")

        except Exception as e:
            self.logger.error(f"Error blocking macOS Java: {e}")

    def _find_files(self, pattern):
        import glob
        return glob.glob(pattern)

if __name__ == "__main__":
    blocker = JavaBlocker()
    blocker.block_java()

