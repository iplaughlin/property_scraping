# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 16:57:49 2022

@author: iaala
"""

import requests
import pandas as pd
import datetime
from columns import (
    PARCEL_INFO_COLUMNS,
    VALUE_INFO_COLUMNS,
    TAX_COLUMNS,
    SUBDIVISION_COLUMNS,
    MATERIALS_COLUMNS,
)


def transpose_table(table: pd.DataFrame) -> pd.DataFrame:
    try:
        return table.set_index(0).transpose()
    except KeyError:
        print("error table", table)


def find_tables(table_list: list, url: str, ppin: int) -> dict:
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
