import requests
from bs4 import BeautifulSoup
import xlrd
from datetime import datetime
def findTeacher(name):
    page = requests.get("https://www.mirea.ru/schedule/")
    soup = BeautifulSoup(page.text, "html.parser")
    hrefs = soup.find_all('a', {"class": "uk-link-toggle"})
    result = []
    for links in hrefs:
        link = links.get("href")
        if "ИИТ_" in link and "зач_" not in link and "экз_" not in link:
            result.append(link)
    dictionary = {}
    cours = 0
    for j in result:
        resp = requests.get(j)
        f = open("file.xlsx", "wb")
        f.write(resp.content)
        f.close()
        book = xlrd.open_workbook("file.xlsx")
        sheet = book.sheet_by_index(0)
        num_cols = sheet.ncols
        num_rows = sheet.nrows
        sheet = book.sheet_by_index(0)
        num_cols = sheet.ncols
        num_rows = sheet.nrows
        stolb = 7
        strok = 3
        while stolb < num_cols:
            while strok < 75:
                if sheet.cell(strok, stolb).value == "":
                    strok += 1
                    continue
                if str(sheet.cell(strok, stolb).value)[0].isdigit():
                    strok += 1
                    continue
                if name in sheet.cell(strok, stolb).value:
                    if len(sheet.cell(strok, stolb).value.split()) > 2:
                        find = sheet.cell(strok, stolb).value.split()
                        iterator = 0
                        while iterator < len(find):
                            if find[iterator] == name:
                                if "\n" in find[iterator]:
                                    find[iterator] = find[iterator].replace("\n", "")
                                if len(find[iterator + 1]) > 4:
                                    for each in range(len(find[iterator + 1])):
                                        if find[iterator + 1][each] == ".":
                                            if find[iterator + 1][each + 1] == ".":
                                                find[iterator + 1] = find[iterator + 1][:each + 1] + find[iterator + 1][
                                                                                                     each + 2:]
                                                break
                                if len(find[iterator + 1]) > 4:
                                    for each in range(len(find[iterator + 1])):
                                        if find[iterator + 1][each] == ".":
                                            if find[iterator + 1][each + 2] == ".":
                                                find[iterator + 2] = find[iterator + 1][each + 3:] + " " + find[
                                                    iterator + 2]
                                                find[iterator + 1] = find[iterator + 1][:each + 2]
                                                break
                                if find[iterator + 1][2] == ".":
                                    find[iterator + 1] = find[iterator + 1][:2] + find[iterator + 1][3:]
                                if find[iterator + 1][-1] != ".":
                                    find[iterator + 1] += "."
                                if find[iterator] + " " + find[iterator + 1] not in dictionary:
                                    dictionary[find[iterator] + " " + find[iterator + 1]] = [cours]
                                else:
                                    if cours not in dictionary[find[iterator] + " " + find[iterator + 1]]:
                                        dictionary[find[iterator] + " " + find[iterator + 1]].append(cours)
                            iterator += 2
                        strok += 1
                        continue
                    teacher = sheet.cell(strok, stolb).value
                    teacher = teacher.replace("\n", "")
                    if name == teacher.split()[0]:
                        if teacher not in dictionary:
                            dictionary[teacher] = [cours]
                            strok += 1
                            continue
                        else:
                            if cours not in dictionary[teacher]:
                                dictionary[teacher].append(cours)
                            strok += 1
                            continue
                strok += 1
            strok = 3
            stolb += 5
            if stolb > num_cols:
                break
            if sheet.cell(2, stolb).value == "Нач.\nзанятий":
                stolb += 5
        cours += 1
    return dictionary