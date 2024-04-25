from math import*
import numpy as np

class Corpo:
    def __init__(self,matriz_dos_nos,elementos,listaRes,matriz_areas,Elast):
        self.Mnos = matriz_dos_nos
        self.numNos = len(self.Mnos[0])
        self.numElem = len(elementos)
        self.lista_Inicial_Resultantes= listaRes
        self.Elast = Elast
        self.M_areas = matriz_areas

        self.linhasRemovidas = []
        for val,i in zip(self.lista_Inicial_Resultantes,range(len(self.lista_Inicial_Resultantes))):
            if val == None:
                self.linhasRemovidas.append(i)

        Listafinal_R=[]
        for val in self.lista_Inicial_Resultantes:
            if val != None:
                Listafinal_R.append(val)

        self.vetor_resultantes_reduzido = np.array(Listafinal_R)
        self.vetor_resultantes_reduzido.shape = (len(Listafinal_R), 1)
        self.Mconect = np.zeros((self.numNos,self.numElem))

        for elemento,i in zip(elementos,range(self.numElem)):
            self.Mconect[elemento[0]][i] = -1
            self.Mconect[elemento[1]][i] = 1
        
        self.Mmembros = self.Mnos @ self.Mconect

        self.lista_L = []
        self.lista_matriz_S = []
            
        for i in range(self.numElem):
            
            L = np.linalg.norm(self.Mmembros[:,i])
            self.lista_L.append(L)
            c = self.Mmembros[:,i]
            c.shape = [2,1]
            matriz_S = ((self.Elast * self.M_areas[i,0])/L) * ((c) @ (c.T)) / (L**2)
            self.lista_matriz_S.append(matriz_S)
        
        matriz_G = 0

        for j in range(self.numElem):

            t = self.Mconect[:,j]
            t.shape = [3,1]
            
            K = np.kron(((t) @ (t.T)), self.lista_matriz_S[j])
            matriz_G += K
        self.M_K_Global = matriz_G
    
        i=0
        for linha in self.linhasRemovidas:
            matriz_G = np.delete(matriz_G, linha-i, axis=0)  # Removendo a linha
            matriz_G = np.delete(matriz_G, linha-i, axis=1)  # Removendo a coluna
            i+=1
        self.M_K_Global_Reduzida = matriz_G

        









            
