help_text = "/help - вывести справку\n/time - запросить свободное время на ремонт\n/status - запросить статус гтовности автомобиля\n/parts - раздел запчастей"

start_text = "Добро пожаловать в telegram bot нашего автосервиса!\nВведите /help для вызова справки"

free_time = "На сегодня, 15.05.2017 свободно:\n"

code_word = "777"

class simpleTime:
    def __init__(self, h, m):
        self.h = h
        self.m = m
        self.data = h+":"+m

time = []
time.append(simpleTime("11","00"))
time.append(simpleTime("14","00"))
time.append(simpleTime("17","00"))
