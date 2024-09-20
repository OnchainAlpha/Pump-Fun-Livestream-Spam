from pathlib import Path
import subprocess


chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
debugging_port = '--remote-debugging-port=8989'
user_data_dir = '--user-data-dir={}'.format(Path.cwd() / 'profile')


subprocess.Popen([chrome_path, debugging_port, user_data_dir])