import pandas as pd
import geopandas as gpd
import numpy as np
import os
import sqlite3 as sl

class DataLoader():
    def __init__(self):
        self.census_heat_db_name = "census-heat.db"
        self.census_heat_csv_path = "..\\Data\\CensusHeatData.csv"
        self.db_name = "database.db"

        self.connection = sl.connect(self.db_name)
        if self.check_tables() == []:
            self.populate_db()


    def populate_db(self):
        # Create census heat table

        dataframe = pd.read_csv(self.census_heat_csv_path)
        dataframe.to_sql("CENSUSHEAT", self.connection)

    def check_tables(self):
        query = """SELECT name FROM sqlite_master WHERE type='table';"""
        with self.connection:
            tables = self.connection.execute(query)
            return tables.fetchall()
        
    def query(self, q):
        self.connection = sl.connect(self.db_name)
        with self.connection:
            data = self.connection.execute(q)
            return data.fetchall()
