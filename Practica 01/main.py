

def main():
    print("Practica 01 : Monitoreo con SNMP")
    menu()

def menu():
    she_love_you = True
    while she_love_you:
        print("1. Agregar agente. \n"
              "2. Eliminar agente.\n"
              "3. Estado de un agente. \n"
              "4. Graficas de agente.  \n"
              "5. Salir.\n")

        opt = int(input("> "))

        if opt == 1:
            ID_agent  = input("ID Agent:  ")
            hostname  = input("Hostname:  ")
            version   = input("Version:   ")
            port      = input("Port:      ")
            community = input("Community: ")

        elif opt == 2:
            ID_agent  = input("ID Agent:  ")

        elif opt == 3:
            ID_agent  = input("ID Agent:  ")

        elif opt == 4:
            print("Graficas")

        elif opt == 5:
            print("Cerrando gestor.")
            break;

main()
