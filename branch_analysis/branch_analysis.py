import os

import generic_counters
import line_counters

listeners = []


def get_all_files(folder):
    for path, dirs, files in os.walk(folder):
        for filename in files:
            for listener in listeners:
                listener.process(path, filename)


file_counter = generic_counters.FileType('.py')
listeners.append(file_counter)

line_crawler = generic_counters.LineCrawler('.py')
listeners.append(line_crawler)

line_counter = line_counters.LineCounter()
todo_list = line_counters.Finder('TODO')

line_crawler.add_listener(line_counter)
line_crawler.add_listener(todo_list)


get_all_files("C:\\PythonProjects\\Playground")

file_counter.print_result()
line_crawler.print_result()
