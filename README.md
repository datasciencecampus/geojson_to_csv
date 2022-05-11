A simple script for parsing geojson files and converting them to CSV files ready to upload to GCP BigQuery.

Add you `.geojson` file to the `/geojson` folder. Then specify the name of the file as a command line argument when calling the script, e.g.:

`python geojson_to_csv.py <name_of_file>`

This will then convert the file to a CSV file and save to the `/csv` folder.A

This will convert POINT, POLYGON and MULTIPOLYGON feature types.

Once uploaded, you can then convert the GeoJSON field to GEOGRAPHY using:

```
select *,
ST_GEOGFROMGEOJSON(geometry, make_valid => TRUE)
from `kpi.uk_regions`
```