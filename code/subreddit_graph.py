import networkx as nx
import os
import matplotlib.pyplot as plt
from random import randint
from   datetime import datetime

sr_filter=',askreddit,funny,todayilearned,pics,worldnews,science,announcements,explainlikeimfive,askmen,iama,videos,gaming,soccer,movies,music,aww,news,gifs,books,television,technology,mildlyinteresting,sports,diy,showerthoughts,bestof,space,fitness,tifu,jokes,wtf,internetisbeautiful,photoshopbattles,history,gadgets,nottheonion,dataisbeautiful,4chan,adviceanimals,twoxchromosomes,earthporn,art,askhistorians,atheism,blackpeopletwitter,comics,conspiracy,creepy,cringe,cringepics,documentaries,europe,facepalm,fffffffuuuuuuuuuuuu,foodporn,freebies,frugal,futurology,gamedeals,games,gentlemanboners,getmotivated,hiphopheads,historyporn,interestingasfuck,justiceporn,lifehacks,listentothis,malefashionadvice,nosleep,oddlysatisfying,oldschoolcool,outoftheloop,pcmasterrace,personalfinance,philosophy,pokemon,politics,reactiongifs,relationships,sex,tattoos,trees,truereddit,wallpapers,youtube,wow,thebutton,'
def print_neighbors(node):
	for item in G.neighbors(node):
		print item

if __name__ == "__main__":
	
	infile = open('../data/usercounts.csv','r')
	start = datetime.now()
	G=nx.Graph()
	for line in infile:
		line=line.lower()
		data=line.split(',')
		i=2
		while (i<=len(data)-3 and data[1]>1):
			if ','+data[i].lower()+',' not in sr_filter and ','+data[i+2].lower()+',' not in sr_filter:
				if G.has_edge(data[i], data[i+2]) or G.has_edge(data[i+2], data[i]):
					G.edge[data[i]][data[i+2]]['weight']+=1
				else:
					G.add_edge(data[i],data[i+2],weight=1)

			i+=2
	print "Nodes",G.number_of_nodes(),
	print "Edges",G.number_of_edges()
	print "RUNTIME: create_graph()",datetime.now()-start
	node="gatech"
	while node!="":
		node=raw_input('Enter subreddit:').lower()

		if node.isspace() or len(node)==0:
			break
		rcolor=["#70b0c5","#2ca25f","#fff7bc","#bcbddc"]
		try:
			start = datetime.now()
			sorted_G=sorted(G[node], key=lambda (target): G[node][target],reverse=True)[:10]
			H=nx.Graph()
			print '-' * 43
			print '   RANK SUBREDDIT                 WEIGHT'
			print '-' * 43
			for i,item in enumerate(sorted_G):
				print ("%7d %-25s %-7d"%(i+1,item, G[node][item]['weight']))
				H.add_edge(node,item,weight=G[node][item]['weight'])
				print "\nRUNTIME: get_neighbours()",datetime.now()-start
			try:
				pos = nx.spring_layout(H)
				edge_weight=dict([((u,v,),int(d['weight'])) for u,v,d in H.edges(data=True)])
				nx.draw_networkx_edge_labels(H,pos,edge_labels=edge_weight)
				nx.draw_networkx(H,pos,node_color=rcolor[randint(0,3)],font_size=14,linewidths=0,edge_color='#beccd0',font_color="#273d45",)
				plt.show()

			except:
				print "Error drawing Graph"
		except:
			print "Error processing Graph"
			pass
	infile.close()