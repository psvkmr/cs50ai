# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 10:53:09 2020

@author: p.sivakumar
"""

import os
os.getcwd()
os.chdir('C:\\Users\\prasa\\Documents\\Github\\Harvard_AI')

import pygame
import random

# create empty minesweeper board
class MS():
    
    def __init__(self, height=8, width=8, mines=8):
        self.height = height
        self.width = width
        self.mines = set()
        self.board = [[False for x in range(width)] for x in range(height)]
        
        while len(self.mines) != mines:
            coord = [random.randrange(height), random.randrange(width)]
            if not self.board[coord[0]][coord[1]]:
                self.board[coord[0]][coord[1]] = True
                self.mines.add((coord[0],coord[1]))
                
        self.mines_found = set()
            
    def is_mine(self, cell):
        return self.board[cell[0]][cell[1]]
    
    def nearby_mines_count(self, cell):
        i,j = cell
        nearby_coords = [[i-1,j-1],[i-1,j],[i-1,j+1],[i,j-1],[i,j+1],[i+1,j-1],[i+1,j],[i+1,j+1]]
        nearby_cells = [cell for cell in nearby_coords if (cell[0] in range(self.height) and cell[1] in range(self.width))]
        nearby_cells_in_board = [self.board[cell[0]][cell[1]] for cell in nearby_cells]
        nearby_mines = [self.is_mine(cell) for cell in nearby_cells]
        near_counts = nearby_mines.count(True)
        print([nearby_cells, nearby_cells_in_board, nearby_mines])
        return near_counts

    def won(self):
        return self.mines_found == self.mines
        

# create logical sentence around board cells and number of mines
class Sentence():
        
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        #self.safes = set()
        #self.mines = set()
        
    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count
    
    def __str__(self):
        return f"{self.cells} = {self.count}"
    
    def known_mines(self):
        # return set of all cells in self.cells known to be mines
        if len(self.cells) == self.count:
            return(self.cells)
        
    def known_safes(self):
        # return set of all cells in self.cells known to be safe
        #if self.count == 0 and len(self.cells) != 0:
        if self.count == 0:
            return self.cells
        
    def mark_mine(self, cell):
        #updates internal knowledge representation given the fact that a cell is known to be a mine
        if cell in self.cells:
            #self.mines.add(cell)
            self.cells.remove(cell)
            self.count -= 1
                    
    def mark_safe(self, cell):
        #updates interal knowledge representation given the fact that a cell is known to be safe
        if cell in self.cells:
            #self.safes.add(cell)
            self.cells.remove(cell)
            

# create MS gameplayer
class MinesweeperAI():
    
    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []
        
    def mark_mine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
            
    def mark_safe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            
    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        #self.safes.add(cell)
        self.mark_safe(cell)
        self.knowledge.append(Sentence(cell, 0))
        for sentence in self.knowledge:
            if sentence.known_mines() is not None:
                for cell in sentence.cells:
                    self.mines.add(cell)
            if sentence.known_safes() is not None:
                for cell in sentence.cells:
                    self.safes.add(cell)
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if (sentence1.cells.issubset(sentence2.cells)) & (sentence1.cells != sentence2.cells):
                    new_sentence_cells = sentence2.cells.difference(sentence1.cells)
                    new_sentence_count = sentence2.count - sentence1.count
                    new_sentence = Sentence(new_sentence_cells, new_sentence_count)
                    self.knowledge.append(new_sentence)
            
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = self.safes.difference(self.mines).difference(self.moves_made)
        move = safe_moves.pop()
        self.moves_made.add(move)
        return move
        
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        total_moves = set([(x,y) for x in range(self.height) for y in range(self.width)])
        rand_moves = total_moves.difference(self.moves_made).difference(self.mines)
        move = rand_moves.pop()
        self.moves_made.add(move)
        return move
        