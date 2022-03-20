# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 16:57:49 2022

@author: iaala
"""

import re
from collections import defaultdict
import datetime
from columns import (
    PARCEL_INFO_COLUMNS,
    VALUE_INFO_COLUMNS,
    TAX_COLUMNS,
    SUBDIVISION_COLUMNS,
    MATERIALS_COLUMNS,
)


def transpose_table(table):
    try:
        return table.set_index(0).transpose()
    except KeyError:
        print("error table", table)


def find_tables(table_list: list, url: str, ppin: int) -> dict:
    import pandas as pd

    parcel_table = None
    value_table = None
    subdivision_table = None
    tax_table = None
    materials_table = None
    for table in table_list:
        try:
            if (
                sum(
                    table[1].str.contains(
                        "MADISON COUNTY Property Appraisal and Tax Payments"
                    )
                )
                > 0
            ):
                pass
            elif any(
                item in PARCEL_INFO_COLUMNS for item in transpose_table(table).columns
            ):
                parcel_table = transpose_table(table)
            elif any(
                item in VALUE_INFO_COLUMNS for item in transpose_table(table).columns
            ):
                value_table = transpose_table(table)
            elif any(
                item in SUBDIVISION_COLUMNS for item in transpose_table(table).columns
            ):
                subdivision_table = transpose_table(table)
            elif any(
                item in MATERIALS_COLUMNS for item in transpose_table(table).columns
            ):
                materials_table = transpose_table(table)
            else:
                print(transpose_table(table))
                print(transpose_table(table).columns)
        except KeyError:
            try:
                if "Property Appraisal and Tax Payments" in table[0]:
                    pass
            except KeyError:
                if all(item in TAX_COLUMNS for item in table):
                    tax_table = table
        except AttributeError:
            if all(
                table
                == pd.read_json(
                    '{"0":{"0":"PIN","1":"PARCEL","2":"ACCOUNT NUMBER"},"1":{"0":123456.0,"1":123456789.0,"2":999888777.0}}'
                )
            ):
                pass
            else:
                print("missing table", table)
    return {
        "parcel": parcel_table,
        "value": value_table,
        "subdivision": subdivision_table,
        "tax": tax_table,
        "materials": materials_table,
        "date_time_collected": str(datetime.datetime.now()),
        "url": url,
        "gis_url": f"https://isv.kcsgis.com/al.Madison_revenue/?fips={ppin}",
    }


def table_information_one(soup, div_id_name: str = None) -> dict:
    """ first method for bringing back table information as a dict.
    works on:
        parcelInfo
        SummaryPropertyValues
        SummarySubdivision
    """
    table = []
    for x in soup.find_all("div", {"id": div_id_name}):
        for div in x.find_all("div"):
            for row in x.find_all("tr"):
                cols = row.find_all("td")
                cols = [element.text.strip() for element in cols if element]
                table.extend(cols)
    it = iter(table)
    test_dict = dict(zip(it, it))
    if test_dict.get(""):
        del test_dict[""]
    return test_dict


def table_information_two(soup, div_id_name) -> dict:
    """ second method for bringing back table information as a dict.
    works on:
        TaxInfo

    """
    temp_dict = dict()
    for x in soup.find_all("div", {"id": div_id_name}):
        headers = x.find_all("th")
        headers = [item.string for item in headers]
        values = x.find_all("td")
        values = [item.string for item in values]
        temp_dict = dict(zip(headers, values))
    return temp_dict


def table_information_three(soup, div_id_name) -> dict:
    """ third method for bringing back table information as a dict.
    works on:
        SummaryDetailInfo

    """
    temp_dict = defaultdict(list)
    if soup.find("div", {"id": div_id_name}):
        rows = []
        for i in soup.find("div", {"id": div_id_name}).find_all("tr"):
            if (
                i.text
                == "\nYEAR\nOWNER(S)\nTOTAL TAX\nPAID (Y/N)\nAPPRAISED\nASSESSED\n"
            ):
                rows.append([item for item in re.split("\n|\r", i.text)])
            elif (
                i.text
                == "\nTYPE\nREF\nDESCRIPTION\nLAND USE\nTC\nHS\nPN\nAPPRAISED VALUE\n"
            ):
                rows.append([item for item in re.split("\n|\r", i.text)])
            else:
                rows.append([item.text for item in i.find_all("td")])
            # print(repr(i.text))
        headers = [item for item in rows[0] if item]
        for row in rows[1:]:
            row = [item for item in row if item]
            x = 0
            for header in headers:
                temp_dict[header].append(row[x])
                x += 1
    else:
        pass
    return temp_dict


def table_information_four(soup, div_id_name) -> dict:
    """ fourth method for bringing back table information as a dict.
    works on:
        SummaryBuildingComponents

    """
    table = []
    improvement_columns = [
        "Year Built",
        "Structure",
        "Structure Code",
        "Total Living Area",
        "Building Value",
    ]
    computation_columns = [
        "stories",
        "1st level sq. ft.",
        "add'l level sq. ft.",
        "total living area",
        "total adjusted area",
    ]
    materials_columns = [
        "foundation",
        "exterior walls",
        "roof type",
        "roof material",
        "floors",
        "interior finish",
        "plumbing",
        "fireplaces",
        "heat/ac",
    ]
    for x in soup.find_all("div", {"id": div_id_name}):
        for item in x.find_all("div", {"class": "col"}):
            for row in x.find_all("tr"):
                if (
                    "improvement" not in row.text.lower()
                    and "computations" not in row.text.lower()
                ):
                    cols = row.find_all("td")
                    cols = [element.text.strip() for element in cols if element]
                    table.extend(cols)
                    table = [item for item in table if not ""]
                else:
                    pass
    it = iter(table)
    test_dict = dict(zip(it, it))
    improvement = {
        key: value for key, value in test_dict.items() if key in improvement_columns
    }
    if improvement == {}:
        improvement = {column: "" for column in improvement_columns}
    # for column in improvement_columns:
    #     del test_dict[column]
    computations = {
        key: value
        for key, value in test_dict.items()
        if key.lower() in computation_columns
    }
    if computations == {}:
        computations = {column: "" for column in computation_columns}
    materials = defaultdict(list)
    for key, value in test_dict.items():
        if value.lower() in materials_columns:
            materials[value.lower()].append(key)
    try:
        max_length = max([len(item) for item in materials.values()])
    except ValueError:
        max_length = 0
    print(max_length)
    for column in materials_columns:
        while len(materials[column]) < max_length:
            materials[column] += [""]
    if materials == defaultdict(list):
        for column in materials_columns:
            materials[column]
    return {
        "improvement": improvement,
        "computations": computations,
        "materials": materials,
    }
