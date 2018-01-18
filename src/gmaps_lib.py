import googlemaps
import csv
from datetime import datetime, date

key = 'AIzaSyCvzPn7AMvM3Jd8EneaCAl5pOL94T341ww'
gmaps = googlemaps.Client(key=key)

# Distance of a given route
def distance(route):
    return route['legs'][0]['distance']['value']

# Time spent in traffic
def duration_in_traffic(route):
    return int(route['legs'][0]['duration_in_traffic']['value'])

# Prints duration (in minutes) in format HH:MM:SS
def printDuration(duration):
    m, s = divmod(duration, 60)
    h, m = divmod(m, 60)
    return ("%02d:%02d:%02d" % (h, m, s))

# Returns default route between origin and destination, departing at dep_time (minutes into day)
def route(origin, destination, dep_time, client=gmaps):
    dep_time = int(dep_time)
    today = date.today()
    departure = datetime( today.year, today.month, today.day + 1, int(dep_time / 60), dep_time % 60)
    routes = client.directions(origin, destination, departure_time=departure)

    # Assumes only one route
    return routes[0]

# Loads test of a given number
def loadTest(number):
    with open('test' + str(number) + '.csv') as testfile:
        reader = csv.reader(testfile, delimiter=',')
        test = list(reader)

    return test

def main():
    n = int(input("Number of test to load:"))

    test = loadTest(n)

    for row in test:
        orig, dest, start_t, end_t = row

        r = route(orig, dest, start_t)
        dist = distance(r)
        dur  = duration_in_traffic(r)

        print("From:     %s\n"
              "To:       %s\n"
              "Distance: %d m\n"
              "Time:     %s\n" % (orig, dest, dist, printDuration(dur)))

if __name__ == '__main__':
    main()
