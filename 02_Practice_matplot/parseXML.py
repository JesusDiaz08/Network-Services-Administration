import re
def getXMlDataToFile(path_xml, name_xml, path_file, name_file):
    # parser xml databse to txt
    xml_file = open(path_xml + name_xml, "r")

    for line in xml_file:
        r = re.search(".</*database>", line)
        print(r)
if __name__ == "__main__":
    getXMlDataToFile("/home/linuxsnmp/Escritorio/Network-Services-Administration/redes3fix/Pract1/", "Prac1.xml",
                     "/home/linuxsnmp/Escritorio/Network-Services-Administration/redes3fix/Pract1", "text_file.txt")
