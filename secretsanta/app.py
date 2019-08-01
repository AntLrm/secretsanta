import re
import getopt
import sys

from secretsanta.secretdraw import secretdraw

class app():
    """
    Class to parse command arguments, read input files, and launch the roll.
    """

    def __init__(self):
        self.send_mail = False
        self.saved_roll_provided = False
        self.past_file_provided = False
        self.input_file_provided = False
        self.output_file_provided = False
        self.past_file = ""
        self.saved_roll_file = ""
                
    def run(self, argv):
        """
        Parse arguments, and run a roll and write emails and files depending on command arguments.
        """
        self.parse_arguments(argv)
        
        if self.is_command_ok():

            self.secretdraw = secretdraw()
            
            if self.saved_roll_provided:
                self.secretdraw.set_roll_from_file(self.open_file(self.saved_roll_file))
                print('Saved roll in ' + self.saved_roll_file + ' set in a new secret santa!')        
            else:
                self.config_secretdraw()
                print('Secret santa set, launching roll...')
                self.secretdraw.mroll()
                print('Roll done.')
                if self.output_file_provided :
                    self.secretdraw.write_on_file(self.output_file)
                    print('Saving roll to ' + self.output_file)
            
            if self.send_mail:
                print('Sending to mailing list...')
                self.secretdraw.send()
                print('All emails sent.')
                

        else:
            self.print_help()
            sys.exit()
    
    def config_secretdraw(self):
        """
        Set secretdraw object attributes for roll according to inputs.
        """
        if self.input_file_provided:
            input_reader = self.open_file(self.input_file)

            for row in input_reader:
                people_read = self.get_people_inrow(row)
                if people_read != [] :
                    self.secretdraw.addpeople(people_read)
            
            input_reader.seek(0)
            for row in input_reader:
                constrain_read_list = self.get_constrain_list_inrow(row)
                if constrain_read_list != [] :
                    self.secretdraw.addconstrains(constrain_read_list)

        if self.past_file_provided:
            past_reader = self.open_file(self.past_file)

            for row in past_reader :
                past_constrain_read_list = self.get_constrain_list_inrow(row)
                if past_constrain_read_list != [] :
                    self.secretdraw.addconstrains(past_constrain_read_list)

        
    def parse_arguments(self, argv):
        try:
            args = argv
            opts, args = getopt.getopt(args,"hms:p:i:o:",["saved=", "past=", "input=", "output="])
        except getopt.GetoptError:
            self.print_help()
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                self.print_help()
                sys.exit()
            elif opt == '-m':
                self.send_mail = True
            elif opt in ("-s", "--saved"):
                self.saved_roll_provided = True
                self.saved_roll_file = arg
            elif opt in ("-p", "--past"):
                self.past_file_provided = True
                self.past_file = arg
            elif opt in ("-i", "--input"):
                self.input_file_provided = True
                self.input_file = arg
            elif opt in ("-o", "--output"):
                self.output_file_provided = True
                self.output_file = arg
    
    def is_command_ok(self):
        """
        Check if there is necessary inputs in command.
        """
        if self.saved_roll_provided and (input_file_provided or self.past_file_provided):
            print('For info, a saved roll file has been provided: constrains in input file and past constrain file will be ignored.')

        if not(self.input_file_provided) and (self.send_mail):
            print('Input file with emails is mandatory if emails are to be sent!')
            return False

        if not(self.output_file_provided) and not(self.send_mail):
            print('Warning, no output file, nor send email request has been provided, the result of the roll will not be stored anywhere!')

        return True
                

    def get_people_inrow(self, row):
        """
        Return people in the read row if any
        """
        people_search = re.search(".+?(?=:).*", row) 
        if people_search != None :
            name = re.search(".+?(?=:)", row).group().replace(" ", "")
            email = re.search("(?<=:).*", row).group().replace(" ", "")
            return [name, email]

        else:
            return [] 


    def get_constrain_list_inrow(self, row):
        """
        Return constrain in the read row if any
        """
        #constrain_search: search for the strings of type "something > something"
        constrain_search = re.search(".+>.+", row)
        if constrain_search != None :
            #get the second name (string after ">") 
            name2 = re.search("(?<=>).+", row).group().replace(" ", "")
            #search for "something <>" for double constrain
            substringsearch = re.search(".+<>", constrain_search.group())
            if substringsearch != None :
                #first name is before the "<"
                name1 = re.search(".+?(?=<)", substringsearch.string).group().replace(" ", "")
                return [[name1, name2], [name2, name1]]
            else:
                #first name is before the ">"
                name1 = re.search(".+?(?=>)", row).group().replace(" ", "")
                return [[name1, name2]]

        else:
            return []
       
    
    def print_help(self):
        print('python -m secretsanta -m -p <previous roll> -i <input file> -o <output file>')
        print('-m: ask the script to send emails to the secret santa participants')
        print('-f <roll file>: run the command without rolling a new secret santa, but using roll from a file' )
        print('-p <roll file>: previous roll to be considered as constrain')
        print('-i <input filel>: people list file with emails, and constrains')
        print('-o <output file>: roll output file')
   
    def open_file(self, file_path):
        try:
            return open(file_path, "r")
        except IOError:
            print('Error trying to open: ' + file_path + '. Please check existence.')
            sys.exit()
        
    
