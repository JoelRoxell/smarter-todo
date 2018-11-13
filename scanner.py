import os
import re

core_dir = './sample'
issues = []


class Issue():
    def __init__(self, description, labels, estimate):
        self.description = description
        self.labels = labels
        self.estimate = estimate


for dir_name, subs, file_list in os.walk(core_dir):
    print(subs, file_list)

    for file in file_list:
        file_path = os.path.abspath("{}/{}".format(dir_name, file))

        if not os.path.isfile(file_path):
            break

        with open(file_path) as file:
            next_line = file.readline()

            while (len(next_line)):
                todo = re.search(r'TODO:(.*?)\[', next_line)
                labels = re.search(r'\[(.*?)\]', next_line)
                estimate = re.search(r'([0-9]+[m|h])', next_line)

                if todo:
                    todo = str.strip(todo.group(1))
                    labels = labels.group(1).split(',')
                    estimate = estimate.group(1)

                    issues.append(Issue(todo, labels, estimate))

                next_line = file.readline()

print(issues)
