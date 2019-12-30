"""
EMAIL'S ATTACHMENTS CHECKER
Check if your email contains malices attachments.
"""

import getpass
import json
import os
import shutil
import sys
from time import sleep
from attachment_downloader import download_attachments
from vt_file_checker import FileScanner

if __name__ == "__main__":
    fs = FileScanner("c049106f01aaba8a67e614517b8c17f0ab05dd04a37bbbcd52b43c8ff9272c78")
    cwd = os.path.dirname(os.path.abspath(__file__))
    cwd_attachment = f'{cwd}/attachments'
    if 'attachments' not in os.listdir(cwd):
        os.mkdir(f'{cwd_attachment}')
    if 'clean' not in os.listdir(f'{cwd_attachment}'):
        os.mkdir(f'{cwd_attachment}/clean')
    if 'not_clean' not in os.listdir(f'{cwd_attachment}'):
        os.mkdir(f'{cwd_attachment}/not_clean')

    if len(sys.argv) != 3:
        username = input('Enter your Gmail username:')
        password = getpass.getpass('Enter your password:')
    else:
        username = sys.argv[1]
        password = sys.argv[2]

    download_attachments(username, password, fs)
    sleep(60)

    with open(f'{cwd_attachment}/attach_json.json', 'r') as fp:
        attach_hashes = json.load(fp)
    for attach in attach_hashes:
        if os.path.isfile(f'{cwd_attachment}/{attach}'):
            status = fs.get_file_report(attach_hashes[attach]['hash'])
            if status == "Clean!":
                shutil.move(f'{cwd_attachment}/{attach}', f'{cwd_attachment}/clean')
            else:
                shutil.move(f'{cwd_attachment}/{attach}', f'{cwd_attachment}/not_clean')

            with open(f'{cwd_attachment}/attch_summery', "a") as sum:
                sum.write(f"{attach} - "
                          f"from: {attach_hashes[attach]['from']}, "
                          f"Subject: {attach_hashes[attach]['subject']}, "
                          f"Status: {status}\n")
