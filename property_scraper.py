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
    for ppin in range(1, 501):
        url = f"https://madisonproperty.countygovservices.com/Property/Property/Summary?taxyear=2022&ppin={ppin}"
        resp = requests.get(url)
        time.sleep(0.5)
        soup = BeautifulSoup(resp.text)
        parcel_info = table_information_one(soup, "collapseParcelInfo")
        property_values = table_information_one(soup, "collapseSummaryPropertyValues")
        subdivision = table_information_one(soup, "collapseSummarySubdivision")

        tax = table_information_two(soup, "collapseTaxInfo")

        details = table_information_three(soup, "collapseSummaryDetailInfo")
        tax_history = table_information_three(soup, "collapseTaxHistory")

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
        print(ppin)


if __name__ == "__main__":
    main()
