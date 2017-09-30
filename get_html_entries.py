#!/usr/bin/python
#
import os
import sys

import argparse
import sqlite3
import urllib2

sql_conn=sqlite3.connect('dnd4th.db')
sql_conn.text_factory = str
sqlc=sql_conn.cursor()

def parse_url(url):
	index_1=0
	index_2=url.find('.')
	index_3=url.find('=')+1
	
	type=url[0:index_2]
	id=url[index_3:]
	
	return (type,id)
	
def get_source(entry):
	index_1=entry.find('publishedIn')+30
	index_1=entry.find('>', index_1)+1
	index_2=entry.find('<', index_1)
	return(entry[index_1:index_2])

	
def get_prereq(entry):
	index_1=entry.find("Prerequisite")
	if index_1==-1:
		return ''
		
	index_1+=18
	index_2=entry.find('<',index_1)
	return entry[index_1:index_2]
	
def get_recharge(entry):
	recharge=''
	if entry.find('atwillpower')!=-1:
		recharge='At Will'
	elif entry.find('encounterpower')!=-1:
		recharge='Encounter'
	elif entry.find('dailypower')!=-1:
		recharge='Daily'
	return recharge
	
	
def get_power_type_usage_level(name, entry):
	#print name
		
	index_2=entry.find(name+'<')-7
	index_1=entry.find("level")+7
	
	temp_str=entry[index_1:index_2]
	
	
	power_list=temp_str.split(' ')
	#print power_list
	
	temp_part=power_list[len(power_list)-1]
	if temp_part.isdigit():
		tuple2=temp_part
	else:
		tuple2='0'
	power_list.pop()
	
	tuple1=power_list[len(power_list)-1]
	power_list.pop();
	
	tuple0=' '.join(power_list)
	
	return (tuple0,tuple1,tuple2)
	

def get_monster_group_role_level(entry):
	index_1=entry.find('<span class="level">')
	if index_1==-1:
		return ('', 'Conjured', '')
	else:
		index_1+=20
	index_2=entry.find('<', index_1)
	
	temp_str=entry[index_1:index_2]
	#print temp_str
	temp_list=temp_str.split(' ')
	
	if temp_list[0]=='Level':
		temp_list.pop(0)
		tuple2=temp_list.pop(0)
	
	tuple1=''
	if temp_list[0]=='Solo' or temp_list[0]=='Elite' or temp_list[0]=='Minion':
		tuple0=temp_list.pop(0)
	else:
		tuple0='Standard'
	if temp_str.find('Leader')!=-1:
		tuple0+=' (Leader)'
	
	if len(temp_list)==0:
		tuple1=''
	else:
		tuple1=temp_list.pop(0)
	
	return (tuple0, tuple1, tuple2)
	
def get_item_level(entry):
	levels=[]
	index_1=entry.find('headerlevel')
	if index_1==-1:
		return levels
	else:
		index_1+=13
	
	index_2=entry.find('<', index_1)
	temp_str=entry[index_1:index_2]
	if temp_str.find('+')==-1:
		temp_list=temp_str.split(' ')
		levels.append(temp_list[1])
		return levels
		
	find_lvl=True
	while find_lvl:
		index_1=entry.find('mic1', index_2)
		if index_1==-1:
			find_lvl=False
		else:
			index_1+=10
			index_2=entry.find('<', index_1)
			levels.append(entry[index_1:index_2])
	
	return levels

	
def add_db_entry_0(name, url, entry, table_name):
	#default
	global sqlc
	global sql_conn
	type_id=parse_url(url)
	id=type_id[1]
	values=(id, name, entry, get_source(entry))
	
	try:
		sqlc.execute('INSERT INTO {tb} VALUES (?,?,?,?)'.format(tb=table_name), values)
	except sqlite3.IntegrityError:
		#print name, "with id", id, "already exists in table", type
		pass
	
	#sql_conn.commit()

def add_db_prereq(thing_id, thing_name, type, prereqs):
	global sqlc
	global sql_conn
	if prereqs.find(';')==-1:
		prereq_list=prereqs.split(', ')
	else:
		prereq_list=prereqs.split('; ')
	#print prereq_list
	for pq in prereq_list:
		values=(thing_name, thing_id, pq)
		sqlc.execute('INSERT INTO {tb}_prereq VALUES (?,?,?)'.format(tb=type), values)
		#sql_conn.commit()

def add_db_entry_1(name, url, entry, table_name):
	#feats and paragon paths and epic destinies
	global sqlc
	global sql_conn
	type_id=parse_url(url)
	id=type_id[1]
	prereqs=get_prereq(entry)
	if prereqs=='':
		prereq_yes=False
	else:
		prereq_yes=True
	values=(id, name, entry, get_source(entry), prereq_yes)
	
	try:
		sqlc.execute('INSERT INTO {tb} VALUES (?,?,?,?,?)'.format(tb=table_name), values)
	except sqlite3.IntegrityError:
		#print name, "with id", id, "already exists in table", type
		pass
	
	if prereq_yes:
		add_db_prereq(id, name, table_name, prereqs)
	
	#sql_conn.commit()
	
def add_db_entry_2(name, url, entry, table_name):
	#powers
	global sqlc
	global sql_conn
	type_id=parse_url(url)
	id=type_id[1]
	#recharge TEXT, type TEXT, usage TEXT, level INTEGER
	power_tuple=get_power_type_usage_level(name, entry)
	values=(id, name, entry, get_source(entry), get_recharge(entry), power_tuple[0], power_tuple[1], power_tuple[2])
	
	try:
		sqlc.execute('INSERT INTO {tb} VALUES (?,?,?,?,?,?,?,?)'.format(tb=table_name), values)
	except sqlite3.IntegrityError:
		#print name, "with id", id, "already exists in table", type
		pass
	
	#sql_conn.commit()
	
	
def add_db_entry_3(name, url, entry, table_name):
	#monsters
	global sqlc
	global sql_conn
	type_id=parse_url(url)
	id=type_id[1]
	#level INTEGER, role TEXT, group_role TEXT'
	monster_tuple=get_monster_group_role_level(entry)
	values=(id, name, entry, get_source(entry), monster_tuple[0], monster_tuple[1], monster_tuple[2])
	
	try:
		sqlc.execute('INSERT INTO {tb} VALUES (?,?,?,?,?,?,?)'.format(tb=table_name), values)
	except sqlite3.IntegrityError:
		#print name, "with id", id, "already exists in table", type
		pass
	
	#sql_conn.commit()
	
def add_db_item_levels(item_id, item_name, levels):
	global sqlc
	global sql_conn
	for lvl in levels:
		values=(item_name, item_id, lvl)
		sqlc.execute('INSERT INTO item_level VALUES (?,?,?)', values)
		#sql_conn.commit()
	
def add_db_entry_4(name, url, entry, table_name, type):
	#items
	global sqlc
	global sql_conn
	type_id=parse_url(url)
	id=type_id[1]
	levels=get_item_level(entry)
	if len(levels)>0:
		level_yes=True
	else:
		level_yes=False
	values=(id, name, entry, get_source(entry), type, level_yes)
	
	try:
		sqlc.execute('INSERT INTO {tb} VALUES (?,?,?,?,?,?)'.format(tb=table_name), values)
	except sqlite3.IntegrityError:
		#print name, "with id", id, "already exists in table", type
		pass
	
	if level_yes:
		add_db_item_levels(id, name, levels)
	
	#sql_conn.commit()

	
def add_db_entry(name, url, entry, table_name, type):
##  Rewrite to parse source from all things
##  prerequisits from feats and paragon paths
## 	category (head, arm, ring, belt, ect) gold and level from items
##	level, role, group role, from monsters
##  recharge (at will, encounter, daily), type (racial, attack, utility) , level, class/race/feat, for powers
	
	if table_name=='feat' or table_name=='paragonpath' or table_name=='epicdestiny':
		add_db_entry_1(name, url, entry, table_name)
	elif table_name=='power':
		add_db_entry_2(name, url, entry, table_name)
	elif table_name=='monster':
		add_db_entry_3(name, url, entry, table_name)
	elif table_name=='item':
		add_db_entry_4(name, url, entry, table_name, type)
	else:
		add_db_entry_0(name, url, entry, table_name)
	
def parseHTML(html):
	try:
		index_1=html.index('<div id="detail"')
	except ValueError:
		raise
		
	index_2=html.index('</div', index_1)+6
	
	parsed=html[index_1:index_2]
	
	return parsed
	

def getHTML(name_url_pairs, table_name, table_type):
	base_url='http://localhost/ddi/'
	
	for name_url in name_url_pairs:
		name=name_url[0]
		url=name_url[1]
		full_url=base_url+url
		
		#print name_url
		#print full_url
		
		request=urllib2.urlopen(full_url)
		html=request.read()
		try:
			result=parseHTML(html)
		except ValueError:
			file=open('errors.txt', 'a')
			file.write('Error with '+name+' at '+url+'\n')
			file.close()
		else:
			add_db_entry(name, url, result, table_name, table_type)
	


def get_tuple(line):
	try:
		index_1 = line.index('"')+1
	except ValueError:
		raise
	else:
		index_2 = line.index('"', index_1)
		index_3 = line.index('../', index_2  + 1) + 3
		index_4 = line.index('\'', index_3)
		
		name=line[index_1 : index_2]
		url=line[index_3 : index_4]
		
		return (name, url)
	
def readFile(filename):
	#print 'Opening ', filename
	
	file = open(filename, 'r')
	name_url_pairs = []
	
	for line in file:
		try:
			result=get_tuple(line)
		except ValueError:
			pass
		else:
			#print result
			name_url_pairs.append(result)
	
	file.close()
	#print len(name_url_pairs), 'entries have been read from', filename
	return name_url_pairs

	

def db_close():
	global sql_conn
	sql_conn.commit()
	sql_conn.close()


def parse_command_line():
    """
    Parses command line options and returns an argparse instance.
    """
    parser = argparse.ArgumentParser(description='Parses ID\'s from the DDI compendium search results,  and then downloads the html and puts them into a sqlite database.')
    parser.add_argument('-f', '--file', dest='file',
            action='store',
            help='Filenname to be read')
    arg_manager = parser.parse_args()
    return arg_manager
	
def main(arg_manager):
	os.system("python db_helper.py drop")
	
	print "Opening main file ", arg_manager.file
	
	file=open(arg_manager.file,'r')
	file_names=[]
	for line in file:
		file_names.append(line[:-1])
	#file_names.pop()
	file.close()
	
	print file_names
	
	for name in file_names:
		print "Opening subfile ", name
		
		file=open(name, 'r')
		table_name=(file.readline())[:-1]
		table_type=(file.readline())[:-1]
		file.close()
		
		print "Reading entries from", name
		name_url_pairs = readFile(name)
		print len(name_url_pairs), " entries read from ", name
		
		print "Gathering DB entry data for ", name
		getHTML(name_url_pairs, table_name, table_type)

	db_close()
	return True

if __name__ == '__main__':
    arg_manager = parse_command_line()
    main(arg_manager)