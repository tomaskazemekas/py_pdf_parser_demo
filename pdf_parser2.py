# -*- coding: utf-8 -*-
# Python environment: Anaconda3

# by Tomas Kazemekas, 
# tomaskazemekas@gmail.com

# Version: 2.0


"""
This is an proof of concept script to test the working of PyPDF2
 library with supplied example of PDF document in Python 3.4
 environment. The script shows how to extract the required data form
 a PDF file.  
 
 The exact form of the inputs, e.g. from command line or other could be
 set later, when the exact data flow procedure will be specified.
 The same applies to the outputs which is planned to be inserted in the
 database.
"""


from PyPDF2 import PdfFileReader


# Path to an example of PDF document.
# Currently it is in the same directory as this .py script
DOCUMENT = "HISINV_20150511_34400I_AEQUAM_DIVERSIFIED_INDEX.pdf"

#Setting the required asset name. Can be set to any name from the table.
# Please keep the capitalization the same as in the original PDF.
ASSET1 = "CME MINI NASDA1"
ASSET2 = "S&P500 MINI"


# Setting the word indicating the required table, e. g. INVERSES. 
TABLE_MARK = "INVERSES"

# Seting the marker word for the start of the line of the currency table
# INVERSES.
LINE_MARK = "Cours"


pdf_input = PdfFileReader(open(DOCUMENT, "rb"))

# print how many pages input1 has. To test general functioning of the library.
print ("This document has %d pages." % pdf_input.getNumPages(), "\n")

# Transforming the tesxt from the first page of the Pdf document
# in to a list.    
page_lst1 = pdf_input.pages[0].extractText().split()

print("Input from page 1 of the PDF file  as a list: \n", page_lst1, "\n")


# String, list -> int, int
# Defining asset index finding function.
def asset_find(asset_name, page_lst):
    """
    Finds asset by name in the list of words extracted from PDF page.
    Returns the indexex of the first and the last of the asset names.
    If the asset is not found, prints statment and returns None.
    """
    sublist = asset_name.split()
    ind_marker_f = page_lst.index(sublist[0])
    while True:        
        ind_marker_l = ind_marker_f + len(sublist)
        if page_lst[ind_marker_f : ind_marker_l] == sublist:
            return ind_marker_f, (ind_marker_l - 1)
        else:
            try:
                ind_marker_f = page_lst.index(sublist[0], ind_marker_f + 1)
            except ValueError:
                print ("Asset name not found")
                return None
                

asset_mark_f, asset_mark_l = asset_find(ASSET1, page_lst1)   
print("Asset name position in the list is:", asset_mark_f, asset_mark_l, "\n")

# Showing that the required price column is always in the 7th position 
# from the assetMarkerLast.    
print("Table line of the asset:", page_lst1[asset_mark_f : asset_mark_l+8],
      "\n")

#Extractig the required price.
asset_price1 = float(page_lst1[asset_mark_l + 7])
print(ASSET1, "price is", asset_price1, "\n")

asset_mark_f, asset_mark_l = asset_find(ASSET2, page_lst1)   
print("Asset name position in the list is:", asset_mark_f, asset_mark_l,
      "\n")

# Showing that the required price column is always in the 7th position 
# from the assetMarkerLast.    
print("Table line of the asset:", page_lst1[asset_mark_f : asset_mark_l+8],
      "\n")

# Extractig the required price.
asset_price2 = float(page_lst1[asset_mark_l + 7])
print(ASSET2, "price is", asset_price2, "\n")

print("Testing of data extraction from the PDF tables on page 1 completed. \n")


# Currency data extraction


# Assuming the INVERSES table is on the last page.
# Parsing the last page.
page_lst_l = pdf_input.pages[-1].extractText().split()

# Finding the table with the word "INVERSES" in the title. Getting the index
# of it.
table_marker = page_lst_l.index(TABLE_MARK)
print("Index of tableMarker is:", table_marker, "\n")

# Creating  a list from the table.
table_lst_l2 = page_lst_l[table_marker-1 :]
print(table_lst_l2, "\n")


# Scaning the INVERSES table.
#  String, list -> list of tuples, consisting of (list of strings, float)


def table_scan(line_mrk, page_lst):
    """ Function scans indicated table on a PDF file and extracts all the
    lines containing currency pairs. It returns a list of tuples. A tuple
    consists of a list of strings, for name  and a flot for price.
    """
    result = []
    offset = -1
    while True:
        try:
            offset = page_lst.index(line_mrk, offset+1)
        except ValueError:
            return result
        
        currency_pair = page_lst[offset+1 : offset+4]
        price = float(page_lst[offset + 5])
        result.append((currency_pair, price))
        

# Extracting all the currency pairs from the selected table.    
currency_data = table_scan(LINE_MARK, table_lst_l2)
print("Currency Data", currency_data, "\n")    

print("Testing of currency data extraction from the PDF table on the last ",
      "page  completed. \n")

