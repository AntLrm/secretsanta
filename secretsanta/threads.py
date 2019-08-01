import pdb
from threading import Thread
from threading import Event
import random

class tree_pathfinding(Thread):
    def __init__(self, secretdraw):
        Thread.__init__(self)
        self.path_list = []
        self.secretdraw = secretdraw
        self.roll_result = []
        self.stop_event = Event()

    def run(self):
        self.compute_path_list()
        if not(self.stopped()):
            self.roll_result = random.choice(self.path_list)

    def compute_path_list(self):
        """
        Compute list of all possible solutions.
        """
        people_list = list(self.secretdraw.people.keys())
        gift_tree, maxdepth = self.get_tree(people_list[0], people_list[1:])
        if not(self.stopped()):
            if maxdepth == len(people_list):
                self.path_list = self.get_maxpaths_list_from_tree(gift_tree)
            else:
                print('No solution found. Your secret santa may be too constrained')
                sys.exit

    def get_tree(self, top_node, other_node_list):
        """
        Return a tree of solutions from a top node and a list of people.
        """
        output_tree = tree()
        if not(self.stopped()):
            output_tree.set_mainnode(top_node)
            max_subtree_depth = 0 
            children_list = self.get_children(top_node, other_node_list)

            if len(children_list) == 0 :
                return output_tree, max_subtree_depth + 1
            else :
                for child in children_list :
                    if self.stopped():
                        break
                    reduced_node_list = other_node_list[:]
                    reduced_node_list.remove(child)
                    subtree, subtree_depth = self.get_tree(child, reduced_node_list)
                    output_tree.addsubtree(subtree)
                    if subtree_depth > max_subtree_depth:
                        max_subtree_depth = subtree_depth
                return output_tree, max_subtree_depth + 1 
        else:
            return output_tree, 0 
    
    def get_children(self, top_node, candidates):
        """
        Get all possible people to offer a gift.
        """
        children_list = []
        for name in candidates:
            if not (name in self.secretdraw.constrain[top_node]):
                children_list.append(name)
        return children_list

    def get_maxpaths_list_from_tree(self, mtree):
        """
        Return the list of all paths that have the maximum lenght possible for this tree.
        """
        maxpaths_list = []
        if mtree.subtree_list == []:
            return [[mtree.mainnode]]

        subtree_maxdepth = 1
        for subtree in mtree.subtree_list:
            subtree_maxpaths_list = self.get_maxpaths_list_from_tree(subtree)
            if len(subtree_maxpaths_list[0]) >= subtree_maxdepth:
                if len(subtree_maxpaths_list[0]) > subtree_maxdepth:
                    subtree_maxdepth = len(subtree_maxpaths_list[0])
                    maxpaths_list = []
                maxpaths_list.extend(mtree.add_item_to_all_list(mtree.mainnode, subtree_maxpaths_list))

        return maxpaths_list

    def get_roll_result(self):
        return self.roll_result

    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()


class random_pathfinding(Thread):
    def __init__(self, secretdraw):
        Thread.__init__(self)
        self.secretdraw = secretdraw
        self.roll_result = [] 
        self.stop_event = Event()

    def run(self):
        self.roll_result = self.getrandom_path()

    def getrandom_path(self):
        people_list = list(self.secretdraw.people.keys())
        path = [] 
        while len(path) < len(people_list) and not(self.stopped()):
            path = []
            people_not_in_path = people_list[:]
            available_names = people_list[:]
            while len(available_names) > 0 and not(self.stopped()):
                next_name = random.choice(available_names)
                path.append(next_name)
                people_not_in_path.remove(next_name)
                available_names = people_not_in_path[:]
                for constrain in self.secretdraw.constrain[next_name]:
                    if constrain in available_names:
                        available_names.remove(constrain)
        
        if self.stopped():
            return []
        else:
            return path

    def get_roll_result(self):
        return self.roll_result

    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()
                
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
