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

    # Adiciona Task
    def add(self, task):
        df = pd.DataFrame(task.__dict__, index=[0])

        if os.path.isfile("."+self.url):

            tasks = pd.read_csv(os.path.dirname(
                os.path.abspath(__file__)) + self.url)

            if not tasks.loc[tasks['title'] == task.title].empty:
                print("\nTarefa já existente\n")
                return None

            df.to_csv(os.path.dirname(
                os.path.abspath(__file__)) + self.url, mode='a', header=None, index=False)
        else:
            df.to_csv(os.path.dirname(
                os.path.abspath(__file__)) + self.url, mode='a', index=False)

        print("\nTarefa Adicionada com Sucesso\n")

    # Atualiza Status da Task
    def updateStatus(self, title):

        if not os.path.isfile("."+self.url):
            print("\nLista de Tarefas Inexistente: cadastre alguma tarefa\n")
            return None

        tasks = pd.read_csv(os.path.dirname(
            os.path.abspath(__file__)) + self.url)

        if tasks.empty:
            print("\nLista de Tarefas Vazia\n")
        else:

            if tasks.loc[tasks['title'] == title].empty:
                print("\nNão há nenhuma tarefa com este título\n")
            else:

                current_status = tasks.loc[tasks['title'] == title]['status']

                print(f"\nTarefa '{title}': {current_status.iloc[0]}\n")

                choice_status = self.__showChoiceStatus()
                tasks.loc[tasks['title'] == title, 'status'] = choice_status
                tasks.to_csv(os.path.dirname(
                    os.path.abspath(__file__)) + self.url, index=False)

                print("\nStatus Atualizado\n")

    # Deleta a Task
    def deleteTask(self, title):

        if not os.path.isfile("."+self.url):
            print("\nLista de Tarefas Inexistente: cadastre alguma tarefa\n")
            return None

        tasks = pd.read_csv(os.path.dirname(
            os.path.abspath(__file__)) + self.url)

        if tasks.empty or not os.path.isfile("."+self.url):
            print("\nLista de Tarefas Vazia\n")
        else:
            if tasks.loc[tasks['title'] == title].empty:
                print("\nNão há nenhuma tarefa com este título\n")
            else:
                task = tasks.loc[tasks['title'] == title]
                tasks.drop(task.index, inplace=True)
                tasks.to_csv(os.path.dirname(
                    os.path.abspath(__file__)) + self.url, index=False)
                
                print("\nTarefa deletada com sucesso\n")

    def showTasks(self, date=None):
        if not os.path.isfile("."+self.url):
            print("\nLista de Tarefas Inexistente: cadastre alguma tarefa\n")
            return None

        tasks = pd.read_csv(os.path.dirname(
            os.path.abspath(__file__)) + self.url)
        
        if date != '':
            tasks = tasks.loc[tasks['target_date'] == date]

            if tasks.empty:
                print('\nNão há nada para ser visualizado\n')
                return None

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
        questions = [
            inquirer.Editor(name='title', message='Título'),
            inquirer.Editor(name='description', message='Descrição'),
            Text(
                name='tag', message='Tag (deixe em branco caso não queira colocar uma tag)'),
            Text(name='date', message='Data (deixe em branco caso a data seja hoje - formato: dd/mm/AAAA)')
        ]

        return inquirer.prompt(questions)

    # Input do título pelo usuário
    
    @staticmethod
    def getTitle():

        questions = [
            inquirer.Text(name='title', message='Digite o título da tarefa')
        ]

        answers = inquirer.prompt(questions)

        return answers['title']

    @staticmethod
    def getDate():

        questions = [
            inquirer.Text(name='date', message='Digite a data a ser filtrado (deixe em branco caso queira mostrar todos)')
        ]

        answers = inquirer.prompt(questions)

        return answers['date']