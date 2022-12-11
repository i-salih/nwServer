from collections import deque
from math import radians, cos, sin, asin, sqrt
from re import L
import json
from flask import Flask, request
import threading

app = Flask(__name__)

adjac_lis = {
    'A1': [('A2', 850)],
    'A2': [('A1', 850), ('A3', 800)],
    'A3': [('A2', 800), ('A4', 1500), ('K7', 4000)],
    'A4': [('A3', 1500), ('A5', 1000)],
    'A5': [('A4', 1000), ('A6', 650)],
    'A6': [('A5', 650), ('A7', 450)],
    'A7': [('A6', 450), ('A8', 750)],
    'A8': [('A7', 750), ('A9', 900)],
    'A9': [('A8', 900), ('A10', 800)],
    'A10': [('A9', 800), ('A11', 1000)],
    'A11':[('A10', 1000)],
    'S1':[('S2', 1500), ('M1', 4000)],
    'S2':[('S1', 1500), ('S3', 950), ('K2', 4000)],
    'S3':[('S2', 950)],
    'K1':[('K2', 1600)],
    'K2':[('K1', 1600), ('S2', 4000), ('K3', 850)],
    'K3':[('K2', 850), ('K4', 850)],
    'K4':[('K3', 850), ('K5', 130)],
    'K5':[('K4', 130), ('K6', 400)],
    'K6':[('K5', 400), ('K7', 1000)],
    'K7':[('K6', 1000), ('K8', 1800),('A3', 4000)],
    'K8':[('K7', 1800)],
    'M1':[('M2', 1600), ('S1', 4000)],
    'M2':[('M1', 1600), ('J1', 4000)],
    'J1':[('J2', 1000), ('M2', 4000)],
    'J2':[('J1', 1000), ('A1', 4000)]
    

}
nodelist=('A1',
'A2',
'A3',
'A4',
'A5',
'A6',
'A7',
'A8',
'A9',
'A10',
'A11',
'S1',
'S2',
'S3',
'K1',
'K2',
'K3',
'K4',
'K5',
'K6',
'K7',
'K8',
'M1',
'M2',
'J1',
'J2'
)
#dictionary of coordinates
nodeco1 = {'A1':[15.533865,32.568341],
'A2':[15.541562,32.567099],
'A3':[15.548515,32.565849],
'A4':[15.561572,32.563714],
'A5':[15.570385,32.562273],
'A6':[15.576129,32.561348],
'A7':[15.579615,32.560732],
'A8':[15.586067,32.559655],
'A9':[15.594209,32.558286],
'A10':[15.601273,32.558096],
'A11':[15.609411,32.553731],
'S1':[15.529986,32.542208], #sahafa
'S2':[15.542931,32.540083], #connects with K muwasalat
'S3':[15.551182,32.538585],
'K1':[15.540909,32.525122], #kahraba
'K2':[15.543079,32.539717],
'K3':[15.544256,32.547277],
'K4':[15.545558,32.555429],
'K5':[15.544511,32.555684],
'K6':[15.546686,32.556122],
'K7':[15.548146,32.565543], #connects to A muwasalat
'K8':[15.557017,32.578654],
'M1':[15.529882,32.542518],
'M2':[15.532171,32.557451],
'J1':[15.532308,32.558569],
'J2':[15.533535,32.567949]
}

#where the pindrop points values will be placed

#finding startnode

#print(final_list)
app = Flask(__name__)
print('reached Flask init')
@app.route('/', methods=['POST'])
def return_routes():
    def handle_sub_view():
        with app.test_request_context():
            req = request
    threading.Thread(target=handle_sub_view).start()
    #print(float(json.loads(request.data)['startLat']))
    #return {"ok":200}
    
    pickup=[]
    dropoff=[]
    pickup.append(float(json.loads(request.data)['startLat']))
    pickup.append(float(json.loads(request.data)['startLong']))
    dropoff.append(float(json.loads(request.data)['endLat']))
    dropoff.append(float(json.loads(request.data)['endLong']))
    #pickup=[15.526665, 32.542315]
    #dropoff=[15.558596, 32.579990]
    #distance from pickup point to node  ------Working
    def nodedist1 (b):
        a=pickup
        bco=nodeco1.get(b)
        radalat=a[0]/57.29577951
        radalon=a[1]/57.29577951
        radblat=bco[0]/57.29577951
        radblon=bco[1]/57.29577951
        dlat=radblat-radalat
        dlon=radblon-radalon
        p = sin(dlat / 2)**2 + cos(radalat) * cos(radblat) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(p))
        r = 6371
        d=c*r
        return d
    #distance between dropoff and node   ------Working
    def nodedist2 (b):
        a=dropoff
        bco=nodeco1.get(b)
        radalat=a[0]/57.29577951
        radalon=a[1]/57.29577951
        radblat=bco[0]/57.29577951
        radblon=bco[1]/57.29577951
        dlat=radblat-radalat
        dlon=radblon-radalon
        p = sin(dlat / 2)**2 + cos(radalat) * cos(radblat) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(p))
        r = 6371
        d=c*r
        return d

    nnode='A6'
    nnnode='A1'
    k=0
    kk=0
    #(works)

    while k<len(nodelist):
        temp=nodelist[k]
        if nodedist1(temp) <nodedist1(nnode):
            nnode=nodelist[k]
        k=k+1
    startnode=nnode

    while kk<len(nodelist):
        temp=nodelist[kk]
        if nodedist2(temp) <nodedist2(nnnode):
            nnnode=nodelist[kk]
        kk=kk+1
    endnode=nnnode


    print('this is ', startnode)
    print('this is ', endnode)
    reconst_path=[]
    class Graph:
        def __init__(self, adjac_lis):
            self.adjac_lis = adjac_lis
    
        def get_neighbors(self, v):
            return self.adjac_lis[v]
    

        def h(self, n):
                curnode=n
                curnodeco=nodeco1.get(curnode)
                endnodeco=nodeco1.get(endnode)
                radcurlat=curnodeco[0]/57.29577951
                radcurlon=curnodeco[1]/57.29577951
                radendlat=endnodeco[0]/57.29577951
                radendlon=endnodeco[1]/57.29577951
                dlat=radendlat-radcurlat
                dlon=radendlon-radcurlon
                a = sin(dlat / 2)**2 + cos(radcurlat) * cos(radendlat) * sin(dlon / 2)**2
                c = 2 * asin(sqrt(a))
                r = 6371
                curdist=c*r
                return curdist
    
        def a_star_algorithm(self, start, stop):
    
            open_lst = set([start])
            closed_lst = set([])
    

            poo = {}
            poo[start] = 0
    
            par = {}
            par[start] = start
    
            while len(open_lst) > 0:
                n = None
    
                for v in open_lst:
                    if n == None or poo[v] + self.h(v) < poo[n] + self.h(n):
                        n = v;
    
                if n == None:
                    #print('Path does not exist!')
                    return None
    
                if n == stop:
    
                    while par[n] != n:
                        reconst_path.append(n)
                        n = par[n]
    
                    reconst_path.append(start)
    
                    reconst_path.reverse()
    
                    print('Path found: {}'.format(reconst_path))  #where the final path is

                    return reconst_path
    
                for (m, weight) in self.get_neighbors(n):

                    if m not in open_lst and m not in closed_lst:
                        open_lst.add(m)
                        par[m] = n
                        poo[m] = poo[n] + weight
    

                    else:
                        if poo[m] > poo[n] + weight:
                            poo[m] = poo[n] + weight
                            par[m] = n
    
                            if m in closed_lst:
                                closed_lst.remove(m)
                                open_lst.add(m)
                

                open_lst.remove(n)
                closed_lst.add(n)
    
            print('Path does not exist!')
            return None


    graph1 = Graph(adjac_lis)
    graph1.a_star_algorithm(startnode, endnode)

    BusA=[]
    BusS=[]
    BusK=[]
    BusM=[]
    BusJ=[]
    z=0
    while z<len(reconst_path):
        if reconst_path[z].find('A') != -1:
            BusA.append(reconst_path[z])
        elif reconst_path[z].find('S') != -1:
            BusS.append(reconst_path[z])
        elif reconst_path[z].find('K') != -1:
            BusK.append(reconst_path[z])
        elif reconst_path[z].find('M') != -1:
            BusM.append(reconst_path[z])
        elif reconst_path[z].find('J') != -1:
            BusJ.append(reconst_path[z])
        z=z+1


    #print(BusJ)
    #print(BusA)
    #print(BusM)
    #final_list = []  #the list of coordinates to be sent to the front
    BusAco=[]
    BusJco=[]
    BusKco=[]
    BusMco=[]
    BusSco=[]

    aBusA=0
    aBusJ=0
    aBusK=0
    aBusM=0
    aBusS=0
    while aBusA<len(BusA): 
        BusAco.append(nodeco1.get(BusA[aBusA]))
        aBusA=aBusA+1
    while aBusJ<len(BusJ): 
        BusJco.append(nodeco1.get(BusJ[aBusJ]))
        aBusJ=aBusJ+1
    while aBusK<len(BusK): 
        BusKco.append(nodeco1.get(BusK[aBusK]))
        aBusK=aBusK+1
    while aBusM<len(BusM): 
        BusMco.append(nodeco1.get(BusM[aBusM]))
        aBusM=aBusM+1
    while aBusS<len(BusS): 
        BusSco.append(nodeco1.get(BusS[aBusS]))
        aBusS=aBusS+1


    final_list=[BusAco,BusJco,BusKco,BusMco,BusSco]#this will actually be done with the coordinate lists
    route_names=[]
    print(final_list)
    zz=0
    #while zz<len(final_list):
    while len(final_list[0])==0:
        for ibus in final_list:
            if len(ibus)<2:
                final_list.remove(ibus)
                
                print('index {} removed with length {} list:{}'.format(zz,len(ibus),ibus))
            else:
                print('list {} not removed:{}'.format(zz,ibus))
            zz=zz+1
    cas=0

    finalpackage={
        "Startride": nodeco1[startnode],
        "Endride": nodeco1[endnode],
        "routes":
            [

            ]
    }
    cor=0
    while cor<len(final_list):
        if final_list[cas]==BusAco:
            routeN='Ebaid Khetim'
        elif final_list[cas]==BusJco:
            routeN='Africa University'
        elif final_list[cas]==BusKco:
            routeN='Kahraba'
        elif final_list[cas]==BusMco:
            routeN='Soug Markazi'
        elif final_list[cas]==BusSco:
            routeN='Sahafa Zalat'
        finalpackage['routes'].append({routeN:final_list[cor]})
        cor=cor+1


    print(final_list)
    print(zz)
    return finalpackage
