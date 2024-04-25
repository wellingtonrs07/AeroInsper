from math import*
import numpy as np

class Corpo:
    def __init__(self,matriz_dos_nos,elementos,listaRes,matriz_areas,Elast):
        self.Mnos = matriz_dos_nos
        self.numNos = len(self.Mnos[0])
        self.numElem = len(elementos)
        self.listaResultantes= listaRes
        self.Elast = Elast
        self.M_areas = matriz_areas

        self.linhasRemovidas = []
        for val,i in zip(self.listaResultantes,range(len(self.listaResultantes))):
            if val == None:
                self.linhasRemovidas.append(i)

        Listafinal_R=[]
        for val in self.listaResultantes:
            if val != None:
                Listafinal_R.append(val)

        self.vetor_resultantes_incompleta = np.array(Listafinal_R)
        self.vetor_resultantes_incompleta.shape = (len(Listafinal_R), 1)

        self.Mconect = np.zeros((self.numNos,self.numElem))
        for elemento,i in zip(elementos,range(self.numElem)):
            self.Mconect[elemento[0]][i] = -1
            self.Mconect[elemento[1]][i] = 1
        
        self.Mmembros = self.Mnos @ self.Mconect

        self.lista_L = []
        self.lista_matriz_S = []
            
        for i in range(self.numNos):
            
            L = np.linalg.norm(self.Mmembros[:,i])
            self.lista_L.append(L)
            c = self.Mmembros[:,i]
            c.shape = [2,1]
            matriz_S = ((self.Elast * self.M_areas[i,0])/L) * ((c) @ (c.T)) / (L**2)
            self.lista_matriz_S.append(matriz_S)
    


        









            
