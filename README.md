This script scrapes the MD5 sum and GnuPG signature from the mysql.com download page and uses that to verify a previously downloaded file.

Example
=======

    $ ./verify-file.py mysql-5.6.23-linux-glibc2.5-x86_64.tar.gz 
    File: mysql-5.6.23-linux-glibc2.5-x86_64.tar.gz, Checksum: 61affe944eff55fcf51b31e67f25dc10 (OK), Signature: Valid

Requirements
============

* Python
* GnuPG
* Beautiful Soup
* Requests
* python-gnupg

To install the requirements with pip:

    pip install -r requirements.txt

You need to download and trust the MySQL GnuPG key before running this script
