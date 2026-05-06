"""
Physical Constants for Lunar Solar Simulator
All values are based on real-world physics and astronomy.
"""

# Solar Constants
SOLAR_CONSTANT = 1361  # W/m² (solar irradiance at 1 AU)
SOLAR_CONSTANT_MOON = 1361  # Same as Earth (Moon is at same distance from Sun)

# Moon Physical Properties
MOON_RADIUS_KM = 1737.4  # Mean radius in kilometers
MOON_CIRCUMFERENCE_KM = 10921  # Equatorial circumference
MOON_SURFACE_AREA_KM2 = 37930000  # Total surface area

# Earth-Moon System
EARTH_MOON_DISTANCE_KM = 384400  # Mean distance
EARTH_MOON_PERIGEE_KM = 356500  # Closest approach
EARTH_MOON_APOGEE_KM = 406700   # Farthest distance

# Lunar Orbital/Rotational Periods
LUNAR_DAY_HOURS = 708  # ~29.5 Earth days (synodic period)
LUNAR_ORBITAL_PERIOD_HOURS = 655.7  # ~27.3 Earth days (sidereal period)

# Transmission Loss Factors
MICROWAVE_BASE_LOSS = 0.15  # 15% base loss for microwave transmission
LASER_BASE_LOSS = 0.30      # 30% base loss for laser transmission
ATMOSPHERIC_LOSS = 0.10     # 10% atmospheric absorption (clear conditions)

# Weather Impact Factors
WEATHER_CLEAR = 1.0
WEATHER_PARTLY_CLOUDY = 0.85
WEATHER_CLOUDY = 0.6
WEATHER_RAIN = 0.4
WEATHER_HEAVY_RAIN = 0.2

# Panel Properties
PANEL_DEGRADATION = 0.98    # 2% initial degradation factor
PANEL_TEMP_COEFFICIENT = -0.004  # -0.4% efficiency per degree C above 25°C
PANEL_MAX_TEMP_C = 80       # Maximum panel temperature in full sun
PANEL_MIN_TEMP_C = -40      # Minimum operating temperature

# Degradation Rates
ANNUAL_DEGRADATION_RATE = 0.025  # 2.5% per year in space

# Rectenna (Receiving Antenna) Properties
RECTENNA_EFFICIENCY = 0.85  # 85% conversion efficiency
RECTENNA_DIAMETER_KM = 10   # Typical rectenna diameter

# Transmission Frequencies
MICROWAVE_FREQUENCY_GHZ = 2.45  # ISM band frequency
MICROWAVE_WAVELENGTH_M = 0.122  # ~12.2 cm
LASER_WAVELENGTH_M = 1e-6       # 1 micron infrared

# Earth Atmosphere
EARTH_ATMOSPHERE_HEIGHT_KM = 100  # Karman line
SEA_LEVEL_PRESSURE_PA = 101325
ATMOSPHERIC_SCALE_HEIGHT_KM = 8.5

# Energy Conversion
WATTS_TO_GW = 1e-9
GW_TO_WATTS = 1e9
KM2_TO_M2 = 1e6
