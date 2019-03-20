import re
from bs4 import BeautifulSoup
from bs4 import Comment
def xmlToFile(path_xml, name_xml, path_file, name_file):
    xml_file = open(path_xml + name_xml, "r")
    xml_string = xml_file.read()

    bs_s = BeautifulSoup(xml_string, "lxml")
    values = bs_s.find_all("v")
    #print(values)

    comments = bs_s.find_all(string = lambda text: isinstance(text, Comment))
    time_stamps = []

    for c in comments:
        current = c.split(" ")
        if len(current) == 7:
            time_stamps.append(float(current[-2]))
    values_float = []
    series = [i for i in range(0, len(time_stamps))]

    for val in values:
        values_float.append(float(val.string))

    txt_file = open(path_file + name_file, "w")
    for i in range(0, len(time_stamps)):
        txt_file.write(str(time_stamps[i]) + " " + str(values_float[i]) + " " + str(series[i]) + "\n")
    txt_file.close()
    xml_file.close()

'''
if __name__ == "__main__":
    xmlToFile("/home/linuxsnmp/Escritorio/Network-Services-Administration/redes3fix/Pract1/", "Prac1.xml",
                     "/home/linuxsnmp/Escritorio/Network-Services-Administration/redes3fix/Pract1/", "text_file.txt")
'''