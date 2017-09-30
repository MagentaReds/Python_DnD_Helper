#select distinct feat_name, feat_id from feat_prereq where prereq LIKE '%warden%';
import os
import sys

import sqlite3

def main():
	if len(sys.argv) >= 2:
		action = sys.argv[1]


if __name__ == '__main__':
    main()