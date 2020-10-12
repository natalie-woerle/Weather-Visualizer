from parse_web import WeatherParser
import os
import random
from datetime import datetime,date

parser = WeatherParser()

def generate_sample():
    os.chdir(parser.csv_directory)
    
    start_dt = date.today().replace(day=1, month=1).toordinal()
    end_dt = date.today().toordinal()
    random_day = date.fromordinal(random.randint(start_dt, end_dt))
    filename = datetime.strftime(random_day,"%d.%m.%Y.csv")
    
    with open(filename, "a+", encoding="UTF-8") as file:
        for rel_time in parser.relevant_times:
            for station in parser.relevant_stations:
                temp = round(random.uniform(10, 25),1)
                file.write(f"{rel_time};{station};{temp}\n")