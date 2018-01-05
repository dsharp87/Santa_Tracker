# import doctest, 
import math

# from itertools import permutations


def distance(coord_1, coord_2):
    lat1 = coord_1[0]
    long1 = coord_1[1]
    lat2 = coord_2[0]
    long2 = coord_2[1]
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

def shortest_dist_tsp(city_coords, city_names):
    # output dictionary
    results = {
        'miles_traveled': 0,
        'travel_plan':[],
    }

    # initial entry into dictionary (this will be start city)
    new_city = {
        'name': city_names[0],
        'coords': city_coords[0]
        }
    
    # add new city to outdictionary
    results['travel_plan'].append(new_city)
    # not sure what this does yet
    path_coords = [city_coords[0]]
    city_coords.remove(city_coords[0])
    city_names.remove(city_names[0])

    print 'before while loop'
    print results
    print 'city coords'
    print city_coords
    print 'city names'
    print city_names
    print '8'*50
    while city_coords:
        #Find closest coordinate using distance function defined above
        nearest = min(city_coords, key=lambda x: distance(path_coords[-1], x))
        city_index = city_coords.index(nearest)
        
        #add to dictionary
        new_city = {
            'name':city_names[city_index],
            'coords':city_coords[city_index]
        }
        
        # put new city into results dictionary
        results['travel_plan'].append(new_city)
        # put new coords onto end of path list
        path_coords.append(nearest)
        results['miles_traveled'] += distance(path_coords[-2], path_coords[-1])
        
        #remove nearest city from both lists
        city_coords.remove(nearest)
        city_names.remove(city_names[city_index])

    # results = {
    #     'miles_traveled': 0,
    #     'travel_plan':[{name:city_name, coords:[xx.xxx, xx.xxxx]}, {name:city_name, coords:[xx.xxx, xx.xxxx]}, {name:city_name, coords:[xx.xxx, xx.xxxx]}],
    # }
    # this is returned back to optimized_santa_route (miles travled and travel plan list of dictionaries)
    return results

# Input dictionary route_cities = {
#                                   'city_names'=[seattle, vancouver, ....]
#                                   'city_coords'= [[lat long], [lat long]...]
#                                   'start_city' = 'SOME CITY'
#                                   }
def optimized_santa_route(route_cities):
    #break dictionary apart to be passed into shortest_dist_tsp function
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
    
    # call tsp function and pass results back to views file
    # results = {
    #     'miles_traveled': 0,
    #     'travel_plan':[{name:city_name, coords:[xx.xxx, xx.xxxx]}, {name:city_name, coords:[xx.xxx, xx.xxxx]}, {name:city_name, coords:[xx.xxx, xx.xxxx]}],
    # }
    # this is returned back to optimized_santa_route (miles travled and travel plan list of dictionaries)
    return shortest_dist_tsp(city_coords, city_names)
    
# santa_test = {
#     'start_city':'Vancouver',
#     'city_names':['Seattle', 'Portland', 'Vancouver'],
#     'city_coords':[[47.606649, -122.332070],[45.523289, -122.676449],[49.282889, -123.120736]]
# }

# outcome = optimized_santa_route(santa_test)
# print outcome

