""" DataFrame Models (Pandera) for Raw Data """

import pandera as pa
from pandera.typing import Series


# @see https://pandera.readthedocs.io/en/stable/dataframe_models.html
class FlightsSchema(pa.DataFrameModel):
    latitude: Series[pa.Float]
    longitude: Series[pa.Float]
    id: Series[pa.String]
    icao_24bit: Series[pa.String]
    heading: Series[pa.Int]
    altitude: Series[pa.Int]
    ground_speed: Series[pa.Int]
    squawk: Series[pa.String]
    aircraft_code: Series[pa.String]
    registration: Series[pa.String]
    time: Series[pa.Int]
    origin_airport_iata: Series[pa.String]
    destination_airport_iata: Series[pa.String]
    number: Series[pa.String]
    airline_iata: Series[pa.String]
    on_ground: Series[pa.Int]
    vertical_speed: Series[pa.Int]
    callsign: Series[pa.String]
    airline_icao: Series[pa.String]
    requested_at: Series[pa.DateTime]

class AirportsSchema(pa.DataFrameModel):
    latitude: Series[pa.Float]
    longitude: Series[pa.Float]
    altitude: Series[pa.Int]
    name: Series[pa.String]
    icao: Series[pa.String]
    iata: Series[pa.String]
    country: Series[pa.String]
    requested_at: Series[pa.DateTime]