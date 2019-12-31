"""
EMAIL'S ATTACHMENTS CHECKER
Check if your Gmail account contains malices attachments, via VirusTotal's sandboxes.
"""

import json
import os
import shutil
from attachment_downloader import download_attachments
from vt_file_checker import FileScanner


class AttachmentChecker:
    def __init__(self):
        self.fs = FileScanner("c049106f01aaba8a67e614517b8c17f0ab05dd04a37bbbcd52b43c8ff9272c78")
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        self.cwd_attachment = f'{self.cwd}/attachments'

    def reset(self):
        if 'attachments' in os.listdir(self.cwd):
            shutil.rmtree(self.cwd_attachment)
        os.mkdir(f'{self.cwd_attachment}')
        os.mkdir(f'{self.cwd_attachment}/clean')
        os.mkdir(f'{self.cwd_attachment}/not_clean')

    def download(self, username, password):
        self.reset()
        download_attachments(username, password, self.fs)

    def scan(self):
        attch_summery_path = f'{self.cwd_attachment}/attch_summery.json'
        if os.path.isfile(f'{attch_summery_path}'):
            with open(f'{attch_summery_path}', "r") as sum:
                return json.load(sum)

        attch_summery = {}
        with open(f'{self.cwd_attachment}/attach_json.json', 'r') as fp:
            attach_hashes = json.load(fp)
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
