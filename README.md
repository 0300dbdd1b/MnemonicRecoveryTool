# MnemonicRecoveryTool

"The aim of this repo is to create a program that can show you all possibilities for your last word in a mnemonic phrase."

## examples :

here's a mnemonic : toddler pepper buddy gentle crack heart cannon match answer stage shine nominee agree crouch steel cheese mean turtle final person close scorpion latin puzzle

```
python3 mnemonic_gen.py "toddler pepper buddy gentle crack heart cannon match answer stage shine nominee agree crouch steel cheese mean turtle final person close scorpion latin"

Phrase : toddler pepper buddy gentle crack heart cannon match answer stage shine nominee agree crouch steel cheese mean turtle final person close scorpion latin

Lasts words finded :

[0] : book
[1] : couch
[2] : empty
[3] : jacket
[4] : pact
[5] : puzzle
[6] : security
[7] : west
```

here the [5] was the word we searched. <br>
works with any mnemonic phrase (12, 15, 18, 21, 24) <br>


The number of expected words finded is: 2^(-1/3 L + 12) - 1 <br>

where L is the lenght of the complete mnemonic (in our case 24) <br>


(note: this script is shit)

