# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 09:42:09 2022

@author: iaala
"""

import requests
import sql_configs
import datetime
import os
from bs4 import BeautifulSoup
import time

from find_tables import (
    table_information_one,
    table_information_two,
    table_information_three,
    table_information_four,
)
from create_connection import create_sql_connection
import columns


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def main():
    for ppin in range(200001, 18600, -1):
        try:
            conn = create_sql_connection(
                    user=sql_configs.USER,
                    password=sql_configs.PASSWORD,
                    host=sql_configs.HOST,
                    database=sql_configs.DATABASE,
                )
            temp_dict = dict()

            print(ppin)
            with open(os.path.join(__location__, 'status.txt'), 'w') as f:
                f.write(f"currently starting {ppin}")
            c = conn.cursor()
            c.execute('select pin from parcel;')
            items_collected = [int(''.join(map(str, item))) for item in c.fetchall()]
            if ppin not in items_collected:
                url = f"https://madisonproperty.countygovservices.com/Property/Property/Summary?taxyear=2022&ppin={ppin}"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"
                }
                resp = requests.get(url, headers=headers)
                time.sleep(0.25)
                soup = BeautifulSoup(resp.text, "html.parser")
                parcel_info = table_information_one(soup, "collapseParcelInfo")
                if parcel_info == {}:
                    parcel_info = {column: "" for column in columns.PARCEL_INFO_COLUMNS}
                parcel_info['PIN']= ppin
                property_values = table_information_one(soup, "collapseSummaryPropertyValues")
                if property_values == {}:
                    property_values = {column: "" for column in columns.PROPERTY_COLUMNS}
                subdivision = table_information_one(soup, "collapseSummarySubdivision")
                if subdivision == {}:
                    subdivision = {column: "" for column in columns.SUBDIVISION_COLUMNS}
                tax = table_information_two(soup, "collapseTaxInfo")
                if tax == {}:
                    tax = {column: "" for column in columns.TAX_COLUMNS}
                tax_history = table_information_three(soup, "collapseTaxHistory")
                details = table_information_three(soup, "collapseSummaryDetailInfo")

                building_components = table_information_four(
                    soup, "collapseSummaryBuildingComponents"
                )
                improvement = building_components.get("improvement")
                computations = building_components.get("computations")
                materials = building_components.get("materials")

                gis_url = f"https://isv.kcsgis.com/al.Madison_revenue/?fips={ppin}"

                temp_dict[ppin] = {
                    "ppin": ppin,
                    "date": str(datetime.datetime.now()),
                    "parcel": parcel_info,
                    "property_values": property_values,
                    "subdivision": subdivision,
                    "tax": tax,
                    "tax_history": tax_history,
                    "details": details,
                    "improvement": improvement,
                    "computations": computations,
                    "materials": materials,
                    "gis_url": f"https://isv.kcsgis.com/al.Madison_revenue/?fips={ppin}",
                }
                ppin = [ppin]
                conn = create_sql_connection(
                    user=configs.USER,
                    password=configs.PASSWORD,
                    host=configs.HOST,
                    database=configs.DATABASE,
                )
                c = conn.cursor()
                date = [str(datetime.datetime.now())]
                parcel_values = list(parcel_info.values()) + date
                c.execute(configs.PARCEL_STATEMENT, parcel_values)

                property_values = list(property_values.values()) + date + ppin
                c.execute(configs.PROPERTY_VALUES_STATEMENT, property_values)

                subdivision_values = list(subdivision.values()) + date + ppin
                c.execute(configs.SUBDIVISION_STATEMENT, subdivision_values)

                tax_values = [str(item) for item in tax.values()] + date + ppin
                tax_values = tuple(tax_values)
                c.execute(configs.TAX_STATEMENT, tax_values)

                for row in zip(*list(tax_history.values())):
                    c.execute(configs.TAX_HISTORY_STATEMENT, row + tuple(date) + tuple(ppin))
                for row in zip(*list(details.values())):
                    c.execute(configs.DETAILS_STATEMENT, row + tuple(date)+ tuple(ppin))
                improvement_values = list(improvement.values()) + date + ppin
                improvement_values = tuple(improvement_values)
                c.execute(configs.IMPROVEMENTS_STATEMENT, improvement_values)

                computations_values = list(computations.values()) + date + ppin
                computations_values = tuple(computations_values)
                c.execute(configs.COMPUTATION_STATEMENT, computations_values)

                for row in zip(*list(materials.values())):
                    row_length = len(row)
                    if row_length != 0:
                        c.execute(configs.MATERIALS_STATEMENT, row + tuple(date)+ tuple(ppin))
                urls_values = (url, gis_url) + tuple(date) + tuple(ppin)
                c.execute(configs.URLS_STATEMENT, urls_values)


                conn.commit()
        except Exception as e:
#            raise Exception
            new_line = '\n'
            if isinstance(ppin, int):
                ppin = [ppin]
            with open(os.path.join(__location__, 'errors.txt'), 'a') as f:
                f.write(f"error in {ppin[0]} occurred. error was {e}{new_line}")

if __name__ == "__main__":
    main()
