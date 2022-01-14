from datetime import datetime
from inquirer.questions import Text
import pandas as pd
import inquirer
from pandas.core.algorithms import mode
from pandas.io.parsers import read_csv
import os
import re


# Classe Tarefa


class Task:

    def __init__(self, title, description=None, tag='Default', target_date=datetime.today()):

        if target_date.date() < datetime.today().date():
            raise ValueError("A data informada é menor que a data corrente!")
        else:
            self.title = title
            self.description = description
            self.tag = tag
            self.status = 'Pendente'
            self.target_date = target_date.strftime("%d/%m/%Y")

# Classe Gerenciador de Tarefas


class TaskManager:

    def __init__(self, url='/tarefas.csv'):
        self.url = url
        self.directory_csv = os.path.dirname(
            os.path.abspath(__file__)) + self.url

    # Adiciona Task
    def add(self, task):
        df = pd.DataFrame(task.__dict__, index=[0])

        if os.path.isfile(self.directory_csv):

            tasks = pd.read_csv(self.directory_csv)

            if not tasks.loc[tasks['title'] == task.title].empty:
                print("\033[31m"+"\nTarefa já existente\n"+"\033[31m")
                return None

            df.to_csv(self.directory_csv, mode='a', header=None, index=False)
        else:
            df.to_csv(self.directory_csv, mode='a', index=False)

        print("\033[32m" + "\nTarefa Adicionada com Sucesso\n" + "\033[32m")

    # Atualiza Status da Task
    def updateStatus(self, title):

        if not self.__CSVFileExist():
            return None

        tasks = pd.read_csv(self.directory_csv)

        if tasks.empty:
            print("\033[31m"+"\nLista de Tarefas Vazia\n"+"\033[31m")
            return None

        if tasks.loc[tasks['title'] == title].empty:
            print("\033[31m" +
                  "\nNão há nenhuma tarefa com este título\n"+"\033[31m")
        else:

            current_status = tasks.loc[tasks['title'] == title]['status']

            print(f"\033[33m \nTarefa '{title}': {current_status.iloc[0]}\n \033[33m")

            choice_status = self.__showChoiceStatus()
            tasks.loc[tasks['title'] == title, 'status'] = choice_status
            tasks.to_csv(self.directory_csv, index=False)

            print("\033[32m"+"\nStatus Atualizado\n"+"\033[32m")

    # Deleta a Task
    def deleteTask(self, title):

        if not self.__CSVFileExist():
            return None

        tasks = pd.read_csv(self.directory_csv)

        if tasks.empty:
            print("\033[31m"+"\nLista de Tarefas Vazia\n"+"\033[31m")
            return None

        if tasks.loc[tasks['title'] == title].empty:
            print("\033[31m" +
                  "\nNão há nenhuma tarefa com este título\n"+"\033[31m")
        else:
            task = tasks.loc[tasks['title'] == title]
            tasks.drop(task.index, inplace=True)
            tasks.to_csv(self.directory_csv, index=False)

            print("\033[32m"+"\nTarefa deletada com sucesso\n"+"\033[32m")

    def showTasks(self, date=None):

        if not self.__CSVFileExist():
            return None

        tasks = pd.read_csv(self.directory_csv)

        if tasks.empty:
            print("\033[31m"+'\nNão há nada para ser visualizado\n'+"\033[31m")
            return None

        if date != '':
            tasks = tasks.loc[tasks['target_date'] == date]

        print("\n################### Tarefas ###################")

        for _, task in tasks.iterrows():
            print(f'''
                Titulo: {task['title']}
                Descrição: {task['description']}
                Tag: {task['tag']}
                Data: {task['target_date']}
                Status: {task['status']}

                ###############################################
            ''')
        print("###############################################\n")

    def __CSVFileExist(self):
        if not os.path.isfile(self.directory_csv):
            print(
                "\033[31m"+"\nLista de Tarefas Inexistente: cadastre alguma tarefa\n"+"\033[31m")
            return False
        else:
            return True

    # Mostra as opções de mudar o status
   
   
    @staticmethod
    def __showChoiceStatus():
        questions = [
            inquirer.List(
                "status",
                message="Atualizar status da mensagem",
                choices=["Pendente", "Concluído"],
            ),
        ]

        answers = inquirer.prompt(questions)
        return answers['status']

    # Input dados da Task do usuário
   
    @staticmethod
    def getTask():

        data = dict()

        title = input("[?] Título: ")
        description = input('[?] Descrição: ')
        tag = input(
            '[?] Tag (deixe em branco caso não queira colocar uma tag): ')
        date = input(
            '[?] Data (deixe em branco caso a data seja hoje - formato: dd/mm/AAAA): ')

        data['title'] = title
        data['description'] = description
        data["tag"] = tag
        data['date'] = date

        return data

    # Input do título pelo usuário
    @staticmethod
    def getTitle():

        title = input('\nDigite o título da tarefa: ')

        return title

    @staticmethod
    def getDate():

        questions = [
            inquirer.Text(
                name='date', message='Digite a data a ser filtrado (deixe em branco caso queira mostrar todos)')
        ]

        answers = inquirer.prompt(questions)

        return answers['date']


