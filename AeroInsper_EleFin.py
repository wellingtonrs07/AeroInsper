from math import*
import numpy as np
import datetime as dt

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

        self.vetor_U_reduzido = np.linalg.solve(self.M_K_Global_Reduzida,self.vetor_resultantes_reduzido)

        u_original = np.zeros([2*self.numNos, 1])

        j=0
        for i in range(len(u_original)):
            if i not in self.linhasRemovidas:
                u_original[i] = self.vetor_U_reduzido[j]
                j+=1
        self.Vetor_U = u_original
        self.lista_final_Resultantes = self.M_K_Global @ self.Vetor_U

        self.lista_tensoes=[]
        for i in range(self.numElem):
            u_elemento = np.zeros((4,1))
            coluna = self.Mconect[:,i]
            j=0
            for n in coluna:
                if n== -1:
                    conj1 = j
                if n==1: 
                    conj2 =j
                j+=1
            conjs = [conj1,conj2]
            cont= 0
            x1= self.Mnos[0][conj1]
            x2 = self.Mnos[0][conj2]
            y1= self.Mnos[1][conj1]
            y2 = self.Mnos[1][conj2]
            for conj in conjs:
                u_elemento[(cont*2)] = u_original[conj*2]
                u_elemento[(cont*2)+1] = u_original[(conj*2)+1]
                cont+=1
            cscs = np.zeros((1,4))
            co= (x2 -x1)/self.lista_L[i]
            se= (y2 -y1)/self.lista_L[i]
            cscs[0]=[-co,-se,co,se]
            tens = (self.Elast/self.lista_L[i])*(cscs @ u_elemento)
            self.lista_tensoes.append(tens)

    def exibe_dados(self):
       
        for titulo,dado in self.__dict__.items():
            
            print('\u001b[32m'+titulo + ":"+'\u001b[0m')
            print('\u001b[36;1m',end="")
            if type(dado) != list:
                print(dado)
                print('\u001b[0m',end="")
                print('='*100)
            else:     
                for ddlista in dado:
                    print(ddlista)
                print('\u001b[0m',end="")
                print('='*100)
            
    
        with open("registro.txt",'a') as reg:
            reg.write(('====='+str(dt.date.today()) + "=====\n"))
            for titulo,dado in self.__dict__.items():
                    reg.write((str(titulo).upper() + ": \n"))
                    if type(dado) != list:
                        reg.write(('\n'+ str(dado)+'\n'))
                    else:
                        for ddlista in dado:
                            reg.write((str(ddlista)+'\n'))
                    reg.write("="*100 + '\n')

            reg.close()

        return









            
