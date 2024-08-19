DROP TABLE IF EXISTS weather_data;

CREATE TABLE weather_data (
    stn_id INTEGER NOT NULL,                    -- Station ID
    stn_name TEXT NOT NULL,                     -- Station Name
    cimiss_region TEXT NOT NULL,                -- CIMIS Region
    date DATE NOT NULL,                         -- Date
    jul INTEGER NOT NULL,                       -- Julian Day
    eto_in REAL NOT NULL,                       -- ETo (inches)
    precip_in REAL NOT NULL,                    -- Precipitation (inches)
    sol_rad REAL NOT NULL,                      -- Solar Radiation (Ly/day)
    avg_vap_pres REAL NOT NULL,                 -- Average Vapor Pressure (mBars)
    max_air_temp REAL NOT NULL,                 -- Maximum Air Temperature (F)
    min_air_temp REAL NOT NULL,                 -- Minimum Air Temperature (F)
    avg_air_temp REAL NOT NULL,                 -- Average Air Temperature (F)
    max_rel_hum REAL NOT NULL,                  -- Maximum Relative Humidity (%)
    min_rel_hum REAL NOT NULL,                  -- Minimum Relative Humidity (%)
    avg_rel_hum REAL NOT NULL,                  -- Average Relative Humidity (%)
    dew_point REAL NOT NULL,                    -- Dew Point (F)
    avg_wind_speed REAL NOT NULL,               -- Average Wind Speed (mph)
    wind_run REAL NOT NULL,                     -- Wind Run (miles)
    avg_soil_temp REAL NOT NULL,                -- Average Soil Temperature (F)
    PRIMARY KEY (stn_id, date)                  -- Primary Key constraint
);
