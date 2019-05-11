#!/usr/bin/env python
#title:             scrape.py
#description:       Scrape Mostly Mutts - https://www.mostlymutts.org
#author:            Ricky Laney
#date:              20181215
#version:           0.1.0
#usage:             python scrape.py or ./scrape.py
#notes:             Grab urls from menu items to recurse. Saves main content text from each page.
#python_version:    3.6.5
#==============================================================================


import os
import sys
from ftplib import FTP, all_errors

BASE_URL = "ftp.cisco.com"

LONG_TEXT = '''
cisco Systems Public MIB Area
==================================

cisco's public mib area has been reorganized to make it easier for you
to find the mibs that you need.  All SNMPv1 mibs are now in the
subdirectory "v1".  All SNMPv2 mibs are now in the subdirectory "v2".

The suggested way to retrieve the MIBs applicable to the cisco
products that you wish to manage is as follows:

    for each product, retrieve the file supportlists/[product]/supportlist.txt.
    (or supportlists/[product]/supportlist.html for those using WWW)
    determine which mibs each product supports from the retrieved file.
    consult the v2/readme or v1/readme file for brief descriptions of the
    functionality provided by each mib.
    retrieve all mibs which provide the functionality you are interested in,
    and are applicable to the cisco products you wish to support.
    if you need the SunNet Manager OID files, retrieve those for each
    MIB from the oid directory.
    if you need the SunNet Manager schema files, retrieve those for
    each MIB from the schema directory

The following is a list of directories which are in this directory.
The file you're reading is the one named "README", in directory
pub/mibs.

===========================================================================

(1)  ucs-mibs           UCS MIBs
(2)  ucs-C-Series-mibs  UCS-C Series MIBs
(3)  v1                 SNMP version 1 mibs and SNMPv1 conversions of the SNMP version 2 mibs.
(4)  v2                 SNMP version 2 mibs.
(5)  oid                directory w/ SunNet Manager OID files for the mibs.
(6)  schema             directory w/ SunNet Manager schema files for the mibs.
(7)  supportlist        directory w/ directories for each product with information about which mibs that product supports.
(8)  traps              directory w/ SunNet Manager trap files for the mibs.
(9)  app_notes          directory w/ application notes for using the mibs.
(10) archive            directory w/ mibs, oids, schema for IOS 10.0 and earlier releases.
(11) contrib            directory w/ helpful mib-related scripts/files (see contrib/README)
'''

select_map = {
        1: "ucs-mibs",
        2: "ucs-C-Series-mibs",
        3: "v1",
        4: "v2",
        5: "oid",
        6: "schema",
        7: "supportlist",
        8: "traps",
        9: "app_notes",
        10: "archive",
        11: "contrib"
        }


def input_selection():
    print(LONG_TEXT)
    sel = input(f"Enter the number you wish to scrape: ")
    if sel in select_map.keys():
        return f"{select_map[sel]}"
    else:
        print(f"It looks like you did not enter a valid number: {selection}.\n \
               Please try again.")
        input_selection()


def make_dirs():
    if 'mib_stuff' in os.scandir():
        os.rmdir('mib_stuff')
    os.mkdir('mib_stuff')


def get_mibs(sel):
    try:
        ftp = FTP(BASE_URL)
        ftp.login()
        ftp.cwd('pub')
        ftp.cwd('mibs')
        ftp.cwd(sel)
        ftp.dir()
        ftp.()
    except all_errors as e:
        return f"Error connecting to {url} CODE: {e}"


if __name__ == '__main__':
    print("Please make sure you are in a empty directory.")
    print("This program will create and delete the directories 'content' and 'all_text'")
    if input("To continue type 'y' and hit enter: ") == 'y':
        url = input_base_url()
        make_dirs()
        urls = get_urls(url)
        write_all_text(urls)
        write_content(urls)
    else:
        sys.exit(1)

