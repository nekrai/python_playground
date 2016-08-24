import os
import generic_counters

listeners = []


def get_all_files(folder):
    for path, dirs, files in os.walk(folder):
        for filename in files:
            for listener in listeners:
                listener.process(path, filename)

    for listener in listeners:
        listener.print_result()


def print_filename(path, filename):
    print path, filename


listeners.append(generic_counters.FileType('.jar'))
listeners.append(generic_counters.FileType('.py'))
listeners.append(generic_counters.FileType('.cs'))
listeners.append(generic_counters.FileType('.java'))
listeners.append(generic_counters.FileType('.bat'))
listeners.append(generic_counters.FileType('.sh'))

get_all_files("C:\\workspace")