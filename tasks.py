import argparse
import pickle
import uuid
from datetime import date, datetime


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
     '''representation of a task'''
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
        '''open a pickle file'''
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
        '''print all the non-completed tasks in a formatted table'''

        non_completed_tasks = []
        for task in self.tasks:
            if task.completed == None:
                non_completed_tasks.append(task)
        non_completed_tasks.sort(key=lambda x: (x.due_date if x.due_date else date.max, x.priority))

        #print the table
        print(f'{'ID':<40}  {'Age': <5}  {'Due Date':<12}  {"Priority":<9}  {"Task":<50}')
        print(f'{'--':<40}  {'---': <5}  {'--------':<12}  {"--------":<9}  {"----":<50}')

        for task in non_completed_tasks:
            age = (date.today() - task.created).days
            print(f'{task.unique_id:<40}  {age: <5}  {str(task.due_date.strftime("%d/%m/%Y")) if task.due_date else "-":<12}  {task.priority:<9}  {task.name:<50}')


   def report(self):
        '''print all the tasks including completed, not including deleted task'''
        self.tasks.sort(key=lambda x: (x.due_date if x.due_date else date.max, x.priority))

        print(f'{'ID':<40}  {'Age': <5}  {'Due Date':<12}  {"Priority":<9}  {"Task":<30}  {"Created":<30}  {"Completed":<20}')
        print(f'{'--':<40}  {'---': <5}  {'--------':<12}  {"--------":<9}  {"----":<30}  {"-------":<30}  {"---------":<20}')
        for task in self.tasks:
            age = (date.today() - task.created).days
            print(f'{task.unique_id:<40}  {age:<5}  {str(task.due_date.strftime("%d/%m/%Y")) if task.due_date else "-":<12}  {task.priority:<9}  {task.name:<30}  {str(task.created.strftime("%a %b %d %H:%M:%S CST %Y")):<30}  {str(task.completed.strftime("%a %b %d %H:%M:%S CST %Y")) if task.completed else "-":<30}')
         

   def done(self, unique_id):
        '''mark a task as complete'''
        for task in self.tasks:
            if task.unique_id == unique_id:
                task.completed = date.today()
        self.pickle_dump()


   def delete(self, unique_id):
       '''delete a task'''
       for task in self.tasks:
           if task.unique_id == unique_id:
               self.tasks.remove(task)
       self.pickle_dump()

   def query(self, user_input):
        '''query a key word or multipe key words in the task list'''
        query_result = []
        for task in self.tasks:
            for item in user_input:
               if item.lower() in task.name.lower():
                    query_result.append(task)
        if query_result == []:
            print("no result founded.")
        else:
            print(f'{'ID':<40}  {'Age': <5}  {'Due Date':<12}  {"Priority":<9}  {"Task":<50}')
            print(f'{'--':<40}  {'---': <5}  {'--------':<12}  {"--------":<9}  {"----":<50}')
            for task in query_result:
                age = (date.today() - task.created).days
                print(f'{task.unique_id:<40}  {age: <5}  {str(task.due_date.strftime("%d/%m/%Y")) if task.due_date else "-":<12}  {task.priority:<9}  {task.name:<50}')
                

   def add(self, name, priority = 1, due_date=None):
       '''add a new task'''
       def int_check(name):
          try:
               int(name)
               return True
          except ValueError:
               return False
          
       if int_check(name) == True:
          return print('There was an error in creating your task. Run "todo -h" for usage instructions.')
       else:
          if due_date:
               try:
                    due_date = datetime.strptime(due_date,'%d/%m/%Y').date()
               except ValueError:
                    return print('Please enter the due date in the format of mm/dd/yyyy')
                   
          new_task = Task(name = name, priority=priority, due_date=due_date)
          self.tasks.append(new_task)
          print(f'Created task {new_task.unique_id} with due date {new_task.due_date.strftime("%d/%m/%Y")}')
          self.pickle_dump()


def main():
     parser = argparse.ArgumentParser(description='Update your ToDo list.')

     parser.add_argument('--add', type = str, required=False, help='a task string to add to your list')
     parser.add_argument('--due', type = str, required=False, help='due date in mm/dd/yyyy format')
     parser.add_argument('--priority', type = int, required=False, default=1, help='priority of task; default value is 1')
     parser.add_argument('--delete', type = str, required=False, help='a task string delete from your list')
     parser.add_argument('--done', type = str, required=False, help='mark a task as done')
     parser.add_argument('--list', action='store_true', required=False, help='list all tasks that have not been completed')
     parser.add_argument('--report', action='store_true', required=False, help='list all tasks that have not been deleted')
     parser.add_argument('--query', type = str, required=False, nargs="+", help='find the task by a given input')



     args = parser.parse_args()

     task_list = Tasks()

     if args.add:
         task_list.add(args.add, args.priority, args.due)
     elif args.list:
         print(f'all the tasks need to do')
         task_list.list()
     elif args.delete:
         task_list.delete(args.delete)
     elif args.report:
         task_list.report()
     elif args.done:
         task_list.done(args.done)
     elif args.query:
         task_list.query(args.query)


if __name__ == '__main__':
     main()