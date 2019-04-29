import sys


def read_file():
    # if len(sys.argv) == 3:
    #     print('Argumenty ok, vstupny subor:', str(sys.argv[1]), ', nka vysledny:', str(sys.argv[2]))
    # else:
    #     print('Chyba nespravne spustenie skriptu: zadajte interpreter "meno suboru na konverziu" "meno vystupneho '
    #           'suboru"')
    #     sys.exit()

    # filename = str(sys.argv[1])
    filename = 'regex2.txt'
    file = open(filename, 'r')
    filecontent = file.read().splitlines()
    file.close()
    return filecontent


def write_nka_to_file(result):
    # zapis vystupu
    filename = str(sys.argv[2])
    file = open(filename, 'w')
    file.write(result)
    file.close()


# def write_dka_to_file(result):
#     # zapis vystupu
#     filename = str(sys.argv[3])
#     file = open(filename, 'w')
#     file.write(result)
#     file.close()
