import time
import pdb
import sys

from secretsanta.threads import tree_pathfinding
from secretsanta.threads import random_pathfinding

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

    def mroll(self):
        """
        Launch multiple draw using 2 different algorithms, one random (effective for low constrained inputs),
        one tree explore (effective for highly constrained input) and get the result of whatever algo is the fastest.
        """
        random_thread = random_pathfinding(self)
        tree_thread = tree_pathfinding(self)
        random_thread.start()
        tree_thread.start()
        while self.roll == []:
            print('Thread running...')
            if tree_thread.get_roll_result() != []:
                self.roll = tree_thread.get_roll_result()
                print('tree wins')
            elif random_thread.get_roll_result() != []:
                self.roll = random_thread.get_roll_result()
                print('random wins')

        tree_thread.stop()
        random_thread.stop()
        tree_thread.join()
        random_thread.join()    

        print(self.roll)

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
    

