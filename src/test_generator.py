# Generates tests of given size
# input: n - ilość punktów
# output: n krotek (skąd, dokąd, godzina odbioru, godzina dostawy)
# warunki:
#   - skąd, dokąd \in Warszawa
#   - t1, t2 \in [9; 21]
#   - abs(t1 - t2) >= 1h

import numpy as np
import csv

key = 'AIzaSyCvzPn7AMvM3Jd8EneaCAl5pOL94T341ww'
START_TIME_MINUTES = 9  * 60
END_TIME_MINUTES   = 21 * 60
address_file = "../data/raw/addresses_warsaw.csv"

# Generate random iterators
def randomJob(addr_low, addr_high, time_low, time_high):
    j_s = np.random.randint(addr_low, addr_high + 1)

    # python's version of do...while - try to generate different address than starting one
    while True:
        j_e = np.random.randint(addr_low, addr_high + 1)
        if j_s != j_e:
            break

    t_s = np.random.randint(time_low, time_high - 60 + 1)
    t_e = np.random.randint(t_s + 60, time_high + 1)

    return (j_s, j_e, t_s, t_e)


# Generate n jobs in form of tuple: (origin, destination, start_time, end_time)
def generateJobs(n, addresses):
    jobs = []

    for i in range(n):
        j_s, j_e, start_t, end_t = randomJob(1, len(addresses), START_TIME_MINUTES, END_TIME_MINUTES)

        jobs.append((addresses[j_s], addresses[j_e], start_t, end_t))

    return jobs

# Load addresses in Warsaw from .csv file
# Single address format: (dzielnica, ulica, nazwa skrócona ulicy, numer, x, y, id punktu adresowego, kod pocztowy)
def loadAddresses():
    with open(address_file, 'r') as warsaw:
        next(warsaw)
        reader = csv.reader(warsaw, delimiter = ';')
        result = list(reader)
    return result

# Prints out address in format <street name> <street number>, Warszawa
def printAddress(address):
    result = "%s %s, Warszawa" % (address[2], address[3])
    return result

# Prints job with destination, origin, starting time and ending time
def printJob(job):
    origin, destin, start_t, end_t = job
    print("Z:  %s\n"
          "Do: %s\n"
          "Czas odbioru: %d.%02d\n"
          "Czas dostawy: %d.%02d\n"
          % (printAddress(origin), printAddress(destin), start_t / 60, start_t % 60, end_t / 60, end_t % 60))

# Packs jobs for Google Maps API: strings for destination and origin
def packJob(job):
    origin, destin, _, _ = job
    return (printAddress(origin), printAddress(destin))

# Pack into tuple
def toTuple(job):
    origin, destin, start_t, end_t = job
    return (printAddress(origin), printAddress(destin), start_t, end_t)

# Infinite loop
def main():
    addresses = loadAddresses()

    j = 0
    while (True):
        n = int(input("Liczba zleceń: "))

        jobs = []
        jobs = generateJobs(n, addresses)
        qtuple = []

        for i in range(len(jobs)):
            printJob(jobs[i])
            qtuple.append(toTuple(jobs[i]))

        with open('../data/test/test' + str(j) + '.csv', 'w') as testfile:
            wr = csv.writer(testfile)
            for row in qtuple:
                wr.writerow(row)

        j = j + 1

if __name__ == '__main__':
    main()
