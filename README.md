# grandshakeToken
Grandshake Token Skills Project with Team APEX

# Project Version-1.0.0
## Date Edited -- 16 June 2022

# Prerequisite
- AWS Amazon EC2 Instance is running with Linux
- The Instance need to be running with super-user access or root

# Install library and dependencies
- update the EC2 instance if required `sudo yum update`
- install 'Expect' library using `sudo yum install expect`

# Dependency Packages for extractor script and importer feature. -NN
- It is crucial that you first download these libraries, You should be able to download all these libraries on your server, you need to install the libraries in order to make the extractor/importer stuff work.
- Usually python3 should comes preinstalled on your Unix server, for the other packages something like this should work (e.g. sudo apt install python3-pip)
    - Python3 
    - pip3
    - gspread 
    - oauthent

# Installing and running the Algorand Server (process takes up to ~20-50 minutes)
To have a better understanding of how to run a node, click the link and go to 'Installation with updater script' [Algorand - Install Node](https://developer.algorand.org/docs/run-a-node/setup/install/#installation-with-the-updater-script)
follow the steps down below to install and run the node for Algorand
### The Server connection to Algorand can be check when the fast catchup has been done and using `goal node status -d genesisfiles/testnet` and see the `Sync Time` is 0.0

## For Mac
### Verified on OSX v10.13.4 (High Sierra) and 10.15.7 (Catalina).
- Create a folder to hold the install package and files.
1. `mkdir ~/node`
2. `cd ~/node`

- Download the updater script.
3. `curl https://raw.githubusercontent.com/algorand/go-algorand-doc/master/downloads/installers/update.sh -O`

- Ensure that your system knows it's an executable file.
4. `chmod 544 update.sh`

- Run the installer from within your node directory.
5. `./update.sh -i -c stable -p ~/node -d ~/node/data -n`

## For Linux
### Nodes have been verified on Ubuntu, CentOS, Fedora, openSUSE Leap, Manjaro, Mageia, Alpine, and Solus. Other modern distros should work as well.
- Create a temporary folder to hold the install package and files.
1. `mkdir ~/node`
2. `cd ~/node`

- Download the updater script.
3. `wget https://raw.githubusercontent.com/algorand/go-algorand-doc/master/downloads/installers/update.sh`

- Ensure that your system knows it's an executable file.
4. `chmod 544 update.sh`

- Run the installer from within your node directory.
5. `./update.sh -i -c stable -p ~/node -d ~/node/data -n`

When the installer runs, it will pull down the latest update package from S3 and install it. The -n option above tells the installer to not auto-start the node. If the installation succeeds the node will need to be started manually described later in this [Guide](https://developer.algorand.org/docs/run-a-node/setup/install/#start-node)

Add the following exports to shell config files. Hereafter, goal will default to using `$ALGORAND_DATA` as the data directory, removing the need to specify `-d ~/node/data` in every command.
1. type `vi .bashrc`, then put these 2 lines of codes inside, then save
- `export ALGORAND_DATA="$HOME/node/data"`
- `export PATH="$HOME/node:$PATH"`

## Start Node
depending on the server that will be connected, if the server is mainnet, then no need to specify the server, but if it is testnet or betanet, we have to specify the server by redirect it to the folder (the command down below is for testnet server) (if running to mainnet, then delete '-d genesisfiles/testnet' from the code --- The connection to mainnet will take longer to setup)
### this is not a steps, but command to start, or stop the server
- the server needs to be started manually by typing
1. `goal node start -d genesisfiles/testnet` if the current directory is in node folder

- This will start the node and it can be verified by running:
2. `pgrep algod`

- This will check the status server to Algorand by running:
3. `goal node status -d genesisfiles/testnet`

- The node can be manually stopped by running:
4. `goal node stop -d genesisfiles/testnet`

## Sync node with Network [Sync Node with Network](https://developer.algorand.org/docs/run-a-node/setup/install/#sync-node-with-network)
When a node first starts, it will need to sync with the network. This process can take a while as the node is loading up the current ledger and catching up to the rest of the network. See the section below a Fast Catchup option. The status can be checked by running the following goal command:
```
goal node status
```

The goal node status command will return information about the node and what block number it is currently processing. When the node is caught up with the rest of the network, the "Sync Time" will be 0.0 as in the example response below (if on MainNet, some details will be different).
```
Last committed block: 125064
Time since last block: 3.1s
Sync Time: 0.0s
Last consensus protocol: https://github.com/algorandfoundation/specs/tree/5615adc36bad610c7f165fa2967f4ecfa75125f0
Next consensus protocol: https://github.com/algorandfoundation/specs/tree/5615adc36bad610c7f165fa2967f4ecfa75125f0
Round for next consensus protocol: 125065
Next consensus protocol supported: true
Genesis ID: testnet-v1.0
Genesis hash: SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=
```

## Sync Node Network using Fast Catchup [Sync Node Network using Fast Catchup](https://developer.algorand.org/docs/run-a-node/setup/install/#sync-node-network-using-fast-catchup)
Fast Catchup is a new feature and will rapidly update a node using catchpoint snapshots. A new command on goal node is now available for catchup. The entire process should sync a node in minutes rather than hours or days. As an example, the results for a BetaNet fast catchup, at the time of writing this, was a couple minutes to get to the sync point and a few more minutes to sync the remaining blocks since the snapshot. The total blocks synced was around 4.2 million blocks and it finished syncing in under 6 minutes. Actual sync times may vary depending on the number of accounts, number of blocks and the network. Here are the links to get the most recent catchup point snapshot per network. The results include a round to catchup to and the provided catchpoint. Paste into the `goal node catchup` command.
- BetaNet [https://algorand-catchpoints.s3.us-east-2.amazonaws.com/channel/betanet/latest.catchpoint](https://algorand-catchpoints.s3.us-east-2.amazonaws.com/channel/betanet/latest.catchpoint)
- TestNet [https://algorand-catchpoints.s3.us-east-2.amazonaws.com/channel/testnet/latest.catchpoint](https://algorand-catchpoints.s3.us-east-2.amazonaws.com/channel/testnet/latest.catchpoint)
- MainNet [https://algorand-catchpoints.s3.us-east-2.amazonaws.com/channel/mainnet/latest.catchpoint](https://algorand-catchpoints.s3.us-east-2.amazonaws.com/channel/mainnet/latest.catchpoint)
The results will look similar to this: `4420000#Q7T2RRTDIRTYESIXKAAFJYFQWG4A3WRA3JIUZVCJ3F4AQ2G2HZRA`

Steps:
1. Start the node, if not started already, and run a status.
`goal node start -d genesisfiles/testnet`
`goal node status -d genesisfiles/testnet`

Results should look something like this...
```
Last committed block: 308
Time since last block: 0.0s
Sync Time: 6.5s
Last consensus protocol: https://github.com/algorand/spec/tree/a26ed78ed8f834e2b9ccb6eb7d3ee9f629a6e622
Next consensus protocol: https://github.com/algorand/spec/tree/a26ed78ed8f834e2b9ccb6eb7d3ee9f629a6e622
Round for next consensus protocol: 309
Next consensus protocol supported: true
Last Catchpoint:
Genesis ID: betanet-v1.0
Genesis hash: mFgazF+2uRS1tMiL9dsj01hJGySEmPN28B/TjjvpVW0=
```

2. Use the sync point captured above and paste into the catchup option
`goal node catchup 4420000#Q7T2RRTDIRTYESIXKAAFJYFQWG4A3WRA3JIUZVCJ3F4AQ2G2HZRA -d genesisfiles/testnet`

3. Run another status and results should look something like this showing a Catchpoint status: `goal node status`
Results should show 5 Catchpoint status lines for Catchpoint, total accounts, accounts processed, total blocks , downloaded blocks.
```
Last committed block: 4453
Sync Time: 15.8s
Catchpoint: 4420000#Q7T2RRTDIRTYESIXKAAFJYFQWG4A3WRA3JIUZVCJ3F4AQ2G2HZRA
Catchpoint total accounts: 1146
Catchpoint accounts processed: 1146
Catchpoint total blocks: 1000
Catchpoint downloaded blocks: 81
Genesis ID: betanet-v1.0
Genesis hash: mFgazF+2uRS1tMiL9dsj01hJGySEmPN28B/TjjvpVW0=
```

4. A new option can facilitate a status watch, -w which takes a parameter of time, in milliseconds, between two successive status updates. This will eliminate the need to repeatedly issue a status manually. Press ^c to exit the watch.
`goal node status -w 1000`

5. Notice that the 5 Catchpoint status lines will disappear when completed, and then only a few more minutes are needed to sync from that point to the current block. **Once there is a Sync Time of 0, the node is synced and if fully usable. **
```
Last committed block: 4431453
Time since last block: 3.9s
Sync Time: 0.0s
Last consensus protocol: https://github.com/algorandfoundation/specs/tree/e5f565421d720c6f75cdd186f7098495caf9101f
Next consensus protocol: https://github.com/algorandfoundation/specs/tree/e5f565421d720c6f75cdd186f7098495caf9101f
Round for next consensus protocol: 4431454
Next consensus protocol supported: true
Last Catchpoint: 4430000#UAQPNY32LP3K5ARGFUQEFTBGELI5ZAQOMBGE7YL5ZFXL2MXWTO2A
Genesis ID: betanet-v1.0
Genesis hash: mFgazF+2uRS1tMiL9dsj01hJGySEmPN28B/TjjvpVW0=
```

## Troubleshooting for fast catchup [Troubleshooting for fast catchup](https://developer.algorand.org/docs/run-a-node/setup/install/#troubleshooting-for-fast-catchup)
If fast catchup fails, check the following:
- the node is not archival (and is not a relay).
- the software is up-to-date: `goal version -v` should report the latest Algorand version in (https://github.com/algorand/go-algorand/releases), ignoring the `Algorand BetaNet` releases.
- the catch point matches the network used by the node and reported as `Genesis ID` by `goal node status`.
- the hardware requirements above are satisfied, in particular a not-too-slow SSD is used.
- the computer does not run out of memory.

## Updating Node [Updating Node](https://developer.algorand.org/docs/run-a-node/setup/install/#updating-node)
The RPM or Debian packages are updated automatically. For other installs, check for and install the latest updates by running `./update.sh -d ~/node/data` at any time from within your node directory. Note that the `-d` argument has to be specified when updating. It will query S3 for available builds and see if there are newer builds than the currently installed version. To force an update, run `./update.sh -i -c stable -d ~/node/data`.

If there is a newer version, it will be downloaded and unpacked. The node will shutdown, the binaries and data files will be archived, and the new binaries will be installed. If any part of the process fails, the node will restore the previous version (bin and data) and restart the node. If it succeeds, the new version is started. The automatic start can be disabled by adding the `-n` option.

Setting up a schedule to automatically check for and install updates can be done with CRON.
```
crontab -e
```

Add a line that looks like this (run update.sh every hour, on the half-hour, of every day), where ‘user’ is the name of the account used to install / run the node:
```
30 * * * * /home/user/node/update.sh -d /home/user/node/data >/home/user/node/update.log 2>&1
```

# Creating a wallet and account (This steps only needs to be done once in the beginning of the process)
using the CLI to interacting with Algorand from this link [Goal](https://developer.algorand.org/docs/clis/goal/goal/#goal)
### REMEMBER TO SPECIFY THE SERVER USING `-d` IF WE ARE RUNNING TESTNET OR BETANET

## Creating a Wallet
1. To create a wallet type the following code:
```
goal wallet new [wallet name] [flags]
```
for an example
```
goal wallet new grandwallet -d genesisfiles/testnet
```
2. then the terminal or system will require to input a password that will be used for the wallet, **If the password is different, the password in the _expectFile.exp_ **

## Creating two accounts (Primary Account and Secondary account)
1. To create an account, type the following code:
```
goal account new [flags]
```
for an example **the name of the following account is primaryAccount, to create the second account, change the _primaryAccount_ to _secondaryAccount_ or change into any names you like**
```
goal account new primaryAccount -d genesisfiles/testnet
```
2. then the terminal or system will require the password that was being created from wallet creation just now

3. to create the second account, just redo the steps all over again with different name

# Creating the Grandshake Token Skills or creating an asset
**BEFORE CREATING AN ASSET , THE TWO ACCOUNTS HAS TO BE FUNDED BEFORE HAND, IF IT IS USING TESTNET, GO TO TESTNET FAUCET [Algorand Testnet Dispenser](https://dispenser.testnet.aws.algodev.network/), IF USING THE MAINNET, THEN NEED TO BUY ALGO BALANCE FROM THE SERVER**

- To create the Grandshake Token skills, type this: (the total down below is the 1 Billion)
```
goal asset create --creator <primary account address that just being created> --total 1000000000 --unitname <unit-name> --assetid <asset-ID> --decimals 0   -d genesisfiles/testnet
```

# Opt-in the secondary account to the asset using the [MyAlgo Wallet](https://wallet.myalgo.com/home)
1. From the home page, click Access now button
2. If this is the first time accessing the MyAlgo Wallet, then it will prompt to create password, enter the password
3. Go back to the EC2 instance terminal and type `goal account list -d genesisfiles/testnet` then enter the password
4. Record the two address from the account and the asset id
5. Then type `goal account export -a <account address> -d genesisfiles/testnet` **DO THIS FOR BOTH ACCOUNTS**
6. The terminal will give 25 mnemonic words, Record the mneomonic words **DO NOT SHARE THE MNEMONIC WORDS TO ANYONE AND KEEP IT AS SAFE AS POSSIBLE, DO NOT LOSE IT**
7. Go back to MyAlgo Wallet website, then click add account button
8. Click 'Import Phrase'
9. Set the account name
10. Enter the 25 Mnemonic Words
11. Enter the password
12. Do Steps 7-11 for the secondary account as well
13. Then click the secondary account from the website
14. Click on "Add Asset"
15. Then find the Grandshake asset using the Asset ID or the Asset Name
16. Click on the asset
17. then enter the Password
18. It will takes few seconds
19. Go back to the EC2 Instance then type `goal account list -d genesisfiles/testnet`
20. The secondary account balance will have 0.001 algo balance less then the previous balance

# AFTER THE SERVER RUNNING AND SYNCED, THE WALLET AND ACCOUNTS ARE CREATED, THE ASSET HAS BEEN CREATED AND THE SECONDARY ACCOUNT HAS BEEN OPTED-IN TO THE ASSET, THE SYSTEM HAS BEEN COMPLETE TO RUN THE CODE/SOLUTION FROM THE APEX TEAM FROM THE GITHUB REPO

# Code/Solution
## ALL THE CODE THAT NEEDS TO BE CHANGED OR ANYTHING NEEDS TO BE CHANGE
- **The folder name and file name has to be exactly the same as the repo, if there are any changes to the file name or folder name, some changes in the code needs to be done**
- **The Address for the primary Account (the creator of the asset) and the Secondary Account needs to be inputed in the _makeTransaction.sh_ file from the github**
- **the wallet name and the wallet password need to be inputted in the _expectFile.exp_ file, example `<wallet name>` change into `grandwallet`**

## Process Automation
To process the code, just type the follwing code:
```
nohup bash fireProcess.sh
```
**the current _fireProcess.sh_ or the process will be running every 10 minutes to check if there are any transactions needed to be done. this can be done by changing the sleep timer in _fireProcess.sh_ file**
**Record the _JOB PID_ for any future command if needed

# A Guide to The Extractor Script - NN
## In this section, I discuss and elaborate on 1) what is the extractor script 2) what does it do 3) How can it be set up

Before we go any further, Please note there are some dependencies which need to be taken care off. So please make sure you cover that before you proceed with anything else in this section

## What is the Extractor Script and what is it programmed to do?
- Short Answer? The Extractor Script just extracts the values from Grandshake's google sheet DB and creates transaction assignment request files for the module mentioned above to fire into the Algorand Network. It uses the google sheets API mechanism to reach the sheet.
- Long Answer? Our solution initiates when it finds some records from Grandshake's google sheet DB worth creating a transaction assignment request for. What does that mean? It means the extractor script will run every 30 mins(this value can be modified - look below for the automation feature for this script) but when the extractor script runs it makes a check for each record in that google sheet and does a comparison of the time for that value from the datetime field for every record with the last time this script was run. This comparison then has two outcomes, Outcome 1 - The script finds records worth extracting(when the datetime comparison proves that the record's datetime is greater than the datetime for when the script last ran). Outcome 2 - It finds no records worth extracting and does nothing (when the datetime of the records is less than the datetime of when the script last ran).

- What if the extractor actually finds records worth extracting?
- In that case, the extractor will just select that rows enrollmentID and combine that piece of information with the token value that needs to be assigned for that enrollmentID(e.g. give this enrollmentID a token worth 5 as its value) it then combines this with another random job id and then these threee elements are added to a file which becomes the transaction assignment request file(txn_req_job_4134.txt).

- The variable Output inside that txn_req_job_{job_id}.txt file should something like this -> "enrollmentId-tokenValue-randomJobID"
- This output then serves to be read by the module explained before this extractor scripts section.

## How can it be set up?
Just put the extractor script in the same directory as the aforementioned makeTransaction.sh script. Make sure the timekeeper.txt and the "test-project-1-349705-bf9bfec03f61.json" file exists in the same folder as this script.

what is this timekeeper.txt file?
This basically is how the script keeps track of when it was last run. Values from this are lifted when the script wants to make datetime comparisons.(MM-DD-YYYY HH:MM:SS). Also in general please note any datetime activity associated with importer/extractor feature exists in this format(MM-DD-YYYY HH:MM:SS)

What is this test-project-1-349705-bf9bfec03f61.json file?
Consider this file as the reason why the extractor script is able to read information from the Grandshake Google Sheet. If you want to create your own, you could just refer this - https://cloud.google.com/iam/docs/creating-managing-service-accounts

So, overall just make sure the extractor script, timekeeper.txt and the json file co-exist within the same folder as the makeTransaction.sh file. 

## How to automate this script
In the cron file, just add the below entry, Also if you aren't sure about what cron is, its worth taking a look at this(https://ostechnix.com/a-beginners-guide-to-cron-jobs/) before you do anything below 

## Process Automation
```
*/5 * * * * python3 "folder where the extractor script exists minus these quotes thingy"
```

example - 
```
*/5 * * * * python3 /bin/essentials/extractor_main/extractor_main_v2.py
```

So now, this should enable you to 1) Automate the extractor script 2) Set it up on your personalised server 3) Understand what it does
For more hints, Feel free to refer the script as it should be easy enough to modify as per your requirements or needs. Thanks!

#### This concludes the section on the extractor script.


# A guide to an importer script

## This section will discuss about:
### 1) What is the extractor script?
### 2) Explaining the script algorithm.
### 3) What are the assumptions and limitations?

#### What is the extractor script:-
The extractor script is a python script which basically extracts all the relevant transaction details corresponding to each transaction ID.
It basically interacts with the algorand explorer API to fetch all the transaction information and generates it in a
JSON style. Further the script displays the transaction ID and correseponding token amount against each enrollment 
ID of a user completing the course. In a nutshell, the script takes all the transaction ID from a text file generated by
the previous script/module as input and correspondingly extracts all releavnt transaction data which is further displayed 
in the google sheet. 

#### Explaining the script algorithm:-
* All the required libraries are imported at the top.
* The first chuck of the script basically handles the access to the Google sheet.
* Then it point towards the worksheet where all the transaction details are to be displayed.
* The next chunk of the script performs each transaction's information retrieval from the Algo explorer. It first reads all the transaction ID's from the transactionFile.txt and store it in a transaction list. Now for every transaction ID in the list, it interacts with the Algo explorer API to fetch all the transaction details in a json format.
* Further 5 relevant transaction data are filtered from json response and stored in variables named tx_amount, asset_id, rx_id, snd_id and note (containing Enrollment_ID, amount to transfer and Unique_ID. It was found that the Note variable was in base64 format and so it is then converted into ASCII format to read and extract the Enrollment_ID, Unique_ID and amount to transfer variables.
* Once all the relevant variables i.e, relevant transaction data are extracted, it is then stored in a dictionary format (Tx_dict).
* The last chunk of the code basically extracts transaction ID, Enrollment ID and token amount from the Tx_dict and displays the transaction ID along with the token amount for the corresponding enrollment ID in the Google sheet.

#### What are the assumptions and limitations?
* The script assumes input as a list of transaction ID's in text format.
* The script basically produces all the transaction details based on the Algo explorer API schema.
* It is unable to extract the date and time of each transaction.
* The script is accessing the same Google sheet API to display the transaction ID and correponding token amount.


