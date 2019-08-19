# secretsanta
A python package to draw a constrained secret santa and send emails to participants.

This package takes into input a mailing list of participants, a constrain list and calculate all draw possible beforre selecting randomly one draw and sending to participants an email telling them who they have to buy a gift for.

This includes:
* one way constrains (i.e. telling bob can't offer to kevin, but kevin can offer to bob).
* two way constrains
* group constrains (all person in group can't offer to each other)
* save and open to a file a secret santa result
* use a past secret santa result as a constrain file for a next one (so that participants don't have to offer to the same person twice in a row for example). 
* send emails with personnal result to all participants using smtp protocol.

Tested only in python 3.

## Usage
While in the package folder in a terminal window or cmd.exe, launch the command:

`python -m secretsanta -i <input_file> -o <output_file>`

### Options:
* `-h`: diplay help
* `-m <smtp_config_file>`: ask to send emails to participants
* `-i <input_file>`: provide input file containing people list with emails and constrains 
* `-o <output_file>`: ask for output to be saved in output file.
* `-s <saved_file>`: don't launch secret santa drawing but use a saved file instead. Can be used in combinaison with -m and an input file for launching emails using a past result.
* `-p <saved_file>`: use a past saved file as an added constrain list.
* `--iteration <iteration number>` : set the maximum iteration number for path finding. Default is 500.

### SMTP config file syntax:
```
[email parameters]
from address = papanoel@polenord.org
subject = Secret Santa 
host = smtp.gmail.com
port number = 587 
login = example_login@gmail.com
template file path = email_template/email_template.txt 

[optionnal]
password = 
```

Email template file contains the text of the message. This text must contain:
* `${PERSON_NAME}` that will be replaced during the script run by the name of the person to offer a gift.
* `${GIFT_RECIPIENT_NAME}` that will be replace during the script run by the name of the person to received a gift.

The script is using smtp for sending email. It may require some config on your email account. For example, if you are using gmail, your account must allow connection from "less secured app".


### Input file syntax:
* Adding new participant (email is not mandatory if not sending emails):
`toto: toto@email.fr`

* Adding one way constrain (toto can't offer to bob):
`toto > bob`

* Adding two way constrain:
`toto <> bob`

* Adding group constrain (all people in group can't offer to each other):
`[toto, titi, tata]`

* Example of input file:
```
toto: toto@gg.fr
bob: bob@bobby.org
tata: tata_ta@yahii.com
bulle: bulle@air-light.be
tony: tony@morleaux.com

toto <> tata
bulle > toto
bob > bulle
tony <> bulle

[tata, bob, tony]
```
