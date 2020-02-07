# script for excel file utils
# currently: combining the sheets in an excel file into a single csv
#   add a column to track the name/id of the original sheet (e.g. sheet_id)

import csv
import xlrd

def combine_sheets(exl_fp: str,
                   save_fp: str):
    edxl = xlrd.open_workbook(exl_fp)

    all_sheets = []
    num_sheets = 5 # some_int

    for i in range(num_sheets):
        sheet = edxl.sheet_by_index(i)
        all_sheets += [sheet]

    return all_sheets

# REFERENCE CODE

# import csv
# import xlrd

# edxl = xlrd.open_workbook('BrandList_ed.xlsx')

# idic = {1:'Banking', 2:'Insurance', 3:'Cosmetics', 4:'Hotels', 5:'Spirits',
#         6:'Beers',7:'Restaurants',8:'Soft Drinks',9:'Food',10:'Airlines',
#        11:'Apparel',12:'Retail',13:'Toys',14:'Telecommunications',15:'Automotive'}

# with open('companies_test.csv', 'w', encoding = 'utf-8', newline ='') as csvfile:
#     fieldnames = ['Company','Industry']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()

#     for i in range(0,15):
#         sheet = edxl.sheet_by_index(i)
#         companies = []

#         for rownum in range(sheet.nrows-1):
#             comnam = sheet.cell(rownum+1,1).value
#             companies.append(comnam)

#         for company in companies:
#             industry = (idic[(i+1)])
#             writer.writerow({'Company': company, 'Industry': industry})
#     print('Done!')
