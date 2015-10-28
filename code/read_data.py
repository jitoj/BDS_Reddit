import os
import json
import signal
import time,timeit
from sys import stdout
from collections import Counter,defaultdict

redditcount=defaultdict(Counter)

def signal_handler(signal, frame):
	if(raw_input("\nQuit [y/n]?").lower()=='y'):
		close_file(infile)
		write_output(outfile)
		close_file(outfile)
		print "\nExiting on interrupt"
		quit()
	else:
		return


def process_line(line_count,data):
	global redditcount
	try:
		stdout.write("\rReading line: %d" % line_count)
		stdout.flush()
		redditcount[data["subreddit"]][data["author"]]+=1
	except:
		print "Error in process_line"
		return


def process_file(infile,outfile):
	try:
		for line_count,line in enumerate(infile):#while line != '':# and line_count<10000:
		 if '[deleted]' not in line.rstrip():
		 	try:
			 	data=json.loads(line.rstrip())
				process_line(line_count,data)
			except:
				print "Error processing json"
				return
	except:
		print "Error processing file"
		return

def write_output(outfile):
	global redditcount
	try:
		for subreddit,authors in redditcount.iteritems():		
			outfile.write(subreddit+','+str(len(authors)))
			for author,count in authors.iteritems():
				outfile.write(','+author+','+str(count))
			outfile.write('\n')
	except:
		print "Error in write_output"
		return	

def close_file(closefile):
	closefile.close()
	return


if __name__ == "__main__":
	start=timeit.default_timer()

	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGTSTP, signal_handler)
	infile = open('../data/li.txt','r')
	outfile = open('../data/redditcounts.csv','w+')
	
	process_file(infile,outfile)
	close_file(infile)
	
	write_output(outfile)
	close_file(outfile)
	print "\nExiting normally\nRuntime:",time.strftime('%H:%M:%S',time.gmtime(timeit.default_timer()-start))
	quit()