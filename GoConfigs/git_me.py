from git import Repo
import os

path = 'C:\\PythonProjects\\python_playground'

repo = Repo.init(path).git

index = Repo.init(path).index

repo.add('C:\\PythonProjects\\python_playground\\GoConfigs\\git_me.py')

index.commit("commit from python!")
