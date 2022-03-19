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
import columns


def main():

    temp_dict = dict()
    for ppin in range(1, 10001):
        print(ppin)
        url = f"https://madisonproperty.countygovservices.com/Property/Property/Summary?taxyear=2022&ppin={ppin}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"}
        resp = requests.get(url, headers = headers)
        time.sleep(0.5)
        soup = BeautifulSoup(resp.text, "html.parser")
        parcel_info = table_information_one(soup, "collapseParcelInfo")
        if parcel_info == {}:
            parcel_info = {column, "" for column in columns.PARCEL_INFO_COLUMNS}
        property_values = table_information_one(soup, "collapseSummaryPropertyValues")
        if property_values == {}:
            property_values = {column, "" for column in columns.PROPERTY_COLUMNS}
        subdivision = table_information_one(soup, "collapseSummarySubdivision")
        if subdivision == {}:
            subdivision = {column, "" for column in columns.SUBDIVISION_COLUMNS}
        tax = table_information_two(soup, "collapseTaxInfo")
        if tax == {}:
            tax = {column, "" for column in columns.TAX_COLUMNS}

        tax_history = table_information_three(soup, "collapseTaxHistory")
        details = table_information_three(soup, "collapseSummaryDetailInfo")

        building_components = table_information_four(
            soup, "collapseSummaryBuildingComponents"
        )
        improvement = building_components.get("improvement")
        computations = building_components.get("computations")
        materials = building_components.get("materials")

        gis_url= f"https://isv.kcsgis.com/al.Madison_revenue/?fips={ppin}"

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
            "gis_url": f"https://isv.kcsgis.com/al.Madison_revenue/?fips={ppin}"
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

        for row in zip(*list(tax_history.values())):
            c.execute(configs.TAX_HISTORY_STATEMENT, row + tuple(date))

        for row in zip(*list(details.values())):
            c.execute(configs.DETAILS_STATEMENT, row + tuple(date))

        improvement_values = list(improvement.values()) + date
        improvement_values = tuple(improvement_values)
        c.execute(configs.IMPROVEMENTS_STATEMENT, improvement_values)

        computations_values = list(computations.values()) + date
        computations_values = tuple(computations_values)
        c.execute(configs.COMPUTATION_STATEMENT, computations_values)

        for row in zip(*list(materials.values())):
            c.execute(configs.MATERIALS_STATEMENT, row + tuple(date))

        urls_values = (url, gis_url)+tuple(date)
        c.execute(configs.URLS_STATEMENT, urls_values)
#        conn.commit()


if __name__ == "__main__":
    main()
