# RecoverMyPassphrase
Attempt to recover your bitcoin funds through brute force in the event you lose/forget your BIP39 passphrase. This project assumes you used a Trezor to generate the passphrase-protected wallet and know all 24 of your BIP39 mnemonic seed words.

WARNING!!!! Code is under development. DO NOT TRUST THIS CODE WITH YOUR SEED WORDS YET. This code should be used for research, testing, and development purposes until further notice.

WHAT THIS CODE DOES (ERR...WILL DO ONCE IT'S RELEASED...IT'S NOT RELEASED YET.)

Download, install, and configure Bitcoin Core Launch Bitcoin Core and begin syncing the blockchain Disable sleep, suspend, and other power options after confirming with the user Wait until the initial block download has completed Disable all network access after confirming with the user Input all 24 BIP39 seed words from the user, validated against the approved word list Iterate through the Openwall password dictionary, generate WIF private keys, and save them to wallet_WIF_seeds.lst Iterate through the WIF keys, import them into into Bitcoin Core, check for a non-zero balance Build a list of nonzero wallets in balancesFound.lst Report to the user the results live as they are computed INSTRUCTIONS FOR INITIALIZING THE SCRIPT

The short instructions only for experienced Ubuntu users are to completely wipe the laptop hard drive, install the most recent Ubuntu LTS version, install all software patches, open Terminal, and run "sudo apt update; sudo apt install -y git; git clone https://github.com/epiccurious/recovermypassphrase.git ~/rmp; bash ~/rmp/start.sh".

The longer instructions (for non-technical users) are broken into FIRST, SECOND, and THIRD parts.

The FIRST part walks through how to installs the Ubuntu Operating System. The SECOND part installs software updates, which can include critical security patches. The THIRD part verifies all updates are installed and initiates the bash script.

FIRST, we will wipe the laptop's hard drive and install Linux (Ubuntu) operating system:

Source laptop hardware that is compatible with modern Ubuntu. Wipe the hard drive and install the current "LTS" version of Ubuntu using this guide: https://ubuntu.com/tutorials/install-ubuntu-desktop In Step 5 of the Ubuntu installation guide, choose "Minimal Installation" rather than normal. Also in Step 5 of the Ubuntu installation guide, In Step 6 of the Ubuntu installation guide, make sure to choose "Erase disk and install ubuntu." In Step 7 of the Ubuntu installation guide, make sure to "Use LVM" and check "Encrypt the new Ubuntu installation". Choose a strong password to encrypt the disk. In Step 9 of the Ubuntu installation guide, choose a strong user account password and select "Require my password to log in". At the end of Step 10 of the Ubuntu installation guide, choose the most private options: DO NOT connect your online accounts. Click "Skip" at the top-right of the Online Accounts page. DO NOT setup Livepatch. Click "Next" at the top-right of the Livepatch page. OPT OUT of hardware sharing. Choose the option for "No, don't send system info" then click "Next" on the Help Improve Ubuntu page. DO NOT enable location services. Leave the toggle disabled then click "Next" on the Welcome To Ubuntu page. DO NOT download additional apps software. Click "Done" on the Ready To Go page. SECOND, we will install software patches:

Make sure you are connected to the internet either through Wi-Fi or wired ethernet. Click on the nine dots at the bottom-left of the screen to Show Applications Open Software Updater, which has a grey not purple icon. Click "Install Now" at the bottom-right. When Ubuntu finishes updating prompts you to restart the computer, click "Restart Now". (Alternatively, you can accomplish this by opening Terminal with Ctrl+Alt+T, typing "sudo apt update && yes | sudo apt upgrade; shutdown -r" without quotation marks, and pushing Enter.) THIRD, ensure all software updates are installed then start the script:

Wait for the computer to finish restarting then log back into the user account. Verify all software updates are installed by opening Software Updater program again. You should see a popup saying "The software on this computer is up to date.". Click "OK" to close that popup. Open the Terminal application with Ctrl+Alt+T (or by clicking the 9 dots in the bottom-left to Show Applications then clicking Terminal.) You should see a dark Terminal window open with some characters followed by a "$" then a space then a white rectangle representing the cursor. Paste (or type) the following command into Terminal without quotation marks and push Enter: "sudo apt update; sudo apt install -y git; git clone https://github.com/epiccurious/recovermypassphrase.git ~/rmp; bash ~/rmp/initialize.sh" NOTE: the 22nd character in that command (|) is a vertical bar aka a "pipe", not an upper-case "I" or lower-case "l". You can type it by holding Shift and pushing the key just below Backspace. Type in your user account password and push Enter. (You will not be able to see the characters as you type.) The script will eventually open Bitcoin Core and begin syncing the blockchain. At the prompt in Terminal, press any key to disable specific power options (sleep, suspend, and hybernate, and hybrid-sleep) that can interfere with the blockchain sync process. You may need to type in your user account password at this step. As the blockchain syncs, the script should continue updating with the current sync status. If you lose power or accidentally close the terminal window, re-run the script by typing "bash ~/rmp/initialize.sh" without quotation marks into Terminal and push Enter. Once the blockchain is fully synced ("1.000000/1.000000") continue following the prompts to disable internet access, enter your 24 seed words (only after the script disables internet for your system, and begin attempting to brute-force crack your passphrase.
