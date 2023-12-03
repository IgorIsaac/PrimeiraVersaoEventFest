import os
import json
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# Constantes
PATH_EVENTS = 'events.data'
DAYS_BEFORE_NEARBY = 30
HOURS_BEFORE_START = 12

# Classes
class Event(ABC):
    def __init__(self, name, address, price, category, hour, date, description):
        self.name = name
        self.address = address
        self.price = price
        self.category = category
        self.hour = hour
        self.date = date
        self.description = description

    @abstractmethod
    def is_active(self):
        pass

    @abstractmethod
    def is_upcoming(self):
        pass

    @abstractmethod
    def is_passed(self):
        pass


class ConcreteEvent(Event):
    def __init__(self, name, address, price, category, hour, date, description):
        super().__init__(name, address, price, category, hour, date, description)
        self.users = []
        
    def is_active(self):
        # lógica para verificar se o evento está ativo
        pass

    def is_upcoming(self):
        # lógica para verificar se o evento está próximo
        pass

    def is_passed(self):
        # lógica para verificar se o evento foi aprovado
        pass

    def __str__(self):
        return f"Event: {self.name}\nAddress: {self.address}\nPrice: {self.price}\nCategory: {self.category}\nHour: {self.hour}\nDate: {self.date}\nDescription: {self.description}"

    def to_json(self):
        return {
            'name': self.name,
            'address': self.address,
            'price': self.price,
            'category': self.category,
            'hour': self.hour,
            'date': self.date,
            'description': self.description
        }
        
    def event_datetime(self):
        return datetime.strptime(f"{self.date} {self.hour}", "%d/%m/%Y %H:%M")
        
class EventUser:
    def __init__(self, user, event, participating):
        self.user = user
        self.event = event
        self.participating = participating


class User:
    def __init__(self, name, age, sex, cellphone, address):
        self.name = name
        self.age = age
        self.sex = sex
        self.cellphone = cellphone
        self.address = address

    def serialize(self):
        return {
            'name': self.name,
            'age': self.age,
            'sex': self.sex,
            'cellphone': self.cellphone,
            'address': self.address
        }
        
# Funções
def save_events(events):
    serialized_events = []

    for event in events:
        if isinstance(event, ConcreteEvent):
            serialized_events.append(event.to_json())

    with open(PATH_EVENTS, 'w') as file:
        json.dump(serialized_events, file)

def load_events():
    if not os.path.exists(PATH_EVENTS):
        return []

    with open(PATH_EVENTS, 'r') as file:
        return [ConcreteEvent(**event) for event in json.load(file)]


def list_events(events, is_active=None, is_upcoming=None, is_passed=None):
    filtered_events = events
    for event in events:
        print(event)
        
    if is_active is not None:
        filtered_events = [event for event in filtered_events if event.is_active() == is_active]

    if is_upcoming is not None:
        filtered_events = [event for event in filtered_events if event.is_upcoming() == is_upcoming]

    if is_passed is not None:
        filtered_events = [event for event in filtered_events if event.is_passed() == is_passed]
    
    if is_upcoming:
        current_date = datetime.now()
        upcoming_events = [event for event in events if event.event_datetime() >= current_date]
        upcoming_events.sort(key=lambda x: x.event_datetime())
        for event in upcoming_events:
            print(event)
    
    if is_passed:
        current_date = datetime.now()
        passed_events = [event for event in events if event.event_datetime() < current_date]
        passed_events.sort(key=lambda x: x.event_datetime())
        for event in passed_events:
            print(event)


def get_event_by_name(events, name):
    return next((event for event in events if event.name == name), None)


def get_event_by_user(events, user):
    user_events = []
    for event in events:
        if user in event.users:
            user_events.append(event)
    return user_events


def register_user(name, age, sex, cellphone, address):
    return User(name, age, sex, cellphone, address)


def register_event(name, address, price, category, hour, date, description):
    return ConcreteEvent(name, address, price, category, hour, date, description)

def list_user_events(events, user):
    user_events = get_event_by_user(events, user)
    for event in user_events:
        print(event)

# Main
def main():
    print("\n\nBem-vindo ao Sistema de Gerenciamento de Eventos!")

    events = load_events()
    current_user = None

    while True:
        print("\nMenu:")
        print("1. Cadastrar evento")
        print("2. Cadastrar usuário")
        print("3. Listar eventos")
        print("4. Listar eventos próximos")
        print("5. Listar eventos passados")
        print("6. Participar de evento")
        print("7. Cancelar participação de evento")
        print("8. Listar eventos do usuário")
        print("9. Sair")

        option = input("\nDigite o número da opção desejada: ")

        if option == '1':
            event = register_event(
                input("\nDigite o nome do evento: "),
                input("\nDigite o endereço do evento: "),
                float(input("\nDigite o preço do evento: ")),
                input("\nDigite a categoria do evento: "),
                input("\nDigite a hora de início do evento (formato: hh:mm): "),
                input("\nDigite a data do evento (formato: dd/mm/yyyy): "),
                input("\nDigite a descrição do evento: ")
            )
            events.append(event)
            save_events(events)
            print("\nEvento cadastrado com sucesso")

        elif option == '2':
            user = register_user(
                input("\nDigite o nome do usuário: "),
                int(input("\nDigite a idade do usuário: ")),
                input("\nDigite o sexo do usuário (M/F): "),
                input("\nDigite o celular do usuário: "),
                input("\nDigite o endereço do usuário: ")
            )
            current_user = user
            print("\nUsuário cadastrado com sucesso")

        elif option == '3':
            list_events(events)

        elif option == '4':
            list_events(events, is_upcoming=True)

        elif option == '5':
            list_events(events, is_passed=True)

        elif option == '6':
            if current_user is None:
                print("\nNenhum usuário logado")
            else:
                event_name = input("\nDigite o nome do evento que deseja participar: ")
                event = get_event_by_name(events, event_name)
        
                if event is None:
                    print("\nEvento não encontrado")
                else:
                    event.users.append(current_user)  # Adiciona o usuário à lista de usuários do evento
                    save_events(events)
                    print("\nParticipação registrada com sucesso")

        elif option == '7':
            if current_user is None:
                print("\nNenhum usuário logado")
            else:
                event_name = input("\nDigite o nome do evento que deseja cancelar a participação: ")
                event = get_event_by_name(events, event_name)
        
                if event is None:
                    print("\nEvento não encontrado")
                else:
                    if current_user in event.users:
                        event.users.remove(current_user)  # Remove o usuário da lista de usuários do evento
                        save_events(events)
                        print("\nParticipação cancelada com sucesso")
                    else:
                        print("\nVocê não está inscrito neste evento")

        elif option == '8':
            if current_user is None:
                print("\nNenhum usuário logado")
            else:
                list_user_events(events, current_user)


        elif option == '9':
            print("\nObrigado por usar o Sistema de Gerenciamento de eventos")
            break

        else:
            print("\nOpção inválida")
            
if __name__ == '__main__':
    main()
