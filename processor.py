from itertools import groupby
import fileinput


def process_journey_group(group):
    """
    Take a group of predictions for a single journey to a single stop on a
    single route and extract data from them
    """
    # sort the group from first to last
    l = list(group)
    l.sort(key=lambda row: row['time'])
    # if we don't have at least predictions, it isn't useful
    if len(l) < 2:
        return False
    # a place to store
    analysed = []
    # if the last prediction wasn't soon before arrival, it is no use
    if int(l[-1]['togo']) > 30:
        return False
    # when did it arrive?
    arrival = (int(float(l[-1]['time'])) +
               int(l[-1]['togo']))
    for prediction in l[:-1]:
        # for each predictions create a tuple: predicted time
        # and innaccuracy (inaccuracy based on prediction from
        # last time)
        time_made = int(float(prediction['time']))
        togo = int(prediction['togo'])
        analysed.append((togo, arrival - (time_made + togo)))

    return analysed


def process_route_group(group):
    """
    Take a group of of predictions for single route. Group into individual
    journeys to individual stops, and pass of for processing
    """
    # get each group of journeys to a stop and have at it
    stops = []
    for stop, stop_predicts in groupby(sorted(group,
                                       key=lambda x: x['stop']),
                                       lambda x: x['stop']):
        journeys = []

        for journey, journey_predicts in groupby(sorted(stop_predicts,
                                                 key=lambda x: x['trip']),
                                                 lambda x: x['trip']):
            journey_details = process_journey_group(journey_predicts)
            if journey_details:
                journeys.append((journey, journey_details))

        stops.append((stop, journeys))

    return stops


def process_predictions_list(l):
    results = []
    for route, route_predicts in groupby(sorted(l, key=lambda x: x['route']),
                                         lambda x: x['route']):
        results.append((route, process_route_group(route_predicts)))
    return results


preds = []

for line in fileinput.input():
    preds.append(eval(line))

results = process_predictions_list(preds)

for route in results:
    route_name = route[0]
    for stop in route[1]:
        stop_name = stop[0]
        for journey in stop[1]:
            journey_id = journey[0]
            for data_point in journey[1]:
                print route_name, stop_name, data_point[0], data_point[1]
