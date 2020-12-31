import dataclasses
import datetime
import math

from dateutil import tz


HOURS_PER_DEGREE = 24 / 360
HOURS_PER_RADIAN = 12 / math.pi
ONE_HOUR = datetime.timedelta(hours=1)
RADIANS_PER_CYCLE = 2 * math.pi


DEFAULT_LATITUDE = 37.871667
DEFAULT_LONGITUDE = -122.272778
DEFAULT_TIMEZONE_NAME = "America/Los_Angeles"


@dataclasses.dataclass
class SunRiseAndSet:

    current_timestamp: float
    latitude: float
    longitude: float
    solar_noon: datetime.datetime
    sunlight_hours: float
    sunrise: datetime.datetime
    sunset: datetime.datetime
    timezone_name: str

    @staticmethod
    def get_year_fraction(dt: datetime.datetime) -> float:
        start = datetime.datetime(dt.year, 1, 1)
        finish = datetime.datetime(start.year + 1, 1, 1)
        return (dt - start) / (finish - start)

    @staticmethod
    def get_equation_of_time_minutes(year_fraction: float) -> float:
        year_radians = year_fraction * RADIANS_PER_CYCLE
        return 229.18 * (
            + 0.000075
            + 0.001868 * math.cos(year_radians)
            - 0.032077 * math.sin(year_radians)
            - 0.014615 * math.cos(2 * year_radians)
            - 0.040849 * math.sin(2 * year_radians)
        )

    @staticmethod
    def get_solar_declination_radians(year_fraction: float) -> float:
        year_radians = year_fraction * RADIANS_PER_CYCLE
        return (
            + 0.006918
            - 0.399912 * math.cos(year_radians)
            + 0.070257 * math.sin(year_radians)
            - 0.006758 * math.cos(2 * year_radians)
            + 0.000907 * math.sin(2 * year_radians)
            - 0.002697 * math.cos(3 * year_radians)
            + 0.001480 * math.sin(3 * year_radians)
        )

    @staticmethod
    def get_hour_angle_hours(
        latitude: float,
        solar_declination_radians: float,
    ) -> float:
        latitude_radians = latitude * math.pi / 180
        zenith_radians = 90.833 * math.pi / 180
        hour_angle_radians = math.acos(
            math.cos(zenith_radians) / math.cos(latitude_radians) / math.cos(solar_declination_radians)
            - math.tan(latitude_radians) * math.tan(solar_declination_radians)
        )
        return hour_angle_radians * HOURS_PER_RADIAN

    @classmethod
    def from_theory(
        cls,
        current_timestamp: float,
        latitude: float,
        longitude: float,
        timezone_name: str,
    ):
        # Rehasing of https://www.esrl.noaa.gov/gmd/grad/solcalc/solareqns.PDF
        dt = datetime.datetime.fromtimestamp(current_timestamp)
        year_fraction = cls.get_year_fraction(dt=dt)

        equation_of_time_minutes = cls.get_equation_of_time_minutes(year_fraction=year_fraction)

        local_timezone = tz.gettz(timezone_name)
        utc_offset_hours = dt.astimezone(local_timezone).utcoffset() / ONE_HOUR
        solar_noon = (
            # Noon today
            datetime.datetime(dt.year, dt.month, dt.day, 12)
            # Equation of time offset
            + datetime.timedelta(minutes=-equation_of_time_minutes)
            # Longitude physical offset
            + datetime.timedelta(hours=HOURS_PER_DEGREE * -longitude)
            # Longitude timezone offset
            + datetime.timedelta(hours=utc_offset_hours)
        )

        solar_declination_radians = cls.get_solar_declination_radians(year_fraction=year_fraction)

        hour_angle_hours = cls.get_hour_angle_hours(
            latitude=latitude,
            solar_declination_radians=solar_declination_radians,
        )
        return cls(
            current_timestamp=current_timestamp,
            longitude=longitude,
            latitude=latitude,
            solar_noon=solar_noon,
            sunlight_hours=(hour_angle_hours * 2),
            sunrise=(solar_noon - datetime.timedelta(hours=hour_angle_hours)),
            sunset=(solar_noon + datetime.timedelta(hours=hour_angle_hours)),
            timezone_name=timezone_name,
        )


def sun_rise_and_set(
    current_timestamp: float = datetime.datetime.now().timestamp(),
    latitude: float = DEFAULT_LATITUDE,
    longitude: float = DEFAULT_LONGITUDE,
    timezone_name: str = DEFAULT_TIMEZONE_NAME,
):
    return dataclasses.asdict(SunRiseAndSet.from_theory(**locals()))
