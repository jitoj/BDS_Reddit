import networkx as nx
import os
import matplotlib.pyplot as plt

sr_filter=',askreddit,funny,todayilearned,pics,worldnews,science,announcements,explainlikeimfive,askmen,iama,videos,gaming,movies,music,aww,news,gifs,books,television,technology,mildlyinteresting,sports,diy,showerthoughts,bestof,space,fitness,tifu,jokes,wtf,internetisbeautiful,photoshopbattles,history,gadgets,nottheonion,dataisbeautiful,4chan,adviceanimals,twoxchromosomes,earthporn,art,askhistorians,atheism,blackpeopletwitter,comics,conspiracy,creepy,cringe,cringepics,documentaries,europe,facepalm,fffffffuuuuuuuuuuuu,foodporn,freebies,frugal,futurology,gamedeals,games,gentlemanboners,getmotivated,hiphopheads,historyporn,interestingasfuck,justiceporn,lifehacks,listentothis,malefashionadvice,nosleep,oddlysatisfying,oldschoolcool,outoftheloop,pcmasterrace,personalfinance,philosophy,pokemon,politics,reactiongifs,relationships,sex,tattoos,trees,truereddit,wallpapers,youtube,wow,thebutton,'
def print_neighbors(node):
	for item in G.neighbors(node):
		print item

if __name__ == "__main__":
	G=nx.Graph()
	infile = open('../data/usercounts.csv','r')
	#outfile = open('../data/usercounts_split.csv','w+')
	for line in infile:
		line=line.lower()
		data=line.split(',')
		i=2
		while (i<=len(data)-3 and data[1]>1):
			#print i,data[i]+','+data[i+2]#+','+data[i+3]+'\n'
			#outfile.write(data[i]+','+data[i+2]+','+data[i+3]+'\n')
			if ','+data[i].lower()+',' not in sr_filter and ','+data[i+2].lower()+',' not in sr_filter:
				if G.has_edge(data[i], data[i+2]) or G.has_edge(data[i+2], data[i]):
					G.edge[data[i]][data[i+2]]['weight']+=1
				else:
					G.add_edge(data[i],data[i+2],weight=1)

			i+=2
	#outfile.close()
	print "Nodes",G.number_of_nodes()
	print "Edges",G.number_of_edges()
	#print sorted(G.edges(data=True), key=lambda (source,target,data): data['weight'],reverse=True)[:10]
	node="gatech"
	while node!="":
		node=raw_input('Enter subreddit:').lower()
		#print G[node]
		#print_neighbors(node)
		#connected=[]
		try:
			sorted_G=sorted(G[node], key=lambda (target): G[node][target],reverse=True)[:30]
			#connected.append(node)
			H=nx.Graph()
			for i,item in enumerate(sorted_G):
				print ("%10d %-25s %-7d"%(i+1,item, G[node][item]['weight']))
				H.add_edge(node,item,weight=G[node][item]['weight'])
				#connected.append(item)
			try:
				#H = G.subgraph(connected)
				pos = nx.spring_layout(H)
				edge_weight=dict([((u,v,),int(d['weight'])) for u,v,d in H.edges(data=True)])
				nx.draw_networkx_edge_labels(H,pos,edge_labels=edge_weight)
				nx.draw_networkx_nodes(H,pos)
				nx.draw_networkx_edges(H,pos)
				nx.draw_networkx_labels(H,pos)
				nx.draw_networkx(H,pos)
				plt.axis('off')
				plt.show()

			except:
				print "Error drawing Graph"
		except:
			#print "Error processing Graph"
			pass
	infile.close()