# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 09:42:09 2022

@author: iaala
"""

import requests
import configs
import datetime
from bs4 import BeautifulSoup
import time

from find_tables import (
    table_information_one,
    table_information_two,
    table_information_three,
    table_information_four,
)
from create_connection import create_sql_connection


def main():

    temp_dict = dict()
    for ppin in range(1, 2):
        url = f"https://madisonproperty.countygovservices.com/Property/Property/Summary?taxyear=2022&ppin={ppin}"
        resp = requests.get(url)
        time.sleep(0.5)
        soup = BeautifulSoup(resp.text, "html.parser")
        parcel_info = table_information_one(soup, "collapseParcelInfo")
        property_values = table_information_one(soup, "collapseSummaryPropertyValues")
        subdivision = table_information_one(soup, "collapseSummarySubdivision")

        tax = table_information_two(soup, "collapseTaxInfo")

        tax_history = table_information_three(soup, "collapseTaxHistory")
        details = table_information_three(soup, "collapseSummaryDetailInfo")

        building_components = table_information_four(
            soup, "collapseSummaryBuildingComponents"
        )
        improvement = building_components.get("improvement")
        computations = building_components.get("computations")
        materials = building_components.get("materials")
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
        }
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

        property_values = list(property_values.values()) + date
        c.execute(configs.PROPERTY_VALUES_STATEMENT, property_values)

        subdivision_values = list(subdivision.values()) + date
        c.execute(configs.SUBDIVISION_STATEMENT, subdivision_values)

        tax_values = [str(item) for item in tax.values()] + date
        tax_values = tuple(tax_values)
        c.execute(configs.TAX_STATEMENT, tax_values)

        tax_history_values = list(tax_history.values()) + date
        tax_history_values = tuple(tax_history_values)
        c.execute(configs.TAX_HISTORY_STATEMENT, tax_history_values)

        improvement_values = list(improvement.values()) + date
        print(improvement_values)
        improvement_values = tuple(improvement_values)
        c.execute(configs.IMPROVEMENTS_STATEMENT, improvement_values)


#        conn.commit()


if __name__ == "__main__":
    main()
