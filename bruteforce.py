#!/usr/bin/env python3

import zipfile
import argparse
import threading
import time


# Class with all the console colours
class PrintColours:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    FAIL = '\033[91m'
    END = '\033[0m'


# Unzip thread
class ZipThread(threading.Thread):

    def __init__(self, zip_file, words, offset, step):
        threading.Thread.__init__(self)
        self.kill = False
        self.zip_file = zip_file
        self.words = words
        self.offset = offset
        self.step = step
        self.words_attempted = 0

    def run(self):
        global cracked
        global final_password
        global t2

        # Literate through wordlist, with a given step and offset
        for i in range(self.offset, len(words), self.step):
            try:
                password = words[i].strip()
                self.words_attempted += 1

                # Attempt to extract the files with the password
                zip_file.extractall(pwd=password.encode())

                # Output the password, stop other threads
                print("\n" + PrintColours.GREEN + "[+]" + PrintColours.END + " Password found: " + password)
                final_password = password
                cracked = True

                # Print the time taken
                t2 = time.time()
                print(PrintColours.GREEN + "[+]" + PrintColours.END + " Time taken: " + str(round(t2 - t1, 2)) + "s")

            # If the extraction failed...
            except Exception:
                if self.kill:
                    return
        return


# Get the total number of password attempts
def total_attempts(thread_list):

    total = 0

    for thread in thread_list:
        total += thread.words_attempted

    return total


# Kill all threads
def kill_all(thread_list):
    for thread in thread_list:
        thread.kill = True


if __name__ == "__main__":

    # Create a parse our arguments
    parser = argparse.ArgumentParser(description="Run a password protected ZIP file against a wordlist")
    parser.add_argument("zipfile", metavar="zipfile", help="ZIP file")
    parser.add_argument("wordlist", metavar="wordlist", help="Path to the wordlist to use")
    parser.add_argument("-t", dest="threads", default=1, type=int, help="Number of threads to spawn")

    args = parser.parse_args()

    cracked = False
    final_password = ""

    zip_file = zipfile.ZipFile(args.zipfile)
    threads = args.threads
    wordlist = args.wordlist

    # Open the wordlist
    with open(wordlist, errors="ignore") as file:
        words = file.readlines()

    wordlist_len = len(words)

    # Notify the user
    print(PrintColours.BLUE + "[-]" + PrintColours.END + " Loaded " + str(wordlist_len) + " words from wordlist...")

    thread_processes = []

    # Start the timer
    t1 = time.time()

    # Create threads
    for i in range(threads):
        thread_processes.append(ZipThread(zip_file, words, i, threads))
        thread_processes[-1].start()

    print(PrintColours.BLUE + "[-]" + PrintColours.END + " Spawned " + str(threads) + " thread(s)")

    while cracked == False:

        try:
            # Get the total number of attempts and display to user
            attempts = total_attempts(thread_processes)
            attempts_str = PrintColours.BLUE + "[-]" + PrintColours.END + " Attempted " + str(attempts) + "/" + str(wordlist_len) + " words"

            # Get the percentage of passwords attempted
            percent = round(((attempts / wordlist_len) * 100), 1)
            percent_str = " (" + str(percent) + "%)..."
            print(attempts_str + percent_str, end="\r")

            # Check if we've exhaused the wordlist
            if attempts >= wordlist_len:
                print("\n" + PrintColours.FAIL + "[!]" + PrintColours.END + " Password not found")
                break

            # Wait 1 second
            time.sleep(1)

        # Catch Ctrl + C
        except KeyboardInterrupt:
            kill_all(thread_processes)
            print("\n\n" + PrintColours.FAIL + "[!]" + PrintColours.END + " Quitting...")
            exit()

    kill_all(thread_processes)
    zip_file.extractall(pwd=final_password.encode())
