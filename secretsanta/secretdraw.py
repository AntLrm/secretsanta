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
        if len(self.roll) > 1:
            previous_name = self.roll[0]
            for name in self.roll[1:]:
                file_writer.write(previous_name + ">" + name + '\n')
                previous_name = name
            file_writer.write(previous_name + ">" + self.roll[0])
        else:
            print('Not enough people in your secret santa, sorry...')
            sys.exit()
                
    #TODO method to send results to emails
    def send(self):
        """
        send results to emails.
        """
        pass

    #TODO method to set roll from file
    def set_roll_from_file(self, roll_file_reader):
        """
        set self.roll from a roll file.
        """
        pass

    def mroll(self):
        """
        Launch a draw, and select randomly a solution in solution list.
        """
        self.roll = self.getrandom_path()

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
