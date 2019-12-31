import json
import requests
from virustotal_python import virustotal as VT


class FileScanner:
    def __init__(self, api_key):
        self.api_key = api_key
        self.vt = VT.Virustotal(api_key)
        self.report_url = 'https://www.virustotal.com/vtapi/v2/file/report'

    def send_file_to_scan(self, filename):
        scan_res = self.vt.file_scan(filename)
        self.vt.file_rescan(filename)
        return scan_res['json_resp']['resource']

    def get_file_report(self, file_hash):
        params = {'apikey': self.api_key, 'resource': file_hash, 'allinfo': 'true'}
        while True:
            try:
                report_res = requests.get(self.report_url, params=params)
                scans = json.loads(report_res.text)["scans"]
                total_scans = len(scans)
                mal_scans = 0
                for scan in scans:
                    if scans[scan]['result'] is not None:
                        mal_scans += 1
                print(f"Got report for {file_hash}!")
                if mal_scans/total_scans > 0.05:
                    return "Infected!"
                elif 0 < mal_scans/total_scans < 0.05:
                    return "Might be infected"
                else:
                    return "Clean!"
            except Exception as e:
                print(f"Trying to get report for hash {file_hash}")
