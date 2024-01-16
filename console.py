#!/usr/bin/python3
""" This is the Console Module for AirBnB project"""
import cmd
import sys
import shlex
import ast
from models.__init__ import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.place import Place
from models.review import Review
from models.city import City
from models.amenity import Amenity

class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = '', '', '', ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if '.' not in line or '(' not in line or ')' not in line:
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        class_Name = args.split()[0]
        if class_Name not in self.classes:
            print(args.split()[0])
            print("** class doesn't exist **")
            return
        new_instance = self.classes[class_Name]()
        args_list = shlex.split(args)
        for arg in args_list[1:]:
            try:
                key, value = arg.split('=')
                if '.' in value:
                    value = float(value)
                elif value.isdigit() or (value[0] == '-' and
                                         value[1:].isdigit()):
                    value = int(value)
                else:
                    value = value.replace('"', '').replace('_', ' ')
                setattr(new_instance, key, value)
            except ValueError:
                continue
        self.storage.save()
        print(new_instance.id)
        storage.save()

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        class_Name, _, obj_id = args.partition(" ")
        
        # guard against trailing args
        if obj_id and ' ' in obj_id:
            obj_id = obj_id.partition(' ')[0]

        if not class_Name:
            print("** class name missing **")
            return

        if class_Name not in self.classes:
            print("** class doesn't exist **")
            return

        if not obj_id:
            print("** instance id missing **")
            return

        key = f"{class_Name}.{obj_id}"
        try:
            print(self.storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        class_Name, _, obj_id = args.partition(" ")
       
        if obj_id and ' ' in obj_id:
            obj_id = obj_id.partition(' ')[0]

        if not class_Name:
            print("** class name missing **")
            return

        if class_Name not in self.classes:
            print("** class doesn't exist **")
            return

        if not obj_id:
            print("** instance id missing **")
            return

        key = f"{class_Name}.{obj_id}"

        try:
            del (self.storage.all()[key])
            self.storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            class_Name = args.split(' ')[0]  # remove possible trailing args
            if class_Name not in self.classes:
                print("** class doesn't exist **")
                return
            for key, value in self.storage.all(self.classes[className]).items():
                if key.split('.')[0] == class_Name:
                    print_list.append(str(value))
        else:
            for key, value in self.storage.all.items():
                print_list.append(str(value))

        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for key, value in self.storage.all().items():
            if args == key.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        class_Name, obj_id, *update_args= args.split()

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        
        if not class_Name:
        	print("** class name missing **")
		return

        # check for valid class name
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        # check for instance id
        if not obj_id:
            print("** instance id missing **")
            return

        # generate key from class and id
        key = f"{class_name}.{obj_id}"

        # check if key is present
        if key not in self.storage.all():
            print("** no instance found **")
            return

        # retrieve dictionary of current objects
        new_dict = self.storage.all()[key]

        # iterate through attribute names and values
        for i in range(0, len(update_args), 2):
            att_name = update_args[i]
            att_val = update_args[i + 1]

            # check for attribute name
            if not att_name:
                print("** attribute name missing **")
                return

            # check for attribute value
            if not att_val:
                print("** value missing **")
                return

            # type cast as necessary
            if att_name in self.types:
                att_val = self.types[att_name](att_val)

            # update dictionary with name, value pair
            new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

        

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
