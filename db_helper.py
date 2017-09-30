#!/usr/bin/python
#
import sys

import sqlite3


def db_drop(sql_conn, sqlc):
	
	sqlc.execute('PRAGMA writable_schema = 1')
	sqlc.execute("delete from sqlite_master where type in ('table', 'index', 'trigger')")
	sqlc.execute('PRAGMA writable_schema = 0')
	sqlc.execute('VACUUM')
	sqlc.execute('PRAGMA INTEGRITY_CHECK')
	
	sql_conn.commit()

def db_create(sql_conn, sqlc):
	
	sqlc.execute('CREATE TABLE background (id INTEGER PRIMARY KEY, name TEXT, html TEXT, source TEXT)')
	sqlc.execute('CREATE TABLE class (id INTEGER PRIMARY KEY, name TEXT, html TEXT, source TEXT)')
	sqlc.execute('CREATE TABLE companion (id INTEGER PRIMARY KEY, name TEXT, html TEXT, source TEXT)')
	sqlc.execute('CREATE TABLE deity (id INTEGER PRIMARY KEY, name TEXT, html TEXT, source TEXT)')
	sqlc.execute('CREATE TABLE disease (id INTEGER PRIMARY KEY, name TEXT, html TEXT, source TEXT)')
	sqlc.execute('CREATE TABLE epicdestiny (id INTEGER PRIMARY KEY, name TEXT, html TEXT, source TEXT, prereq INTEGER)')
	sqlc.execute('CREATE TABLE feat (id INTEGER PRIMARY KEY, name TEXT, html TEXT, source TEXT, prereq INTEGER)')
	sqlc.execute('CREATE TABLE glossary (id INTEGER PRIMARY KEY, name TEXT, html TEXT, source TEXT)')
	sqlc.execute('CREATE TABLE item (id INTEGER PRIMARY KEY, name TEXT, html TEXT, source TEXT, category TEXT, level INTEGER)')
	sqlc.execute('CREATE TABLE monster (id INTEGER PRIMARY KEY, name TEXT, html TEXT, source TEXT, group_role TEXT, role TEXT, level INTEGER)')
	sqlc.execute('CREATE TABLE paragonpath (id INTEGER PRIMARY KEY, name TEXT, html TEXT, source TEXT, prereq INTEGER)')
	sqlc.execute('CREATE TABLE poison (id INTEGER PRIMARY KEY, name TEXT, html TEXT, source TEXT)')
	sqlc.execute('CREATE TABLE power (id INTEGER PRIMARY KEY, name TEXT, html TEXT, source TEXT, recharge TEXT, type TEXT, usage TEXT, level INTEGER)')
	sqlc.execute('CREATE TABLE race (id INTEGER PRIMARY KEY, name TEXT, html TEXT, source TEXT)')
	sqlc.execute('CREATE TABLE ritual (id INTEGER PRIMARY KEY, name TEXT, html TEXT, source TEXT)')
	sqlc.execute('CREATE TABLE terrain (id INTEGER PRIMARY KEY, name TEXT, html TEXT, source TEXT)')
	sqlc.execute('CREATE TABLE theme (id INTEGER PRIMARY KEY, name TEXT, html TEXT, source TEXT)')
	sqlc.execute('CREATE TABLE trap (id INTEGER PRIMARY KEY, name TEXT, html TEXT, source TEXT)')
	
	sqlc.execute('CREATE TABLE feat_prereq (feat_name TEXT, feat_id INTEGER NOT NULL, prereq TEXT, FOREIGN KEY (feat_id) REFERENCES feat(id))')
	sqlc.execute('CREATE TABLE paragonpath_prereq (paragonpath_name TEXT, paragonpath_id INTEGER NOT NULL, prereq TEXT, FOREIGN KEY (paragonpath_id) REFERENCES paragonpath(id))')
	sqlc.execute('CREATE TABLE epicdestiny_prereq (epicdestiny_name TEXT, epicdestiny_id INTEGER NOT NULL, prereq TEXT, FOREIGN KEY (epicdestiny_id) REFERENCES epicdestiny(id))')
	sqlc.execute('CREATE TABLE item_level (item_name TEXT, item_id INTEGER NOT NULL, level INTEGER, FOREIGN KEY (item_id) REFERENCES item(id))')

	
	
	sql_conn.commit()

def main():
	if len(sys.argv) >= 2:
		action = sys.argv[1]
		
	
	sql_conn=sqlite3.connect('dnd4th.db')
	sql_conn.text_factory = str
	sqlc=sql_conn.cursor()
	
	if action=='create':
		db_create(sql_conn, sqlc)
		
	elif action=='drop':
		print "Cleaning db"
		db_drop(sql_conn, sqlc)
		db_create(sql_conn, sqlc)
	else:
		print "GIVE ME SOMETHING TO DO"
		
	sql_conn.commit()
	sql_conn.close()

if __name__ == '__main__':
    main()