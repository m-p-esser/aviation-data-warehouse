""" DataFrame Models (Pandera) for Raw Data """

import pandera as pa
from pandera.typing import Series


# @see https://pandera.readthedocs.io/en/stable/dataframe_models.html
class FlightsSchema(pa.DataFrameModel):
    latitude: Series[
        pa.Float
    ]  # = pa.Field(in_range={"min_value": -180, "max_value": 180})
    longitude: Series[
        pa.Float
    ]  # = pa.Field(in_range={"min_value": -180, "max_value": 180})
    id: Series[pa.String] = pa.Field(unique=True)
    icao_24bit: Series[pa.String]
    heading: Series[pa.String]
    altitude: Series[pa.String]
    ground_speed: Series[pa.String]
    squawk: Series[pa.String]
    aircraft_code: Series[pa.String]
    registration: Series[pa.String]
    time: Series[pa.String]
    origin_airport_iata: Series[pa.String]
    destination_airport_iata: Series[pa.String]
    number: Series[pa.String]
    airline_iata: Series[pa.String]
    on_ground: Series[pa.Int] = pa.Field(isin=[0, 1])
    requested_at: Series[pa.DateTime]
