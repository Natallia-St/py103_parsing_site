import csv
import json

with open('cars_info.json', encoding='UTF-8', ) as file:
    data = json.load(file)
print(data)


workFile = open("cars_info.csv", encoding="UTF-8")
workReader = csv.reader(workFile, delimiter=";")
workData = list(workReader)
print(workData)
workFile.close()
