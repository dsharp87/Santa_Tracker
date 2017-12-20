# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
import random
import argparse
from django.db import models

from ortools.constraint_solver import pywrapcp
# from ortools.constraint_solver import routing_enums_pb2

# Create your models here.
parser = argparse.ArgumentParser()
parser.add_argument('--tsp_size', default = 10, type = int,
                     help='Size of Traveling Salesman Problem instance.')
parser.add_argument('--tsp_use_random_matrix', default=True, type=bool,
                     help='Use random cost matrix.')
parser.add_argument('--tsp_random_forbidden_connections', default = 0,
                    type = int, help='Number of random forbidden connections.')
parser.add_argument('--tsp_random_seed', default = 0, type = int,
                    help = 'Random seed.')
parser.add_argument('--light_propagation', default = False,
                    type = bool, help = 'Use light propagation')




def distance(lat1, long1, lat2, long2):
    # Note: The formula used in this function is not exact, as it assumes
    # the Earth is a perfect sphere.

    # Mean radius of Earth in miles
    radius_earth = 3959

    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
    phi1 = lat1 * degrees_to_radians
    phi2 = lat2 * degrees_to_radians
    lambda1 = long1 * degrees_to_radians
    lambda2 = long2 * degrees_to_radians
    dphi = phi2 - phi1
    dlambda = lambda2 - lambda1

    a = haversine(dphi) + math.cos(phi1) * math.cos(phi2) * haversine(dlambda)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius_earth * c
    return d

def haversine(angle):
  h = math.sin(angle / 2) ** 2
  return h

#Distance callback

class CreateDistanceCallback(object):
    def __init__(self,city_coords):
        locations = city_coords
        size = len(locations)
        self.matrix = {}

        for from_node in xrange(size):
            self.matrix[from_node] = {}
            for to_node in xrange(size):
                if from_node == to_node:
                    self.matrix[from_node][to_node] = 0
                else:
                    x1 = locations[from_node][0]
                    y1 = locations[from_node][1]
                    x2 = locations[to_node][0]
                    y2 = locations[to_node][1]
                    self.matrix[from_node][to_node] = distance(x1,y1,x2,y2)
    
    def Distance(self, from_node, to_node):
        return int(self.matrix[from_node][to_node])


# Takes dictionary route_cities = {'start_city': NAME,
#                                   'city_names': [city1, city2, city3....],
#                                   'city_coords': [lat, long]}


def optimize_santa_route(route_cities):
    results = {
        'miles_traveled': 0,
        'travel_plan':[],
        'errors': "",
    }

    #break dictionary apart 
    city_names = route_cities['city_names']
    city_coords = route_cities['city_coords']
    start_city = route_cities['start_city']

    #Move start city to top of list
    start_city_index = city_names.index(start_city)
    temp_city = city_names[0]
    temp_coords = city_coords[0]
    city_names[0] = city_names[start_city_index]
    city_coords[0] = city_coords[start_city_index]
    city_names[start_city_index] = temp_city
    city_coords[start_city_index] = temp_coords
    print city_names
    print city_coords
    print '8'*100
    
    
    tsp_size = len(city_names)
    num_routes = 1
    depot = 0

    if tsp_size > 0:
        routing = pywrapcp.RoutingModel(tsp_size, num_routes, depot)
        search_parameters = pywrapcp.RoutingModel.DefaultRoutingSearchParameters()
    
        # Create the distance callback, which takes two arguments (the from and to node indices)
        # and returns the distance between these nodes.
        dist_between_nodes = CreateDistanceCallback(city_coords)
        dist_callback = dist_between_nodes.Distance
        routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
        # Solve, returns a solution if any.
        #assignment = routing.SolveWithParameters(search_parameters) # used in one google example
        assignment = routing.Solve()  #used in githug google OR example
  
        if assignment:
          # Solution cost.
          results['miles_traveled'] = str(assignment.ObjectiveValue()) + " miles\n"
          # Inspect solution.
          # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
          route_number = 0
          index = routing.Start(route_number) # Index of the variable for the starting node.
          route = ''
          while not routing.IsEnd(index):
            # Convert variable indices to node indices in the displayed route.
            next_city = {}
            next_city[city_names[routing.IndexToNode(index)]] = city_coords[routing.IndexToNode(index)]
            results['travel_plan'].append(next_city)
            
          #   route += str(city_names[routing.IndexToNode(index)]) + ' -> '
          #   index = assignment.Value(routing.NextVar(index))
          #   route += str(city_names[routing.IndexToNode(index)])
        else:
          results['errors'] = 'No solution found.'
    else:
        results['errors'] = 'Specify an instance greater than 0.'
    return results


# Takes dictionary route_cities = {'start_city': NAME,
#                                   'city_names': [city1, city2, city3....],
#                                   'city_coords': [lat, long]}
if __name__ == '__optimize_santa_route__':
  optimize_santa_route(parser.parse_args())

santa_test = {
    'start_city':'Vancouver',
    'city_names':['Seattle', 'Portland', 'Vancouver'],
    'city_coords':[[47.606649, -122.332070],[45.523289, -122.676449],[49.282889, -123.120736]]
}

outcome = optimize_santa_route(santa_test)
print outcome




