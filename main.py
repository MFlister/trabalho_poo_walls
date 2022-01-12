from datetime import datetime
from inquirer.questions import Text
import pandas as pd
import inquirer
from pandas.core.algorithms import mode
from pandas.io.parsers import read_csv
import os
import re
from task import TaskManager, Task



def MainMenu():
    questions = [
        inquirer.List(
            "opcao",
            message="Gerenciador de Tarefas: O que deseja fazer?",
            choices=["Adicionar Tarefa", "Mudar status",
                     "Deletar Tarefa", "Mostrar Tarefas", "Sair"],
        ),
    ]

    answers = inquirer.prompt(questions)

    return answers['opcao']

# Filtra os dados recebidos do usuário e retorna um objeto Task

def dataTaskDictProcessing(task_dict):

    title = ' '.join(task_dict['title'].split())

    if title == "":
        print("\nO título da tarefa é obrigatório\n")
        return None
    else:
        #title = task_dict['title'].strip("\n")
        description = task_dict['description'].rstrip("\n")

        if task_dict['tag'] == '':
            tag = 'Default'
        else:
            tag = task_dict['tag']

        if task_dict['date'] == '':
            date = datetime.today()
        elif re.match(r"^(?:(?:31(\/)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$", task_dict['date']):
            date = datetime.strptime(task_dict['date'], '%d/%m/%Y')
        else:
            print("\nData informada inválida\n")
            return None

        return Task(title, description, tag, date)

if __name__ == '__main__':

    task_manager = TaskManager()

    while True:
        choice = MainMenu()

        if choice == 'Adicionar Tarefa':
            task_dict = task_manager.getTask()
            task = dataTaskDictProcessing(task_dict)

            if task != None:
                task_manager.add(task)

        elif choice == 'Mudar status':
            title = task_manager.getTitle()
            task_manager.updateStatus(title)

        elif choice == 'Deletar Tarefa':
            title = task_manager.getTitle()
            task_manager.deleteTask(title)

        elif choice == 'Mostrar Tarefas':
            date = task_manager.getDate()
            task_manager.showTasks(date)

        elif choice == 'Sair':
            break
