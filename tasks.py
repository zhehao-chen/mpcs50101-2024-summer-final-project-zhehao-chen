import argparse
import pickle
import uuid
import re
from datetime import date,timedelta


class Task:
  """Representation of a task
  
  Attributes:
              - created - date
              - completed - date
              - name - string
              - unique id - number
              - priority - int value of 1, 2, or 3; 1 is default
              - due date - date, this is optional
  """
  def __init__(self, name, unique_id = None, created = None, due_date = None, completed = None, priority = 1):
     #name
     self.name = name
     #priority
     self.priority = priority
     #due_date
     self.due_date = due_date
     # created
     if created != None:
        self.created = created
     else:
        self.created = date.today()
     #completed
     self.completed = completed
     #unique_id
     if unique_id != None:
        self.unique_id = unique_id
     else:
        self.unique_id = str(uuid.uuid4())

     
class Tasks:
   """A list of `Task` objects."""
   def __init__(self, filename = '.todo.pickle'):
        """Read pickled tasks file into a list"""
        # List of Task objects
        self.tasks = []
        self.filename = filename
        self.pickle_load()
    
   def pickle_load(self):
        try:
           with open(self.filename, 'rb') as f:
              self.tasks = pickle.load(f)
        
        except FileNotFoundError:
           self.tasks = []
           

   def pickle_dump(self):
        """Picle your task list to a file"""
        with open(self.filename, 'wb') as f:
            pickle.dump(self.tasks, f)

    # Complete the rest of the methods, change the method definitions as needed
   def list(self):
        '''print all the tasks in a formatted table'''

        non_completed_tasks = []
        for task in self.tasks:
            if task.completed == None:
                non_completed_tasks.append(task)
        non_completed_tasks.sort(key=lambda x: (x.due_date if x.due_date else date.max, x.priority))

        #print the table
        print(f'{'ID':<100}  {'Age': <5}  {'Due Date':<12}  {"Priority":<9}  {"Task":<50}')
        print(f'{'--':<100}  {'---': <5}  {'--------':<12}  {"--------":<9}  {"----":<50}')

        for task in non_completed_tasks:
            age = (date.today() - task.created).days
            print(f'{task.unique_id:<100}  {age: <5}  {task.due_date if task.due_date else "-":<12}  {task.priority:<9}  {task.name:<50}')


   def report(self):
        self.tasks.sort(key=lambda x: (x.due_date if x.due_date else date.max, x.priority))

        print(f'{'ID':<100}  {'Age': <5}  {'Due Date':<12}  {"Priority":<9}  {"Task":<50}  {"Created":<50}  {"Completed":<50}')
        print(f'{'--':<100}  {'---': <5}  {'--------':<12}  {"--------":<9}  {"----":<50}  {"-------":<50}  {"---------":<50}')
        for task in self.tasks:
            age = timedelta(date.today() - task.created)
            print(f'{task.unique_id: < 20}  {age: <5}  {task.due_date if task.due_date else "-":<12}  {task.priority:<9}  {task.name:<50}  {task.created:<50}  {task.completed if task.completed else "-":<50}')
            

   def done(self, unique_id):
        for task in self.tasks:
            if task.unique_id == unique_id:
                task.completed = date.today()
        self.pickle_dump()


   def delete(self, unique_id):
       for task in self.tasks:
           if task.unique_id == unique_id:
               self.tasks.remove(task)
       self.pickle_dump()

   def query(self):
        pass

   def add(self, name, priority = 1, due_date = None):
       new_task = Task(name = name, priority=priority, due_date=due_date)
       self.tasks.append(new_task)
       print(f'Created task {new_task.unique_id}')
       self.pickle_dump()


def main():
     parser = argparse.ArgumentParser(description='Update your ToDo list.')

     parser.add_argument('--add', type = str, required=False, help='a task string to add to your list')
     parser.add_argument('--due', type = str, required=False, help='due date in dd/mm/yyyy format')
     parser.add_argument('--priority', type = int, required=False, default=1, help='priority of task; default value is 1')
     parser.add_argument('--delete', type = str, required=False, help='a task string delete from your list')
     parser.add_argument('--done', type = str, required=False, help='mark a task as done')
     parser.add_argument('--list', action='store_true', required=False, help='list all tasks that have not been completed')
     parser.add_argument('--report', action='store_true', required=False, help='list all tasks that have not been deleted')
     parser.add_argument('--query', type = str, required=False, nargs="+", help='find the task by a given input')



     args = parser.parse_args()

     task_list = Tasks()

     if args.add:
         print(f'A new task {args.add} will be added to our to-do list with a priority of {args.priority}')
         task_list.add(args.add, args.priority)
     elif args.list:
         print(f'all the tasks need to do')
         task_list.list()


if __name__ == '__main__':
     main()