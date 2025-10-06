# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 11:05:56 2024

@author: IITM
"""

class Binary_Tree:
    def __init__(self, data):
        self.data=data
        self.left=None
        self.right=None
        self.children=[]
        
    def insert_child(self,data,left_node,right_node):
        if data not in self.children:
            self.children.append(data)

        self.children.append(left_node,right_node)
        self.left=left_node
        self.right=right_node
        
    def traverse(self):
        nodes_to_visit=[self]
        while len(nodes_to_visit)>0:
            current_node=nodes_to_visit.pop()
            nodes_to_visit+=current_node.children
            
#%% SO solution
class Node:
    """
    Class Node
    """
    def __init__(self, value):
        self.left = None
        self.data = value
        self.right = None

class Tree:
    """
    Class tree will provide a tree as well as utility functions.
    """

    def createNode(self, data):
        """
        Utility function to create a node.
        """
        return Node(data)

    def insert(self, node , data):
        """
        Insert function will insert a node into tree.
        Duplicate keys are not allowed.
        """
        #if tree is empty , return a root node
        if node is None:
            return self.createNode(data)
        # if data is smaller than parent , insert it into left side
        if data < node.data:
            node.left = self.insert(node.left, data)
        elif data > node.data:
            node.right = self.insert(node.right, data)

        return node