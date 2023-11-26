""" DataFrame Models (Pandera) for Raw Data """

import pandera as pa
from pandera.typing import Series


class FlightsSchema(pa.DataFrameModel):
    latitude: Series[
        float
    ]  # = pa.Field(in_range={"min_value": -180, "max_value": 180})
    longitude: Series[
        float
    ]  # = pa.Field(in_range={"min_value": -180, "max_value": 180})
    id: Series[str] = pa.Field(unique=True)
    icao_24bit: Series[str]
    heading: Series[int]
    altitude: Series[int]
    ground_speed: Series[int]
    squawk: Series[str]
    aircraft_code: Series[str]
    registration: Series[str]
    time: Series[int]
    origin_airport_iata: Series[str]
    destination_airport_iata: Series[str]
    number: Series[str]
    airline_iata: Series[str]
    on_ground: Series[int] = pa.Field(isin=[0, 1])
