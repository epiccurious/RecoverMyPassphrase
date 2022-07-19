from mnemonic import Mnemonic

mnemo = Mnemonic("english")

testSeedWords = "program traffic coil weather sleep black push retreat recall oil chief cement ability tonight must give margin tragic risk edit page impose assist dust"
# https://iancoleman.io/bip39/#english

seed1 = mnemo.to_seed(testSeedWords,"")

hd_master_key1 = to_hd_master_key(seed1)

print("The hd master key is " + hd_master_key1)
