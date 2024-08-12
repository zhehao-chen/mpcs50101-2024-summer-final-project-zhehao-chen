import argparse


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

print("Add: ",args.add)
print("Due: ",args.due)
print("Priority:", args.priority)
print("List:", args.list)
print("Query:", args.query)
