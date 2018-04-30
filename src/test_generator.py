# Generates tests of given size
# input: n - ilość punktów
# output: n krotek (skąd, dokąd, godzina odbioru, godzina dostawy)
# warunki:
#   - skąd, dokąd \in Warszawa
#   - t1, t2 \in [9; 21]
#   - abs(t1 - t2) >= 1h

import os
import csv
import argparse
import numpy as np

key = 'AIzaSyCvzPn7AMvM3Jd8EneaCAl5pOL94T341ww'


# Generate random iterators
def randomJob(addr_low, addr_high, time_low, time_high):
    j_s = np.random.randint(addr_low, addr_high)

    while True:
        j_e = np.random.randint(addr_low, addr_high)
        if j_s != j_e:
            break

    t_s = np.random.randint(time_low, time_high - 60 + 1)
    t_e = np.random.randint(t_s + 60, time_high + 1)

    return (j_s, j_e, t_s, t_e)


# Generate n jobs in form of tuple: (origin, destination, start_time, end_time)
def generateJobs(n, addresses, start_time_min, end_time_min):
    jobs = []

    for i in range(n):
        j_s, j_e, start_t, end_t = randomJob(1, len(addresses),
                                             start_time_min,
                                             end_time_min)

        jobs.append((addresses[j_s], addresses[j_e], start_t, end_t))

    return jobs


# Load addresses in Warsaw from .csv file
# Single address format: (dzielnica, ulica, nazwa skrócona ulicy, numer,
#   x, y, id punktu adresowego, kod pocztowy)
def loadAddresses(address_file):
    with open(address_file, 'r') as warsaw:
        next(warsaw)
        reader = csv.reader(warsaw, delimiter=';')
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
          % (printAddress(origin), printAddress(destin),
             start_t / 60, start_t % 60, end_t / 60, end_t % 60))


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
    parser = argparse.ArgumentParser(description='Generate test data.')
    parser.add_argument('--start_hour', type=int, default=9,
                        help='Earliest hour at which generated jobs can start')
    parser.add_argument('--end_hour', type=int, default=21,
                        help='Latest hour at which generated jobs can start')
    parser.add_argument('--address_file', type=str,
                        default='../data/raw/addresses_warsaw.csv',
                        help='File to path containing address data.')
    parser.add_argument('--output_dir', type=str, default="../data/test/",
                        help='Directory path at which tests will be saved.')
    parser.add_argument('--verbose', type=bool, default=False,
                        help='Print generated jobs to the standard output.')
    args = parser.parse_args()

    addresses = loadAddresses(args.address_file)
    START_TIME_MINUTES = args.start_hour * 60
    END_TIME_MINUTES = args.end_hour * 60

    j = 0
    while os.path.exists(args.output_dir + "test%s.csv" % j):
        j += 1

    while (True):
        n = int(input("Liczba zleceń: "))

        jobs = []
        jobs = generateJobs(n, addresses, START_TIME_MINUTES, END_TIME_MINUTES)
        qtuple = []

        for i in range(len(jobs)):
            if args.verbose:
                printJob(jobs[i])
            qtuple.append(toTuple(jobs[i]))

        with open(args.output_dir + '/test%s.csv' % j, 'w') as testfile:
            wr = csv.writer(testfile)
            for row in qtuple:
                wr.writerow(row)

        j = j + 1


if __name__ == '__main__':
    main()
