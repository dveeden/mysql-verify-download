#!/usr/bin/python
import os
import sys
import hashlib
from StringIO import StringIO

import requests
import bs4
import gnupg

def get_metadata():
    data_checksums = {}
    base_url='https://dev.mysql.com/downloads/mysql/%s.html'
    for version in ['5.1', '5.5', '5.6', '5.7']:
        url = base_url % version
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.text)
        table = soup.find('table', attrs={'class':'table04'})
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [x.text.strip() for x in cols]
            if cols[1].startswith('MD5'):
              filename, checksum = cols
              filename = filename[1:-1]
              checksum = checksum.split(' ')[1]
              data_checksums[filename] = checksum
    return data_checksums

def check_md5(filename):
    with open(filename, 'rb') as fh:
        filehash = hashlib.md5(fh.read()).hexdigest()
        return filehash

def check_gpg(filename):
    gpg = gnupg.GPG(gnupghome=os.path.expanduser('~/.gnupg'))
    url = 'https://dev.mysql.com/downloads/gpg.php?file=%s' % filename
    page = requests.get(url)

    filesig = ''
    sigpart = False
    for line in page.text.split('\n'):
        if line.startswith('-----BEGIN PGP SIGNATURE-----'):
            filesig += line 
            filesig += '\n'
            sigpart = True
        elif line.startswith('-----END PGP SIGNATURE-----'):
            filesig += line
            filesig += '\n'
            sigpart = False
        elif sigpart:
            filesig += line
            filesig += '\n'
    r = gpg.verify_file(StringIO(filesig), filename)
    return r.valid
    

if __name__ == "__main__":
    checksumdata = get_metadata()
    for filename in sys.argv[1:]:
        try:
            filemd5 = checksumdata[filename] 
        except KeyError:
            print("No checksum found for %s" % filename)
        output = "File: %s" % filename
        filehash = check_md5(filename)
        gpgvalid = check_gpg(filename)
        if filehash == filemd5: 
            output += ", Checksum: %s (OK)" % filemd5
        else:
            output += ", Checksum: %s (FAIL)" % filemd5
        if gpgvalid:
            output += ", Signature: Valid"
        else:
            output += ", Signature: INVALID"
        print(output)
