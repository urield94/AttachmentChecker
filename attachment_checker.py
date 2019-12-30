"""
EMAIL'S ATTACHMENTS CHECKER
Check if your Gmail account contains malices attachments, via VirusTotal's sandboxes.
"""

import json
import os
import shutil
from time import sleep
from attachment_downloader import download_attachments
from vt_file_checker import FileScanner

VT_SCAN_TIME = 60


class AttachmentChecker:
    def __init__(self):
        self.fs = FileScanner("c049106f01aaba8a67e614517b8c17f0ab05dd04a37bbbcd52b43c8ff9272c78")
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        self.cwd_attachment = f'{self.cwd}/attachments'
        self.reset()

    def reset(self):
        if 'attachments' in os.listdir(self.cwd):
            shutil.rmtree(self.cwd_attachment)
        os.mkdir(f'{self.cwd_attachment}')
        os.mkdir(f'{self.cwd_attachment}/clean')
        os.mkdir(f'{self.cwd_attachment}/not_clean')

    def download(self, username, password):
        download_attachments(username, password, self.fs)

    def scan(self):
        with open(f'{self.cwd_attachment}/attach_json.json', 'r') as fp:
            attach_hashes = json.load(fp)
        attch_summery = {}
        for attach in attach_hashes:
            if os.path.isfile(f'{self.cwd_attachment}/{attach}'):
                status = self.fs.get_file_report(attach_hashes[attach]['hash'])
                if status == "Clean!":
                    shutil.move(f'{self.cwd_attachment}/{attach}', f'{self.cwd_attachment}/clean')
                else:
                    shutil.move(f'{self.cwd_attachment}/{attach}', f'{self.cwd_attachment}/not_clean')
                attch_summery[attach] = {"from": str(attach_hashes[attach]['from']).replace('<', '').replace('>', ''),
                                         "subject": attach_hashes[attach]['subject'],
                                         "status": status}
                with open(f'{self.cwd_attachment}/attch_summery.json', "w") as sum:
                    json.dump(attch_summery, sum)
        return attch_summery

    def download_and_scan(self, username, password):
        self.download(username, password)
        sleep(VT_SCAN_TIME)
        attch_summery = self.scan()
        return attch_summery
