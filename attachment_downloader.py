import email
import imaplib
import json
import os


def download_attachments(username, password, fs, cwd):
    try:
        attach_hashes = {}
        imapSession = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        typ, accountDetails = imapSession.login(username, password)
        if typ != 'OK':
            print('Not able to sign in!')
            raise Exception

        imapSession.select('"[Gmail]/All Mail"')
        typ, data = imapSession.search(None, 'ALL')
        if typ != 'OK':
            print('Error searching Inbox.')
            raise Exception

        # Iterating over all emails
        for msgId in data[0].split():
            typ, message_parts = imapSession.fetch(msgId, '(RFC822)')
            if typ != 'OK':
                print('Error fetching mail.')
                raise Exception

            email_body = message_parts[0][1].decode()
            mail = email.message_from_string(email_body)
            for part in mail.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                file_name = part.get_filename()

                if bool(file_name):
                    filePath = os.path.join(cwd, 'attachments', file_name)
                    print(file_name)
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                    file_hash = fs.send_file_to_scan(filePath)
                    attach_hashes[file_name] = {'hash': file_hash, 'from':mail['From'], 'subject': mail['Subject']}

        imapSession.close()
        imapSession.logout()
        with open(f'{cwd}/attachments/attach_json.json', 'w') as fp:
            json.dump(attach_hashes, fp)

    except Exception as e:
        print(f'Not able to download all attachments - {e}')
