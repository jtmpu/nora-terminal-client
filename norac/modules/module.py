#!/usr/bin/env python

from . import add_note

class Handler:
    '''
    Handles the creation of modules for the application
    '''
    def __init__(self, config, connection):
        self.config = config
        self.connection = connection
        self.modules = {}

    def create_modules(self):   
        self.modules["add_note"] = add_note.AddNoteModule(self.config, self.connection)
    
    def get_modules(self):
        return self.modules


