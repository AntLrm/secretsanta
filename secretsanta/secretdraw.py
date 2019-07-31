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


    #TODO: test this method
    def write_on_file(self, output_file):
        """ 
        write roll result on an output file.
        """
        file_writer = open_file_to_write(ouptut_file)
        if len(self.roll) > 1:
            previous_name = self.roll[0]
            for name in self.roll[1:]:
                file_writer.write(previous_name + ">" + name)
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
        self.compute_path_list()
        print(len(self.path_list))
        self.roll = random.choice(self.path_list)
        print(self.roll)

    def compute_path_list(self):
        """
        Compute list of all possible solutions.
        """
        people_list = list(self.people.keys())
        gift_tree, maxdepth = self.get_tree(people_list[0], people_list[1:])

        if maxdepth == len(people_list):
            self.path_list = gift_tree.get_maxpaths_list_from_tree()
        else:
            print('No solution found. Your secret santa may be too constrained')
            sys.exit

    def get_tree(self, top_node, other_node_list):
        """
        Return a tree of solutions from a top node and a list of people.
        """
        output_tree = tree()
        output_tree.set_mainnode(top_node)
        max_subtree_depth = 0 
        children_list = self.get_children(top_node, other_node_list)

        if len(children_list) == 0 :
            return output_tree, max_subtree_depth + 1
        else :
            for child in children_list :
                reduced_node_list = other_node_list[:]
                reduced_node_list.remove(child)
                subtree, subtree_depth = self.get_tree(child, reduced_node_list)
                output_tree.addsubtree(subtree)
                if subtree_depth > max_subtree_depth:
                    max_subtree_depth = subtree_depth
            return output_tree, max_subtree_depth + 1 
    
    def get_children(self, top_node, candidates):
        """
        Get all possible people to offer a gift.
        """
        children_list = []
        for name in candidates:
            if not (name in self.constrain[top_node]):
                children_list.append(name)
        return children_list


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

    
class tree():
    """
    Tree object.
    - mainnode : top node of the tree
    - subtree_list : list of all tree object that are child of the mainnode.
    """
    def __init__(self):
        self.mainnode = ''
        self.subtree_list = []

    def set_mainnode(self, mainnode_to_set):
        self.mainnode = mainnode_to_set

    def addsubtree(self, subtree_to_add):
        self.subtree_list.append(subtree_to_add)

    def get_maxpaths_list_from_tree(self):
        """
        Return the list of all paths that have the maximum lenght possible for this tree.
        """
        maxpaths_list = []
        if self.subtree_list == []:
            return [[self.mainnode]]

        subtree_maxdepth = 1
        for tree in self.subtree_list:
            subtree_maxpaths_list = tree.get_maxpaths_list_from_tree()
            #pdb.set_trace()
            if len(subtree_maxpaths_list[0]) >= subtree_maxdepth:
                if len(subtree_maxpaths_list[0]) > subtree_maxdepth:
                    subtree_maxdepth = len(subtree_maxpaths_list[0])
                    maxpaths_list = []
                maxpaths_list.extend(self.add_item_to_all_list(self.mainnode, subtree_maxpaths_list))

        return maxpaths_list

    def add_item_to_all_list(self, item_to_add, list_of_list):
        """
        add an item at first position of all sub lists in a list of lists.
        """
        list_of_list_to_return = []
        for mlist in list_of_list: 
            new_list = [item_to_add]
            new_list.extend(mlist)
            list_of_list_to_return.append(new_list)
        return list_of_list_to_return

