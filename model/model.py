import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.DiGraph()
        self._idMap = {}
        self._idMapNome = {}

    def creaGrafo(self, prezzo):
        self.nodi = DAO.getNodi(prezzo)
        self.grafo.add_nodes_from(self.nodi)
        for v in self.nodi:
            self._idMap[v.AlbumId] = v
        for v in self.nodi:
            self._idMapNome[v.Title] = v
        self.addEdges(prezzo)
        return self.grafo

    def getNumNodes(self):
        return len(self.grafo.nodes)

    def getNumEdges(self):
        return len(self.grafo.edges)

    def addEdges(self, prezzo):
        self.grafo.clear_edges()
        allEdges = DAO.getConnessioni(prezzo)
        for connessione in allEdges:
            nodo1 = self._idMap[connessione.v1]
            nodo2 = self._idMap[connessione.v2]
            if nodo1 in self.grafo.nodes and nodo2 in self.grafo.nodes and nodo1!=nodo2:
                if self.grafo.has_edge(nodo1, nodo2) == False:
                    if connessione.peso>0:
                        self.grafo.add_edge(nodo1, nodo2, weight=connessione.peso)
                    if connessione.peso<0:
                        self.grafo.add_edge(nodo2, nodo1, weight=abs(connessione.peso))

    def getBilancio(self, a1Titolo):
        album=self._idMapNome[a1Titolo]
        lista=[]
        print(album.AlbumId)
        for nodo in self.grafo.successors(album):
            print("ciao")
            lista.append((nodo.Title,self.bilancio(nodo)))
            print(nodo)
        for nodo in self.grafo.predecessors(album):
            print("ciao")
            lista.append((nodo.Title,self.bilancio(nodo)))
            print(nodo)
        return sorted(lista, key=lambda x:x[1], reverse=True)


    def bilancio(self,nodo):
        print(nodo)
        numeroArchi=self.grafo.degree(nodo)
        somma=0
        for arco in self.grafo.in_edges(nodo):
            somma+=self.grafo[arco[0]][arco[1]]["weight"]
        for arco in self.grafo.out_edges(nodo):
            somma+=self.grafo[arco[0]][arco[1]]["weight"]
        print(somma)
        print(numeroArchi)
        return somma/numeroArchi