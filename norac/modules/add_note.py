#!/usr/bin/env python
import tempfile
import os

class AddNoteModule:
    def __init__(self, config, connection):
        self.editor = config.get("default", "editor")
        self.connection = connection
    
    def get_shorthand(self):
        return "-a"
   
    def get_longhand(self):
        return "--add_note"

    def get_description(self):
        return "Adds a note to the database. Opens the editor chosen in the configuration file."

    def handle(self, args):
        filehandle, path = tempfile.mkstemp(prefix="new_note_tmp") 
        os.system("%s %s" % (self.editor, path))

        with open(path, "r") as f:
            note = "".join(f.readlines())
        os.remove(path)
        response = self.connection.send_request({ "command" : "add_note", "meta" : [], "data" : note })
        print(response)
