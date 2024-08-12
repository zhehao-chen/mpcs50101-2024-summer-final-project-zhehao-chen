import argparse
import pickle
import uuid
from datetime import date, timedelta

unique_id = uuid.uuid4()
print(type(unique_id))
print(unique_id)

today = date.today()
dates = date.today()-timedelta(days=1)


dif = today -dates
print(dif)

print(len("7488748e-7062-4f0d-bdc1-0e1fcd5b1e1b"))