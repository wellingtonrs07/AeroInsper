from AeroInsper_EleFin import *
import numpy as np


#INSERE OS NÓS
'''Exemplo: [x0,x1,x2]
            [y0,y1,y2]
'''
mn= np.array( [ 
    [ 0,   0, 0.3 ] ,
    [ 0, 0.4, 0.4 ]
                ])

#INSERE ELEMENTOS
'''Exemplo: [n° do nó inicial , n° do nó final] pra cada elemento
            [n° do nó inicial , n° do nó final] pra cada elemento
'''
el = np.array( [
    [0,1],
    [1,2],
    [2,0]
    ])

#INSERE FORÇAS

r1x = None 
r1y = 0
r2x = None
r2y = None
r3x = 150
r3y = -100

Res = [r1x,r1y,r2x,r2y,r3x,r3y]

Marea = np.ones([len(mn[0]),1]) * 2e-4 #área da secção transversal (m²)

Elast = 210e9

Teste1 = Corpo(mn,el,Res,Marea,Elast)

print(Teste1.__dict__)