import os
import sys
import json
from collections import Counter,defaultdict

redditcount=defaultdict(Counter)
line_count=1
def process_line(data):
	global redditcount,line_count
	try:
		print "Line:",line_count," ",data["subreddit"]," ",data["author"]
		redditcount[data["subreddit"]][data["author"]]+=1
		line_count+=1
	except:
		return


def process_file(infile,outfile):
	global line_count
	try:
		line=infile.readline()
		while line != '':# and line_count<10000:
		 if '[deleted]' not in line:
		 	try:
			 	data=json.loads(line)
				process_line(data)
			except:
				pass
		 line=infile.readline()
	except:
		return

if __name__ == "__main__":
	global line
	infile = open('../data/li.txt','r')
	outfile = open('../data/redditcounts.csv','w+')
	try:
		process_file(infile,outfile)
	except:
		pass
	try:
		for subreddit,authors in redditcount.iteritems():		
			outfile.write(subreddit+','+str(len(authors)))
			for author,count in authors.iteritems():
				print subreddit
				outfile.write(','+author+','+str(count))
			outfile.write('\n')
	except:
		pass
	infile.close()
	outfile.close()
	quit()
