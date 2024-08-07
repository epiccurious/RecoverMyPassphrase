#!/bin/bash

## update the apt package list then install upgrades
sudo apt update && sudo apt upgrade -y

## enable automatic installation of upgrades in debug mode
sudo unattended-upgrade -d

## install the python3-pip package
yes | sudo apt install git python3-pip

# upgrade pip to the latest version
pip install --upgrade pip

## install the BIP39 mnemonic python library
pip install mnemonic

## install tor version 0.4.2.7-1
# sudo apt install -y tor=0.4.2.7-1

## delete existing files, if they exist (in case the script was run multiple times)
rm -rf ~/rmp/bitcoin
rm -f ~/rmp/bitcoin-22.0-x86_64-linux-gnu.tar.gz

## download to the ~/rmp directory and install Bitcoin Core tarball 
wget https://bitcoincore.org/bin/bitcoin-core-22.0/bitcoin-22.0-x86_64-linux-gnu.tar.gz -P ~/rmp
tar xzvf ~/rmp/bitcoin-22.0-x86_64-linux-gnu.tar.gz -C ~/rmp

mv ~/rmp/bitcoin-22.0 ~/rmp/bitcoin

## set the Bitcoin Core binaries to executable
chmod +x ~/rmp/bitcoin/bin/bitcoin-qt
chmod +x ~/rmp/bitcoin/bin/bitcoin-cli

## create a fresh .bitcoin directory and prune the blockchain to 20gb
rm -rf ~/.bitcoin
mkdir ~/.bitcoin
echo "prune=20000" > ~/.bitcoin/bitcoin.conf

## clear the terminal and launch bitcoin-qt 
clear
~/rmp/bitcoin/bin/bitcoin-qt &

echo "Bitcoin blockchain is now synchronizing.
This may take a couple days to a couple weeks depending on the speed of your machine and connection.
Keep your computer connected to A/C power and the Internet. If you get disconnected or your computer hangs, rerun this script.
To maximize the chances everything goes smoothly, sleep and suspend will be disabled."
echo

## disable system sleep, suspend, hibernate, and hybrid-sleep
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target

echo
echo "Please wait while Bitcoin Core initializes then begins syncing block headers.
Do not close this terminal window."

## Pause for 10 seconds to allow Bitcoin Core to open
sleep 10


blockchain_info=$(~/rmp/bitcoin/bin/bitcoin-cli getblockchaininfo)
ibd_status=$(echo "$blockchain_info" | grep "initialblockdownload" | head -c30 | tail -c4)
ibd_progress=$(echo "$blockchain_info" | grep "verificationprogress" | head -c34 | tail -c8 > ~/rmp/syncprogress.txt)

# wait until blockchain sync is at least 0.01% complete
while [[ "$ibd_status" == "true" || "$ibd_status" == "" ]]
do 
   clear
   echo "Please be patient while the bitcoin blockchain syncs to the current state.

The current sync progress is $ibd_progress out of 1.000000.
This step may take over a week, depending on your internet and hardware.
Check the Bitcoin Core application to see more details on the sync progress.

DO NOT CLOSE THIS WINDOW, but if you do simply re-run the script to resume.

This window will update about every 30 seconds."
   sleep 30
   
   # update the sync status, trim to the sixth character from the end, and save to a file syncprogress.txt
   blockchain_info=$(~/rmp/bitcoin/bin/bitcoin-cli getblockchaininfo)
   ibd_status=$(echo "$blockchain_info" | grep "initialblockdownload" | head -c30 | tail -c4)
   ibd_progress=$(echo "$blockchain_info" | grep "verificationprogress" | head -c34 | tail -c8)
done

clear
echo "The blockchain sync process is now complete.
Please press any key to continue."
read -n1

# warning to user about disabling networking with a "press any key" prompt
clear
echo "ATTENTION!

We will now disable networking on the computer.
After entering your private keys, DO NOT RE-ENABLE networking until you securely wipe the hard drive.

Please press any key to continue."
read -n1

# disable networking before inputting the seed words
nmcli networking off

## create a wallet
#~/rmp/bitcoin/bin/bitcoin-cli createwallet rmp false true "" true false true

#STEP TO BE WRITTEN WILL BE TO INPUT THE 24 SEED WORDS FROM THE USER, VALIDATING THEM ONE AT A TIME AGAINST THE FILE seed_words.
#SAVE THE 24 WORDS SEPARATED BY SPACES TO A FILE user_seed.

#OPTIONAL STEP TO ADD ONCE THIS SCRIPT IS WRITTEN - CHECKSUM THE SEED WORDS AND REPORT TO THE USER IF IT FAILS.

## execute the python script to generate WIF-format seeds using the mnemonic library
## which will use the words from user_seed the openwall_passwords to generate WIF-format keys and save then to a new file wif_keys.
#python3 ~/rmp/generate_keys.py

## iterate through wif_keys, the list of generated WIF-format keys
#for each line in the file...
#~/rmp/bitcoin/bin/bitcoin-cli sethseed false <WIF seed>
#then check the balance
#if a balance exists, use the line number (iterator)
#to check the passphrase list to get the associated passphrase
#then write the passphrase, WIF-format seed and balance amount to a new file found_money.
#echo to the user that "a balance of XX was found using passphrase YYYY."

python3 generate_bip32_seeds.py

wif_keys_file='wif_private_keys'
passphrase=''

# Iterate over each line in the input file
for line in $(cat "${wif_keys_file}"); do
    case "${line}" in
        passphrase=*)
            # Extract the passphrase
            passphrase="${line#passphrase=}"
            echo "New passphrase set: ${passphrase}"
            ;;

        L*|K*)
            # Import the private key into Bitcoin Core
            private_key="${line}"
            echo "Importing private key: ${private_key}"

            # Use bitcoin-cli to import the private key
            # Replace `your_wallet_name` with the actual wallet name or omit if not using a specific wallet
            bitcoin-cli importprivkey "${private_key}"
            ;;

        *)
            # Handle any unexpected lines if necessary
            echo "Unrecognized line: ${line}"
            ;;
    esac
done