# Python_DnD_Helper

These are a small set of python scripts that scrape the DDI Compendium for 4th Edition DND.

These scripts require you to be logged in or otherwise have access to the DDI compendium.

The data is stored using SQLite3.

---

###db_helper.py
This file initializes the schema for the sqlite3 database file.  It also helps drop tables from the database if needed.

###get_html_entries.py
This file reads in text files and parses them to learn which id and name the specific entry is stored in the DDI Compendium.  It then access that webpage/webapp to fetch the html response.  It then parses the html to get all the information needed to store the item into the sqlite3 database.