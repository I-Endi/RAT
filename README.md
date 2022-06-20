# RAT malware demostration
Made by computer science students of the Technical University of Eindhoven.

<hr>

DISCLAIMER: **This repo is created to demonstrate how a remote backdoor works. Hacking without permission is illegal. This is strictly educational for learning about malware cyber-security in the areas of ethical hacking so that we can protect ourselves against the real black-hat hackers.**

<hr>

# Usage

## Set-up
Set up a safe virtual network with both a **Windows 10** machine and any other OS able to listen for connections on a specified port (to test this, **Parrot OS** was used).

## Usage
**First of all**: change the IP value to the correct IP address of the listener machine at the bottom of ```client/src/client_main/py```

### To test without building a .exe
**Client:** Run ```client/src/client_main/py```
**Server:** Listen on specified port for connections (default set to 9001) using any command like: ```nc -lvnp 9001```

### To test with an executable
**Client:** Build the executable file using ```output/pyinstaller.txt``` or ```output/pymake.py```
**Server:** Same as above, listen to specified port
