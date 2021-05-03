from faker import Faker
from random import randint
from os.path import abspath

fake = Faker()


def generateFakeUsers():
    with open(abspath("./files/users_list.txt"), "w") as usersFile:
        for i in range(100):
            userId = randint(1, 1024)
            name = fake.name()
            user = name + "_" + str(userId)
            usersFile.write(user + "\n")
