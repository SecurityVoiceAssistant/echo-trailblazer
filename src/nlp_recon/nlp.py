import torch
import torchvision
import subprocess
import easygui
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pyExploitDb import PyExploitDb

from transformers import RobertaTokenizer, RobertaTokenizerFast

tokenizer = RobertaTokenizerFast.from_pretrained("ehsanaghaei/SecureBERT")

model = torch.load('models/model.pt')
model.to('cuda:0')

def prepare_features(
  seq_1, max_seq_length = 300, zero_pad = False,
  include_CLS_token = True, include_SEP_token = True):
    ## Tokenzine Input
    tokens_a = tokenizer.tokenize(seq_1)

    ## Truncate
    if len(tokens_a) > max_seq_length - 2:
        tokens_a = tokens_a[0:(max_seq_length - 2)]
    ## Initialize Tokens
    tokens = []
    if include_CLS_token:
        tokens.append(tokenizer.cls_token)
    ## Add Tokens and separators
    for token in tokens_a:
        tokens.append(token)

    if include_SEP_token:
        tokens.append(tokenizer.sep_token)

    input_ids = tokenizer.convert_tokens_to_ids(tokens)
    ## Input Mask 
    input_mask = [1] * len(input_ids)
    ## Zero-pad sequence lenght
    if zero_pad:
        while len(input_ids) < max_seq_length:
            input_ids.append(0)
            input_mask.append(0)
    return torch.tensor(input_ids).unsqueeze(0), input_mask

def get_reply(msg):
  model.eval()
  input_msg, _ = prepare_features(msg)
  if torch.cuda.is_available():
    input_msg = input_msg.cuda()
  output = model(input_msg)[0]
  _, pred_label = torch.max(output.data, 1)
  result = pred_label.item()
  return result

def runShodanIp(ip):
    command = f"shodan host '{ip}' "
    return command
import subprocess

while(True):
    result = get_reply(input("what do you want to do? \n"))

    if(result==1):

        print("\nThe tools that are identified to help you are theHarvester and Shodan, we will guide u on a step by step to use them")

        print("Available parameters of search")
        print("1. Domain")
        print("2. IP address")

        searchW = True
        while(searchW):
            search = input()
            if(search=="1" or search=="2"):

                searchW = False
            else:
                print("Enter valid option")
        if(search =="1"):
            # Prompting user for essential parameters
            #target = input("Enter the target domain, (remember, if u want to search for emails associated is recomended to add the API key of hunter on api-keys.yml on theHarvester folder and use hunter source or all ):\n  \n")
            rTarget = True
            while(rTarget):
                target = input("Enter the target domain(www.example.com): ")
                target = target.lower()
                if(target.startswith("www.")):
                    rTarget = False
                else:
                    print("Enter valid domain")

            data_source = "all"
            #output_file = input("Enter the output file name: ")


            # Creating a menu for additional options

            extra_params = ""
            rOption = True
            shodanUse = False
            listOptions = []
            while(rOption):
                print("\nAdditional Options:")
                print("1. Enable Shodan(Must have shodan api added on api-keys.yml of theHarvester)")
                print("2. Enable DNS")
                print("3. Check for takeovers")
                print("4. No additional options")
                option = input("Choose an option (1, 2, 3 or 4): \n \n")
                # Processing the chosen option
                if option == "1":
                    shodanUse = True
                    listOptions.append(option)
                if option == "2":
                    dns_server = input("Enter the DNS server address: ")
                    extra_params += "-e {dns_server} "
                    listOptions.append(option)
                if option == "3":
                    extra_params += "-r  " 
                    listOptions.append(option)
                if option == "4":
                    extra_param=""
                    rOption = False
                    listOptions.append(option)
                elif option != '1' or option != '2' or option != '3' or option != '4':
                    print("Enter valid option")

                print("Added options: " + str(','.join(listOptions)))

            print("Searching...")
            # Launching theHarvester with the provided parameters
            #command = f"theHarvester -d {target} -b {data_source} -f {output_file}"
            command = f"theHarvester -d '{target}' -b {data_source} {extra_params} "
            #command = f"theHarvester -d {target} -b {data_source}"
            output = subprocess.check_output(command, shell=True).decode()

            if(shodanUse):
                command = f"shodan domain '{target}' "
                output += subprocess.check_output(command, shell=True).decode()
        else:
            ip = input("Enter the IP: ")
            command = runShodanIp(ip)
            output = subprocess.check_output(command, shell=True).decode()
        # Displaying the results
        print("\nResults:\n")
        print(output)
        print("thanks for everything, it was pleasure to help you")

    elif(result==0):

        easygui.msgbox("The tool identified to help you is Exiftool, please choose a file to analyze", title="simple gui")
        # Open file picker dialog
        imageR = True
        while(imageR):
            Tk().withdraw()
            image_path = askopenfilename(title="Select an image file")
            if(image_path == ""):
                raise SystemExit("Stop right there!")
            else:
                imageR = False


        print("\n Select mode for metadata extracion")
        print("1. Save visualization on .html")
        print("2. Save visualization on .csv")
        print("3. Save visualization on .txt")
        print("Other key. Don't save, just show it on screen")

        option = input("Choose an option (1, 2, 3 or Other): \n \n")

        extra_params = ""

        # Processing the chosen option
        if option == "1":

            extra_params += '-h > '
            output_file = input("Enter the output file name: ")
            extra_params += output_file+'.html'


        elif option == "2":

            extra_params += '-T > '
            output_file = input("Enter the output file name: ")
            extra_params += output_file+'.csv'

        elif option == "3":

            extra_params += '-t > '
            output_file = input("Enter the output file name: ")
            extra_params += output_file+'.txt'


        else:
            print('Visualization will be shown on screen')

        # Step 1: Extracting metadata using exiftool
        extract_command = f"exiftool {image_path} {extra_params}"
        metadata_output = subprocess.check_output(extract_command, shell=True).decode()

        # Displaying the extracted metadata
        print("Extracted Metadata:")
        print(metadata_output)

        # Step 2: Modifying a specific metadata tag

        modify_choose= input ("Do you want to modify a metadata tag o a new file? please answer 'yes' or 'no' /n ")

        if 'yes' in modify_choose:

            tag_name = input("Enter the name of the metadata tag to modify: ")
            new_value = input("Enter the new value for the metadata tag: ")

            modify_command = f'exiftool -{tag_name}="{new_value}" {image_path}'
            subprocess.run(modify_command, shell=True)

            # Step 3: Verifying the modified metadata
            verification_command = f"exiftool {image_path}"
            verified_metadata_output = subprocess.check_output(verification_command, shell=True).decode()

            # Displaying the verified metadata
            print("\nVerified Metadata:")
            print(verified_metadata_output)

        else:

            print("thanks for everything, it was pleasure to help you")
    elif(result==2):
        print("The tool identified to help you is ExploitDB")
        exploitDB = True
        while(exploitDB):
            print("Especify a function (1, 2, 3)")
            print("1. Search a exploit")
            print("2. Donwload a exploit")
            print("3. Search CVE")
            
            option= input()
            if(option == "1"):
                exploit = input("Enter name of exploit ")
                command_exploit = f"searchsploit {exploit}"
                output_exploit = subprocess.check_output(command_exploit, shell=True).decode()
                print(output_exploit)
            elif(option == "2"):
                exploit = input("Enter name of exploit ")
                command_exploit = f"searchsploit -p {exploit}"
                output_exploit = subprocess.check_output(command_exploit, shell=True).decode()
                print(output_exploit)
            elif(option == "3"):
                searched = input("Enter name number of CVE. (Example: 2018-14592) ")
                pEdb = PyExploitDb()
                pEdb.debug = False
                pEdb.openFile()
                results = pEdb.searchCve("CVE-" + str(searched))  
                print(results)  
            else:
                print("Enter valid option")

            exploitT = input("Do you want use the tool again? ('yes' or 'no'): ")
            if(exploitT != "yes"):
                exploitDB = False

