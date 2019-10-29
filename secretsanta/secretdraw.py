import pdb
import sys
import random

class secretdraw():
    """
    Secret draw define an object to roll the secret santa. Storing people, constrains, and constructing gift tree.
    - people : people dict containing names and emails.
    - constrain : constrain dict containing for each name, the list of forbidden people to gift.
    - roll : result of the draw.
    - path_list : list of all possible draw.
    """

    def __init__(self):
        self.people= {}
        self.constrain = {}
        self.roll = []
        self.path_list = []
        self.pathfind_max_iter = 500


    def write_on_file(self, output_file):
        """ 
        write roll result on an output file.
        """
        file_writer = self.open_file_to_write(output_file)
        if len(self.gifts_list) > 1:
            for gift in self.gifts_list:
                file_writer.write(gift[0] + ">" + gift[1] + '\n')
        else:
            print('Not enough people in your secret santa, sorry...')
            sys.exit()
                
    def get_gift_list_from_roll(self):
            previous_name = self.roll[0]
            gifts_list = []
            for name in self.roll[1:]:
                gifts_list.append([previous_name, name])
                previous_name = name
            gifts_list.append([previous_name, self.roll[0]])
            return gifts_list

    def send(self, email_send_obj):
        """
        send results to emails.
        """
        if '' in self.people.values():
            print('All listed in input file need an email address if you wish to send emails.')
            return False
        else:
            email_send_obj.read_template(email_send_obj.template_file)
            email_send_obj.smtp_config()

            if len(self.gifts_list) > 1:
                for gift in self.gifts_list:
                    email_send_obj.send_message(gift[0], gift[1], self.people[gift[0]])
            return True

    def set_giftlist_from_file(self, saved_file_reader):
        """
        set self.gift_list from a previously saved file.
        """
        self.gifts_list = []
        for line in saved_file_reader:
            names_in_line = line.rstrip().split('>')
            self.gifts_list.append(names_in_line)

    def mroll(self):
        """                                     
        Launch a draw, and select randomly a solution in solution list.
        """
        self.roll = self.getrandom_path()
        self.gifts_list = self.get_gift_list_from_roll()

    def getrandom_path(self):
        """
        Search for a path in people list with constrains.
        """
        people_list = list(self.people.keys())
        path = [] 
        iterations = 0
        while len(path) < len(people_list) and iterations < self.pathfind_max_iter :
            iterations += 1
            path = []
            people_not_in_path = people_list[:]
            available_names = people_list[:]
            while len(available_names) > 0:
                next_name = random.choice(available_names)
                path.append(next_name)
                people_not_in_path.remove(next_name)
                available_names = people_not_in_path[:]
                print(available_names)
                for constrain in self.constrain[next_name]:
                    if constrain in available_names:
                        available_names.remove(constrain)

        if iterations == self.pathfind_max_iter :
            print('Max number of iterations reached while searching for a path, your secret santa may be too constrained and may not have a solution.')
            sys.exit()
        else:
            return path

    def addconstrains(self, constrain_list):
        """
        add a constrain to this secretdraw object.
        """
        for constrain in constrain_list:
            if self.checkexistence(constrain[0]) and self.checkexistence(constrain[1]):
                self.constrain[constrain[0]].append(constrain[1])
   
    def addpeople(self, people):
        """
        add a person to this secretdraw object.
        """
        self.people[people[0]] = people[1]
        self.constrain[people[0]] = []

    def checkexistence(self, name):
        """
        Check if name provided in input is existing in this object people list.
        """
        if name in self.people:
            return True
        else:
            print('Warning: ' + name + 'is not in your people input list, please check your input file.')

    def open_file_to_write(self, file_path):
        try:
            return open(file_path, "w+")
        except IOError:
            print('Error trying to open: ' + file_path + '. Please check existence.')
            sys.exit()
