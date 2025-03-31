import os
import platform
import logging
import subprocess

class NodeBlocker:
    def __init__(self, log_file="node_blocker.log"):
        self.log_file = log_file
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger("NodeBlocker")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def block_node(self):
        """Blocks Node.js execution and installation."""
        system = platform.system()

        if system == "Windows":
            self._block_windows()
        elif system == "Linux":
            self._block_linux()
        elif system == "Darwin": # macOS
            self._block_macos()
        else:
            self.logger.warning(f"Unsupported operating system: {system}")

    def _block_windows(self):
        """Blocks Node.js on Windows."""
        try:
            # Block Node.js executables by renaming them
            node_paths = [
                os.path.join(os.environ["ProgramFiles"], "nodejs", "node.exe"),
                os.path.join(os.environ["ProgramFiles(x86)"], "nodejs", "node.exe"),
                os.path.join(os.environ["LOCALAPPDATA"], "npm", "node.exe"),
                # Add more Node.js paths as needed
            ]

            for path in node_paths:
                if os.path.exists(path):
                    new_path = path + ".blocked"
                    os.rename(path, new_path)
                    self.logger.info(f"Blocked Node.js: {path}")

            # Block npm (Node Package Manager)
            npm_paths = [
                os.path.join(os.environ["ProgramFiles"], "nodejs", "npm.cmd"),
                os.path.join(os.environ["ProgramFiles(x86)"], "nodejs", "npm.cmd"),
                os.path.join(os.environ["LOCALAPPDATA"], "npm", "npm.cmd"),
                # Add more npm paths as needed
            ]

            for path in npm_paths:
                if os.path.exists(path):
                    new_path = path + ".blocked"
                    os.rename(path, new_path)
                    self.logger.info(f"Blocked npm: {path}")

        except Exception as e:
            self.logger.error(f"Error blocking Windows Node.js: {e}")

    def _block_linux(self):
        """Blocks Node.js on Linux."""
        try:
            # Block Node.js executables by renaming them
            node_paths = [
                "/usr/bin/node",
                "/usr/local/bin/node",
                "/opt/node/*/bin/node",
                # Add more Node.js paths as needed
            ]

            for path in node_paths:
                if os.path.exists(path):
                    new_path = path + ".blocked"
                    os.rename(path, new_path)
                    self.logger.info(f"Blocked Node.js: {path}")

            # Block npm
            npm_paths = [
                "/usr/bin/npm",
                "/usr/local/bin/npm",
                # Add more npm paths as needed
            ]

            for path in npm_paths:
                if os.path.exists(path):
                    new_path = path + ".blocked"
                    os.rename(path, new_path)
                    self.logger.info(f"Blocked npm: {path}")

        except Exception as e:
            self.logger.error(f"Error blocking Linux Node.js: {e}")

    def _block_macos(self):
        """Blocks Node.js on macOS."""
        try:
            # Block Node.js executables by renaming them
            node_paths = [
                "/usr/bin/node",
                "/usr/local/bin/node",
                "/opt/homebrew/bin/node",
                # Add more Node.js paths as needed
            ]

            for path in node_paths:
                if os.path.exists(path):
                    new_path = path + ".blocked"
                    os.rename(path, new_path)
                    self.logger.info(f"Blocked Node.js: {path}")

            # Block npm
            npm_paths = [
                "/usr/bin/npm",
                "/usr/local/bin/npm",
                "/opt/homebrew/bin/npm",
                # Add more npm paths as needed
            ]

            for path in npm_paths:
                if os.path.exists(path):
                    new_path = path + ".blocked"
                    os.rename(path, new_path)
                    self.logger.info(f"Blocked npm: {path}")

        except Exception as e:
            self.logger.error(f"Error blocking macOS Node.js: {e}")

if __name__ == "__main__":
    blocker = NodeBlocker()
    blocker.block_node()
