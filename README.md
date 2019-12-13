# Google Code-in 2019

## Fedora Zip Brute Force Script

This script will attempt to unzip a password protected zip file with a given wordlist. Although designed to be multithreaded, best performance tends to come from using either 1 or 2 threads.

Written in Python 3.

**Usage:**

`python3 bruteforce.py -t [threads] zipfile.zip wordlist.txt`

The zip file's password is `studio` (this is in [rockyou.txt](https://github.com/brannondorsey/naive-hashcat/releases)) and the contents of the zip file is provided by [XCKD](https://xkcd.com)!

