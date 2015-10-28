import os
import sys
import json
from collections import Counter,defaultdict

redditcount=defaultdict(Counter)
line_count=1
def process_line(data):
	global redditcount,line_count
	print "Line:",line_count," ",data["subreddit"]," ",data["author"]
	redditcount[data["subreddit"]][data["author"]]+=1
	line_count+=1
	return


def process_file(infile,outfile):
	global line_count
	line=infile.readline()
	while line != '':# and line_count<10000:
	 if '[deleted]' not in line:
	 	data=json.loads(line)
		process_line(data)
	 line=infile.readline()
	return

if __name__ == "__main__":
	global line
	infile = open('data/RC_2015-05','r')
	outfile = open('data/redditcounts.csv','w')
	process_file(infile,outfile)
	for subreddit,authors in redditcount.iteritems():
		#print subreddit
		outfile.write(subreddit+','+str(len(authors)))
		for author,count in authors.iteritems():
			outfile.write(','+author+','+str(count))
		outfile.write('\n')
	infile.close()
	outfile.close()
	quit()
