import os
import re
import shutil

def sanitize_python_file(filepath):
    """Sanitizes a Python file by removing potentially harmful code patterns."""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()

        sanitized_lines = []
        for line in lines:
            # Example sanitization rules (modify as needed):
            # Remove system calls (be cautious with this)
            line = re.sub(r'os\.system\(.*\)', '# Removed system call', line)
            line = re.sub(r'subprocess\.run\(.*\)', '# Removed subprocess call', line)
            # Remove potentially dangerous imports (be cautious with this)
            line = re.sub(r'import\s+(os|subprocess|shutil|eval|exec)\b', '# Removed dangerous import', line)
            # Remove eval() and exec() (extremely dangerous)
            line = re.sub(r'\beval\(.*\)', '# Removed eval()', line)
            line = re.sub(r'\bexec\(.*\)', '# Removed exec()', line)

            sanitized_lines.append(line)

        # Write the sanitized content back to the file
        with open(filepath, 'w') as f:
            f.writelines(sanitized_lines)

        print(f"Sanitized: {filepath}")

    except Exception as e:
        print(f"Error sanitizing {filepath}: {e}")

def sanitize_package(src_dir):
    """Sanitizes all Python files within the src directory."""
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                sanitize_python_file(filepath)

if __name__ == "__main__":
    src_dir = "src" # Adjust if your src directory is located elsewhere
    sanitize_package(src_dir)
