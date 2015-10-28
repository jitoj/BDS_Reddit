import os
import sys
import json
import signal
from collections import Counter,defaultdict

redditcount=defaultdict(Counter)
line_count=1

def signal_handler(signal, frame):
	if(raw_input("\nQuit [y/n]?").lower()=='y'):
		close_file(infile)
		write_output(outfile)
		close_file(outfile)
		quit()
	else:
		return


def process_line(data):
	global redditcount,line_count
	try:
		print "Reading line:",line_count," ",data["subreddit"]," ",data["author"]
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

def write_output(outfile):
	global redditcount
	try:
		for subreddit,authors in redditcount.iteritems():		
			outfile.write(subreddit+','+str(len(authors)))
			print "Writing subreddit:",subreddit
			for author,count in authors.iteritems():
				outfile.write(','+author+','+str(count))
			outfile.write('\n')
	except:
		return	

def close_file(closefile):
	closefile.close()
	return


if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGTSTP, signal_handler)
	global line
	#infile = open('data/RC_2015-05','r')
	#outfile = open('data/redditcounts.csv','w+')	
	infile = open('../data/li.txt','r')
	outfile = open('../data/redditcounts.csv','w+')
	try:
		process_file(infile,outfile)
		close_file(infile)
	except:
		pass
	write_output(outfile)
	close_file(outfile)
	quit()
