import os
import json
import codecs
import signal
import bz2 as bz
import time,timeit
from sys import stdout
from collections import Counter,defaultdict

redditcount=defaultdict(Counter)
chunk_size = 16 * 1024
line_count=1
last_line=""

def signal_handler(signal, frame):
	if(raw_input("\nQuit [y/n]?").lower()=='y'):
		close_file(infile)
		write_output(outfile)
		close_file(outfile)
		print "\nExiting on interrupt"
		quit()
	else:
		return


def process_line(data):
	global redditcount,line_count
	try:
		stdout.write("\rReading line: %s" % line_count)
		stdout.flush()
		redditcount[data["subreddit"]][data["author"]]+=1
		line_count+=1
	except:
		print "Error in process_line"
		return


def process_file(infile):
	try:
		for line_count,line in enumerate(infile):
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

def process_zip(infile):
	global chunk_size,last_line,line_count
	decompressor = bz.BZ2Decompressor()
	try:
		while True:
			chunk = infile.read(chunk_size)
			if not chunk:
				break
			decomp = decompressor.decompress(chunk)

			if decomp:
				lines=decomp.split('\n')
				for i,line in enumerate(lines):
					if i==0:
						last_line=last_line+lines[0]
						if '[deleted]' not in last_line and len(last_line)!=0:
							try:
								data=json.loads(last_line.rstrip())
								process_line(data)			
							except:
								print "Error processing JSON:",line
								pass

					elif i==len(lines)-1:
						last_line=lines[len(lines)-1]
					else:
						if '[deleted]' not in line and len(line)!=0:
							try:
								data=json.loads(line.rstrip())
								process_line(data)			
							except:
								print "Error processing JSON:",line
								pass						
		return
	except:
		print "Error processing zipfile"
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
	#infile = codecs.open('../../../data/RC_2015-05.bz2','r')
	infile = codecs.open('../data/RC_2015-05.bz2','r')
	outfile = open('../data/redditcounts.csv','w+')
	
	#process_file(infile)	
	process_zip(infile)
	close_file(infile)
	
	write_output(outfile)
	close_file(outfile)
	print "\nExiting normally\nRuntime:",time.strftime('%H:%M:%S',time.gmtime(timeit.default_timer()-start))
	quit()