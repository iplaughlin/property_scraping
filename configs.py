PARCEL_STATEMENT = """ INSERT into parcel(
                       pin,
                       parcel,
                       account_number,
                       owner,
                       mailing_address,
                       property_address,
                       legal_description,
                       exempt_code,
                       tax_district,
                       date_time) VALUES(
                       %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

COMPUTATION_STATEMENT = """ INSERT into computations(
                        total_living_area,
                        stories,
                        first_level_sq_ft,
                        addl_level_sq_ft,
                        total_adjusted_area,
                        date_time,
                        pin) VALUES(
                        %s,%s,%s,%s,%s,%s,%s)"""

IMPROVEMENTS_STATEMENT= """ INSERT into improvements(
                       year_built,
                       structure,
                       structure_code,
                       total_living_area,
                       building_value,
                       date_time,
                       pin) VALUES(
                       %s,%s,%s,%s,%s,%s,%s)"""
MATERIALS_STATEMENT = """ INSERT into materials(
                      foundation,
                      exterior_walls,
                      roof_type,
                      roof_material,
                      floors,
                      interior_finish,
                      plumbing,
                      fireplaces,
                      heat_ac,
                      date_time,
                      pin) VALUES(
                      %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
SUBDIVISION_STATEMENT = """ INSERT into subdivision(
                        code,
                        name,
                        lot,
                        block,
                        type_book_page,
                        s_t_r,
                        date_time,
                        pin) VALUES(
                        %s,%s,%s,%s,%s,%s,%s,%s)"""

TAX_STATEMENT = """INSERT into tax(
               year,
               tax_due,
               paid,
               balance,
               date_time,
               pin) VALUES(
               %s,%s,%s,%s,%s,%s)"""

TAX_HISTORY_STATEMENT = """INSERT into tax_history(
                        year,
                        owner,
                        total_tax,
                        paid,
                        appraised,
                        assessed,
                        date_time,
                        pin) VALUES(
                        %s,%s,%s,%s,%s,%s,%s,%s)"""

URLS_STATEMENT = """INSERT INTO urls(
                 url,
                 gis_url,
                 date_time,
                 pin) VALUES(
                 %s,%s,%s,%s)"""

PROPERTY_VALUES_STATEMENT = """INSERT INTO value(
                  total_acres,
                  use_value,
                  land_value,
                  improvement_value,
                  total_appraised_value,
                  total_taxable_value,
                  assessment_value,
                  date_time,
                  pin) VALUES(
                  %s,%s,%s,%s,%s,%s,%s,%s,%s)"""

DETAILS_STATEMENT = """INSERT INTO details(
                    type,
                    ref,
                    description,
                    land_use,
                    tc,
                    hs,
                    pn,
                    appraised_value,
                    date_time,
                    pin) VALUES (
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
