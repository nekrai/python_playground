import os


class LineCounter:
    def __init__(self):
        self.line_count = {}

    def process(self, path, filename, line_number, line_content):
        key = os.path.join(path, filename)
        self.line_count[key] = line_number

    def result_file(self, path, filename):
        return self.line_count[os.path.join(path, filename)]

    def result_all(self):
        return self.line_count

    def description(self):
        return '# total lines'

    def print_result(self):
        print self.description()
        for file_path in self.line_count.keys():
            print file_path, self.line_count[file_path]


class EmptyLineCounter(LineCounter):
    def __init__(self):
        LineCounter.__init__(self)

    def process(self, path, filename, line_number, line_content):
        if '\n' == line_content:
            key = os.path.join(path, filename)
            if key in self.line_count.keys():
                self.line_count[key] += 1
            else:
                self.line_count[key] = 1

    def description(self):
        return '# total empty lines'


class Finder(LineCounter):
    def __init__(self, string_to_find):
        LineCounter.__init__(self)
        self.string_to_find = string_to_find

    def process(self, path, filename, line_number, line_content):
        if self.string_to_find in line_content:
            key = os.path.join(path, filename)
            if key in self.line_count.keys():
                self.line_count[key].append(line_number)
            else:
                self.line_count[key] = [line_number]

    def description(self):
        return '# files with {0}'.format(self.string_to_find)
