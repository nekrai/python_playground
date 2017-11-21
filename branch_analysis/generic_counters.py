import os


class FileType:
    def __init__(self, file_type):
        self.file_type = file_type
        self.count = 0

    def process(self, path, filename):
        if filename.endswith(self.file_type):
            self.count += 1

    def description(self):
        return '# {0} files'.format(self.file_type)

    def print_result(self):
        print self.description(), self.count


class LineCrawler:
    def __init__(self, file_type):
        self.file_type = file_type
        self.listeners = []

    def add_listener(self, listener):
        self.listeners.append(listener)

    def process(self, path, filename):
        if filename.endswith(self.file_type):
            i = 0
            with open(os.path.join(path, filename)) as f:
                for i, l in enumerate(f, 1):
                    for listener in self.listeners:
                        listener.process(path, filename, i, l)

    def print_result(self):
        for listener in self.listeners:
            listener.print_result()