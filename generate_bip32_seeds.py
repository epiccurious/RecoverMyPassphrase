import sys
from mnemonic import Mnemonic
from bip32utils import BIP32Key

def derive_private_keys(seed_phrase: str, passphrase: str) -> str:
    """
    Derives a private key from a BIP39 seed phrase and passphrase.

    :param seed_phrase: The BIP39 seed phrase.
    :param passphrase: The passphrase used with the seed phrase.
    :return: The private key in Wallet Import Format (WIF).
    """
    # Initialize the Mnemonic class for the English word list
    mnemo = Mnemonic("english")

    # Convert the seed phrase to a binary seed using the passphrase
    seed = mnemo.to_seed(seed_phrase, passphrase)

    # Create the root BIP32 key from the seed
    root_key = BIP32Key.fromEntropy(seed)

    # Initialize array of derivation paths and private keys
    # Trezor devices have three paths 44'/0'/0', 49'/0'/0', and 84'/0'/0'
    derivation_paths = [44, 49, 84]
    private_keys = []

    for derivation_path in derivation_paths:
        # Derive the child key /0'/0' at derivatio path
        child_key = root_key.ChildKey(derivation_path).ChildKey(0).ChildKey(0)
        # Convert private key to WIF format
        private_key = child_key.WalletImportFormat()
        # Add the private key to the array of WIF-format keys
        private_keys.append(private_key)
    
    # Return an array of strings of WIF-format private keys
    return private_keys

def load_password_list(file_path: str) -> list[str]:
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def remove_wif_duplicates(file_path: str):
    output_path = file_path

    lines = open(file_path, 'r').readlines()
    unique_lines = set(line.strip() for line in lines)

    with open(output_path, 'w') as file:
        for line in sorted(unique_lines):
            file.write(f"{line}\n")

def main():
    output_file_path='wif_private_keys'
    # password_list_path='openwall/openwall_passwords'
    # Use mini file for development and debugging only
    password_list_path='openwall/openwall_passwords_mini'

    # Define your BIP39 seed phrase and passphrase
    seed_phrase = 'program traffic coil weather sleep black push retreat recall oil chief cement ability tonight must give margin tragic risk edit page impose assist dust'
    #passphrase = 'apple'
    try:
        password_list = load_password_list(password_list_path)
    except Exception as e:
        print(f'Error loading password list from {password_list_path}: {e}')
        sys.exit(1)

    # Open the output file in write mode to clear any existing contents
    with open(output_file_path, 'w') as output_file:
        # Iterate throuch each password
        for passphrase_to_check in password_list:
            print(f'Found a password: {passphrase_to_check}')

            # Derive the WIF-format private keys to import into Bitcoin Core
            try:
                wif_private_keys_to_import = derive_private_keys(seed_phrase, passphrase_to_check)
            except Exception as e:
                print(f'Error deriving private keys for passphrase {passphrase_to_check}: {e}')
                sys.exit(1)

            # Save the passphrase and each WIF key to the output file
            try:
                output_file.write(f'passphrase={passphrase_to_check}\n')
                # Print the private keys
                print(f'The BIP32 private keys for {passphrase_to_check} are:')
                for wif_private_key in wif_private_keys_to_import:
                    print(f'The WIF-format private key is: {wif_private_key}')
                    output_file.write(f"{wif_private_key}\n")
            except Exception as e:
                print(f'Error trying to write to file {output_file_path}: {e}')
                sys.exit(1)
    
    # try:
    #     remove_wif_duplicates(output_file_path)
    # except Exception as e:
    #     print(f'Error removing duplicates from {output_file_path}: {e}')
    #     sys.exit(1)

if __name__ == "__main__":
    main()
