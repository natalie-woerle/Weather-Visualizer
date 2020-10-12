import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime
import os
import csv

class WeatherParser:
    def __init__(self):
        self.link = "https://www.wetterdienst.de/Deutschlandwetter/Wetterstationen"
        self.website = BS(requests.get(self.link).text, "html.parser")
        self.relevant_times = ["05:00","12:00","18:00", "00:00"]
        self.relevant_stations = ["Augsburg",
                                 "Fürstenzell",
                                 "Illesheim",
                                 "Kempten",
                                 "Lechfeld",
                                 "Rosenheim"]
        self.data_list = []
        self.csv_directory = os.path.join(os.getcwd(),'csv')
        if not os.path.exists(self.csv_directory):
            os.mkdir(self.csv_directory)
        self.curr_date = datetime.now().strftime('%d.%m.%Y')
        self.filename = f"{self.curr_date}.csv"

    # parse website, create sublists [station, temperature, time] in data_list

    def parse_website(self):
        table_rows = [row.text.split("\n") for row in self.website.select("tbody tr.BY")]
        for row in table_rows:
            row = row[1:]  #remove empty [0]
            row[0] = row[0].strip()  #remove whitespace around stat
            
            if row[0] in self.relevant_stations:
                if row[0] == "Illesheim":
                    row[2] = row[2].replace("°C","").strip()  #format temp
                    formatted_data = [row[0],row[2],row[8]]
                else:
                    row[1] = row[1].replace("°C","").strip()  
                    formatted_data = [row[0],row[1],row[7]]

                self.data_list.append(formatted_data)

    def write_to_csv(self,csv_file):
        for station, temperature, timestamp in self.data_list:
            new_row = f"{timestamp};{station};{temperature}\n"
            csv_file.write(new_row)

    def timestamp_is_duplicate(self):
        if os.path.isfile(self.csv_directory + self.filename) and self.data_list != []:
            current_timestamp = self.data_list[0][2]
            with open (self.filename, "r", encoding="UTF-8") as csv_file:
                reader = csv.reader(csv_file, delimiter=";")
                for row in reader:
                    if current_timestamp in row:
                        print(f"Error: Timestamp \"{current_timestamp}\" already exists in \"{self.filename}\".")
                        return True
        return False

        
    #---- create/append to csv file (station,temperature,time) ----#                 
            
    def create_csv(self):
        os.chdir(self.csv_directory)
        self.parse_website()
                
        if not self.timestamp_is_duplicate():
            try:
                with open (self.filename, "a+", newline="", encoding="UTF-8") as csv_file:
                    self.write_to_csv(csv_file)
                    print(f"\"{self.filename}\" updated successfully")
            except PermissionError:
                print(f"Error: Access denied, close \"{self.filename}\" and try again.")
                
        elif self.data_list == []:
            print("Error: No data. Check website.")

# order of operations:
# get website -> parse website -> append data from table rows on website to data_list -> open csv file in read mode (if existing) -> 
# check if entry for timestamp already exists -> if no -> open file in append mode -> write data from data_list to file