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
        print('Private key is: ' + private_key)
        # Add the private key to the array of WIF-format keys
        private_keys.append(private_key)
    
    # Return an array of strings of WIF-format private keys
    return private_keys

def remove_wif_duplicates(file_path):
    output_path = file_path

    lines = open(file_path, 'r').readlines()
    unique_lines = set(line.strip() for line in lines)

    with open(output_path, 'w') as file:
        for line in sorted(unique_lines):
            file.write(f"{line}\n")

def main():
    output_file_path='wif_private_keys'

    # Define your BIP39 seed phrase and passphrase
    seed_phrase = 'program traffic coil weather sleep black push retreat recall oil chief cement ability tonight must give margin tragic risk edit page impose assist dust'
    passphrase = 'apple'

    # Derive the private key
    wif_private_keys_to_import = derive_private_keys(seed_phrase, passphrase)

    # Print the private keys
    print("The BIP32 private keys are:")
    for wif_private_key in wif_private_keys_to_import:
        print('The BIP32 private key is:   ' + wif_private_key)
        open(output_file_path,'a+').write(f"{wif_private_key}\n")

    remove_wif_duplicates(output_file_path)

if __name__ == "__main__":
    main()
