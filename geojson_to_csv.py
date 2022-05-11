import json
import csv
import sys
import os


dir_path = os.path.dirname(os.path.realpath(__file__))

def main(geojson_filename):
    """
    Converts GeoJSON to Csv
    :param geojson_filename: <string> The GeoJSON file to convert
    """

    geojson_file_path = os.path.join(dir_path, 'geojson', geojson_filename + '.geojson')
    geojson_file = open(geojson_file_path, 'r')

    geojson_file_string = geojson_file.readlines()

    if type(geojson_file_string) == list:
        string = ''.join(geojson_file_string)
    else:
        string = geojson_file_string

    string = string.replace("\n","")

    geojson_data = json.loads(string)

    if geojson_data['type'] == 'FeatureCollection':
        parse_feature_collection(geojson_data['features'], geojson_filename)
        print("File successfully converted")

    else:
        print("File is not a GeoJSON or doesn't have a FeatureCollections feature in the JSON structure.")


def parse_feature_collection(features, geojson_filename):
    """
    Converts GeoJSON to Csv
    :param features: <dict> The feature in the feature collection
    :param geojson_filename: <string> the original geojson filename
    """
    csv_file_path = os.path.join(dir_path, 'csv', geojson_filename + '.csv')

    with open(csv_file_path, 'w', newline="") as f:
        csvwriter = csv.writer(f, delimiter=',', lineterminator='\r\n', quotechar = '"')

        header = []
        for count, feature in enumerate(features):
            if count == 0:
                header = list(feature['properties'].keys())
                header.extend(['geometry'])
                csvwriter.writerow(header)
                count += 1
            csvwriter.writerow(feature_to_row(feature, feature['properties'].keys()))
        f.close()

def feature_to_row(feature, header):
    """
    Makes a list of values and the geometry string for each feature
    :param feature: <dict> The feature in the feature collection
    :param header: <list> the featrure header
    :return row_list: <list> a list of the feature properties and the geometry as a string
    """
    row_list = []
    geometry_string = ""

    for h in header:
        row_list.append(feature['properties'][h])
    if feature['geometry']['type'] not in ['Point', 'Polygon', 'MultiPolygon']:
        raise RuntimeError("Expecting point, polygon or multipolygon type, but got ", feature['geometry']['type'])

    coords = feature['geometry']['coordinates']


    if feature['geometry']['type'] == "Point":
        geometry_string += '{"type":"Point","coordinates":'
        geometry_string += str(coords)

    if feature['geometry']['type'] == "Polygon":
        geometry_string += '{"type":"Polygon","coordinates":'
        geometry_string += str(coords)

    if feature['geometry']['type'] == "MultiPolygon":
        geometry_string += '{"type":"MultiPolygon","coordinates":['
        for count, coord in enumerate(coords):
            if count != len(coords) - 1:
                geometry_string += str(coord) + ","
            else:
                geometry_string += str(coord) + "]"

    geometry_string += "}"

    row_list.extend([geometry_string])

    return row_list


if __name__ == "__main__":

    geojson_filename = sys.argv[1:]
    main(geojson_filename[0])