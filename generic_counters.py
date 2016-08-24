import os

class FileType:
    def __init__(self, file_type):
        self.file_type = file_type
        self.count = 0

    def process(self, path, filename):
        if filename.endswith(self.file_type):
            self.count += 1

    def result(self):
        return self.count

    def description(self):
        return '# {0} files'.format(self.file_type)

    def print_result(self):
        print self.description(), self.result()


class TotalLines:
    def __init__(self, file_type):
        self.file_type = file_type
        self.total_lines = []

    def process(self, path, filename):
        if filename.endswith(self.file_type):
            i = 0
            with open(os.path.join(path, filename)) as f:
                for i, l in enumerate(f, 1):
                    pass
            self.total_lines.append((os.path.join(path,filename), i))

    def result(self):
        return self.total_lines

    def description(self):
        return '# total lines in {0} files'.format(self.file_type)

    def print_result(self):
        print self.description()
        for full_path, count in self.total_lines:
            print full_path, count


class EmptyLines:
    def __init__(self, file_type):
        self.file_type = file_type
        self.empty_lines = []

    def process(self, path, filename):
        if filename.endswith(self.file_type):
            count = 0
            with open(os.path.join(path, filename)) as f:
                for i, l in enumerate(f, 1):
                    if '\n' == l:
                        count += 1
            self.empty_lines.append((os.path.join(path,filename), count))

    def result(self):
        return self.empty_lines

    def description(self):
        return '# empty lines in {0} files'.format(self.file_type)

    def print_result(self):
        print self.description()
        for full_path, count in self.empty_lines:
            print full_path, count