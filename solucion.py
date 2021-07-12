import numpy as np 


class Solucion():
    def __init__(self, datos_entrada):
        self.datos = datos_entrada # Diccionario con datos

        nudo_1 = Nudos(1,0, self.datos['valor_B'])
        nudo_2 = Nudos(2, self.datos['valor_A'], self.datos['valor_B'])
        nudo_3 = Nudos(3, self.datos['valor_A'], 0)

        nudos = {}
        nudos[1] = nudo_1
        nudos[2] = nudo_2
        nudos[3] = nudo_3

        elementos = {}
        elemento_1 = Elementos(1, nudos[1], nudos[2], self.datos['valor_E'], self.datos['valor_Ar'], self.datos['valor_I'])
        elemento_2 = Elementos(2, nudos[2], nudos[3], self.datos['valor_E'], self.datos['valor_Ar'], self.datos['valor_I'])

        elementos[1] = elemento_1
        elementos[2] = elemento_2

        # Cargas Aplicadas directamente en los nudos
        cargas = [0] * 9
        cargas[0] = self.datos['valor_Fx1']
        cargas[1] = self.datos['valor_Fy1']
        cargas[3] = self.datos['valor_Fx2']
        cargas[4] = self.datos['valor_Fy2']
        cargas[6] = self.datos['valor_Fx3']
        cargas[7] = self.datos['valor_Fy3']





        # Cargas Ingresadas
        w1 = self.datos['valor_w1']
        w2 = self.datos['valor_w2']
        p1 = self.datos['valor_p1']
        p2 = self.datos['valor_p2']

        #Longitudes
        long_A = self.datos['valor_A']
        long_B = self.datos['valor_B']

        # Vector Solucion Particular
        sol_particular = [0] * 9
        # Cargas Distribuidas
        # Elemento 1
        # Nudo Inicial
        rx1 = 0
        ry1 = w1*long_A/2
        m1 =  w1*long_A**2/12

        sol_particular[0] += rx1
        sol_particular[1] += ry1
        sol_particular[2] += m1
        # Nudo Final
        rx2_1 = 0
        ry2_1 = w1*long_A/2
        m2_1 = -w1*long_A**2/12

        sol_particular[3] += rx2_1
        sol_particular[4] += ry2_1
        sol_particular[5] += m2_1

        # Elemento 2
        # Nudo Inicial
        rx2 = w2*long_B/2
        ry2 = 0
        m2 = w2*long_B**2/12
        sol_particular[3] += rx2
        sol_particular[4] += ry2
        sol_particular[5] += m2

        # Nudo Final
        rx3 = w2*long_B/2
        ry3 = 0
        m3 = -w2*long_B**2/12

        sol_particular[6] += rx3
        sol_particular[7] += ry3
        sol_particular[8] += m3

        # Cargas Puntuales
        # Elemento 1
        p1 = self.datos['valor_p1']
        a1 = self.datos['valor_a1']
        b1 = self.datos['valor_b1']

        m1 = p1*a1*b1**2/long_A**2
        m2 = - p1*a1**2*b1/long_A**2
        ry1 = p1*b1/long_A + (m1 - m2)/long_A
        ry2 = p1*a1/long_A - (m1 - m2)/long_A
        rx1 = 0
        ry1 =0

        sol_particular[0] += rx1
        sol_particular[1] += ry1
        sol_particular[2] += m1
        sol_particular[3] += rx2
        sol_particular[4] += ry2
        sol_particular[5] += m2

        # Elemento 2
        p2 = self.datos['valor_p2']
        a2 = self.datos['valor_a2']
        b2 = self.datos['valor_b2']

        m2 = p2*a2*b2**2/long_B**2
        m3 = - p2*a2**2*b2/long_B**2
        ry2 = 0
        ry3 = 0
        rx2 = p2*b2/long_B + (m2 - m3)/long_B
        rx3 =p2*a2/long_B - (m2 - m3)/long_B

        sol_particular[3] += rx2
        sol_particular[4] += ry2
        sol_particular[5] += m2
        sol_particular[6] += rx3
        sol_particular[7] += ry3
        sol_particular[8] += m3

        print(sol_particular)

        

        # Reacciones en el Vector de Fuerzas
        fuerzas = [0, 'Ry1',0,  0, 0, 0, 'Rx3', 'Ry3', 'M3']
        vector_fuerzas = self.convertir_arrays(fuerzas)
        # Desplazamientos en el Vector de los Desplazamientos
        desplazamientos = ['U1', 0, 'rot1', 'U2','V2','rot2', 0, 0, 0]
        vector_desplazamientos = self.convertir_arrays(desplazamientos)

        #print(structure.frames[2].glob_stiff_matrix)

        marco = Estructura(nudos, elementos, fuerzas, desplazamientos, cargas, sol_particular)
        self.desplazamientos = marco.get_desplazamientos()
        self.reacciones = marco.get_reacciones()

    def resolver(self):
        return 'Problema resuelto'

    def convertir_arrays(self, vector):
        arreglo = np.array([vector]).transpose()
        print(arreglo.shape)
        return arreglo

    def get_desplazamientos(self):
        return self.desplazamientos

    def get_reacciones(self):
        return self.reacciones

            

class Estructura():
    def __init__(self, nudos, elementos,fuerzas, desplazamientos, cargas, sol_particular):
        self.nudos = nudos
        self.elementos = elementos
        self.estructura_matriz_rigidez = self.construir_matriz_rigidez_estructura() # Array Numpy [K]
        print('MATRIZ DE RIGIDEZ DE LA ESTRUCTURA')
        print(self.estructura_matriz_rigidez)
        self.vector_fuerzas = fuerzas
        self.vector_desplazamientos = desplazamientos
        self.sol_particular = sol_particular
        self.vector_cargas = cargas
        print('VECTOR DE LAS FUERZAS')
        print(self.vector_fuerzas)
        print('VECTOR DE LOS DESPLAZAMIENTOS')
        print(self.vector_desplazamientos)
        print('VECTOR DE LAS CARGAS')
        print(self.vector_cargas)
        # Submatrices
        self.KFF = self.build_submatrix_KFF()
        print('SUBMATRIZ KFF')
        print(self.KFF)
        self.inverse_KFF = np.linalg.inv(self.KFF)
        print('SUBMATRIZ INVERSA KFF')
        print(self.inverse_KFF)
        self.FF = self.build_subvector_FF()
        print('SUBVECTOR FF')
        print(self.FF)
        print('SUBVECTOR TF')
        self.TF = self.build_subvector_TF()
        print(self.TF)
        self.SPF = self.build_subvector_SPF()
        print('SUBVECTOR SPF')
        print(self.SPF)
        self.DF = self.calcular_desplazamientos_desconocidos()
        print('SUBVECTOR DESPLAZAMIENTOS DESCONOCIDOS')
        print(self.DF)
        self.KSF = self.build_submatrix_KSF()
        print("KSF")
        print(self.KSF)
        self.SPS = self.build_subvector_SPS()
        print('TS')
        self.TS = self.build_subvector_TS()
        print(self.TS)
        print('SPS')
        print(self.SPS)
        self.FS = self.calcular_reacciones()
        print('FS')
        print(self.FS)





    def construir_matriz_rigidez_estructura(self):
        stiffness_matrix_glob = np.zeros((3*len(self.nudos.keys()), 3*len(self.nudos.keys()))) # Numpy Array
        for key in self.elementos:
            #print(self.elementos[key].glob_stiff_matrix)
            kg = self.elementos[key].matriz_rigidez_global

            #print(f'kg = {kg}')
            Ni = int(self.elementos[key].nudo_inicio.id_nudo)
            #print(Ni)
            Nj = int(self.elementos[key].nudo_fin.id_nudo)
            #print(Nj)
            # Primera Fila
            stiffness_matrix_glob[(3*Ni-2)-1, (3*Ni-2)-1] += kg[0][0]
            stiffness_matrix_glob[(3*Ni-2)-1, (3*Ni-1)-1] +=  kg[0][1]
            stiffness_matrix_glob[(3*Ni-2)-1, (3*Ni)-1] += kg[0][2]
            stiffness_matrix_glob[(3*Ni-2)-1, (3*Nj-2)-1] += kg[0][3]
            stiffness_matrix_glob[(3*Ni-2)-1, (3*Nj-1)-1] += kg[0][4]
            stiffness_matrix_glob[(3*Ni-2)-1, (3*Nj)-1] += kg[0][5]
            # Segunda Fila
            stiffness_matrix_glob[(3*Ni-1)-1, (3*Ni-2)-1] += kg[1][0]
            stiffness_matrix_glob[(3*Ni-1)-1, (3*Ni-1)-1] += kg[1][1]
            stiffness_matrix_glob[(3*Ni-1)-1, (3*Ni)-1] += kg[1][2]
            stiffness_matrix_glob[(3*Ni-1)-1, (3*Nj-2)-1] += kg[1][3]
            stiffness_matrix_glob[(3*Ni-1)-1, (3*Nj-1)-1] += kg[1][4]
            stiffness_matrix_glob[(3*Ni-1)-1, (3*Nj)-1] += kg[1][5]

            # Tercera Fila
            stiffness_matrix_glob[(3*Ni)-1, (3*Ni-2)-1] += kg[2][0]
            stiffness_matrix_glob[(3*Ni)-1, (3*Ni-1)-1] += kg[2][1]
            stiffness_matrix_glob[(3*Ni)-1, (3*Ni)-1] += kg[2][2]
            stiffness_matrix_glob[(3*Ni)-1, (3*Nj-2)-1] += kg[2][3]
            stiffness_matrix_glob[(3*Ni)-1, (3*Nj-1)-1] += kg[2][4]
            stiffness_matrix_glob[(3*Ni)-1, (3*Nj)-1] += kg[2][5]

            # Cuarto Fila
            stiffness_matrix_glob[(3*Nj-2)-1, (3*Ni-2)-1] += kg[3][0]
            stiffness_matrix_glob[(3*Nj-2)-1, (3*Ni-1)-1] += kg[3][1]
            stiffness_matrix_glob[(3*Nj-2)-1, (3*Ni)-1] += kg[3][2]
            stiffness_matrix_glob[(3*Nj-2)-1, (3*Nj-2)-1] += kg[3][3]
            stiffness_matrix_glob[(3*Nj-2)-1, (3*Nj-1)-1] += kg[3][4]
            stiffness_matrix_glob[(3*Nj-2)-1, (3*Nj)-1] += kg[3][5]

            # Quinta Fila
            stiffness_matrix_glob[(3*Nj-1)-1, (3*Ni-2)-1] += kg[4][0]
            stiffness_matrix_glob[(3*Nj-1)-1, (3*Ni-1)-1] += kg[4][1]
            stiffness_matrix_glob[(3*Nj-1)-1, (3*Ni)-1] += kg[4][2]
            stiffness_matrix_glob[(3*Nj-1)-1, (3*Nj-2)-1] += kg[4][3]
            stiffness_matrix_glob[(3*Nj-1)-1, (3*Nj-1)-1] += kg[4][4]
            stiffness_matrix_glob[(3*Nj-1)-1, (3*Nj)-1] += kg[4][5]

            # Sexta Fila
            stiffness_matrix_glob[(3*Nj)-1, (3*Ni-2)-1] += kg[5][0]
            stiffness_matrix_glob[(3*Nj)-1, (3*Ni-1)-1] += kg[5][1]
            stiffness_matrix_glob[(3*Nj)-1, (3*Ni)-1] += kg[5][2]
            stiffness_matrix_glob[(3*Nj)-1, (3*Nj-2)-1] += kg[5][3]
            stiffness_matrix_glob[(3*Nj)-1, (3*Nj-1)-1] += kg[5][4]
            stiffness_matrix_glob[(3*Nj)-1, (3*Nj)-1] += kg[5][5]


        return stiffness_matrix_glob

    def extract_indexes_F(self):
        indexes_KFF = []
        for desplazamiento in self.vector_desplazamientos:
            #print(desplazamiento)
            if isinstance(desplazamiento, str):
                indexes_KFF.append(self.vector_desplazamientos.index(desplazamiento))

        return indexes_KFF

    def extract_indexes_S(self):
        indexes_KSF = []
        for num, desplazamiento in enumerate(self.vector_desplazamientos):
            #print('tipos')
            #print(type(desplazamiento))
            if isinstance(desplazamiento,int):
                indexes_KSF.append(num)
        
        return indexes_KSF


    def build_submatrix_KFF(self):
        # Submatrix [KFF]
        
        indexes_KFF = self.extract_indexes_F()
        #print(indexes_KFF)
        KFF = np.zeros((len(indexes_KFF), len(indexes_KFF)))
        row = 0
        for i in indexes_KFF:
            column = 0
            for j in indexes_KFF:
                KFF[row,column] = self.estructura_matriz_rigidez[i,j]
                column += 1
            row += 1


        return KFF

    def build_submatrix_KSF(self):
        # subvector {KSF}
        indexes_KFF = self.extract_indexes_F()
        indexes_KSF = self.extract_indexes_S()
        print('INDEX KFF')
        print(indexes_KFF)
        print('INDEX KSF')
        print(indexes_KSF)
        KSF = np.zeros((len(indexes_KSF), len(indexes_KFF)))
        row = 0
        for i in indexes_KSF:
            column = 0
            for j in indexes_KFF:
                KSF[row, column] = self.estructura_matriz_rigidez[i,j]
                column += 1
            row += 1

        return KSF



    def build_subvector_SPF(self):
        # Subvector {SPF}
        indexes_KFF = self.extract_indexes_F()

        SPF = np.zeros((len(indexes_KFF), 1))
        row = 0
        for i in indexes_KFF:
            SPF[row, 0] = self.sol_particular[i]
            row += 1
        return SPF

    def build_subvector_SPS(self):
        # Subvector {SPS}
        indexes_KFS = self.extract_indexes_S()
        print(indexes_KFS)
        SPS = np.zeros((len(indexes_KFS), 1))
        row = 0
        for i in indexes_KFS:
            SPS[row, 0] = self.sol_particular[i]
            row += 1
        return SPS

    def build_subvector_FF(self):
        # Subvector {FF}
        indexes_KFF = self.extract_indexes_F()
            
        FF = np.zeros((len(indexes_KFF), 1))
        #print(indexes_KFF)
        row = 0
        for i in indexes_KFF:
            FF[row,0] = self.vector_fuerzas[i]
            row += 1
        return FF

    def build_subvector_TF(self):
        # Subvector {TF}
        indexes_KFF = self.extract_indexes_F()

        TF = np.zeros((len(indexes_KFF), 1))
        print(indexes_KFF)
        row = 0
        for i in indexes_KFF:
            #print(self.forces_vector[i])
            TF[row,0] = self.vector_cargas[i]
            row += 1
        return TF

    def build_subvector_TS(self):
        # Subvector {TF}
        indexes_KFS = self.extract_indexes_S()

        TS = np.zeros((len(indexes_KFS), 1))
        #print(indexes_KFS)
        row = 0
        for i in indexes_KFS:
            #print(self.forces_vector[i])
            TS[row,0] = self.vector_cargas[i]
            row += 1
        return TS

    def calcular_desplazamientos_desconocidos(self):
        # {DF} unknown displacements

        # numpy array: {AF} = {FF} + {TF} 
        #F = np.zeros((len(self.FF)),1)
        
        #print(AF)
        neg_SPF = - self.SPF
        AF = np.add(self.TF,neg_SPF)
        print('AF')
        print(AF)
        DF = np.dot(self.inverse_KFF,AF)

        return DF

    def calcular_reacciones(self):
        # {FS} unknown displacements

        SR1 = np.dot(self.KSF, self.DF)
        FS = np.add(SR1, self.SPS)
        SR2 = np.add(FS, -self.TS)


        return SR2

    def get_desplazamientos(self):
        dic_desplazamientos = {}
        indexes_KFF = self.extract_indexes_F()
        for num in range(len(indexes_KFF)):
            dic_desplazamientos[self.vector_desplazamientos[indexes_KFF[num]]] = self.DF[num][0]
        return dic_desplazamientos

    def get_reacciones(self):
        dic_reacciones = {}
        indexes_KSF = self.extract_indexes_S()
        for num in range(len(indexes_KSF)):
            dic_reacciones[self.vector_fuerzas[indexes_KSF[num]]] = self.FS[num][0]
        return dic_reacciones





class Nudos():
    def __init__(self,id_nudo,coor_x,coor_y):
        self.id_nudo = id_nudo
        self.coor_x = coor_x
        self.coor_y = coor_y

class Elementos():
    def __init__(self, id_elemento, nudo_inicio, nudo_fin, modulo_elas, area, inercia):
        self.id_elemento = id_elemento
        self.nudo_inicio = nudo_inicio
        self.nudo_fin = nudo_fin
        self.modulo_elas = modulo_elas
        self.area = area
        self.inercia = inercia
        self.longitud = self.calcular_longitud()
        self.coseno = self.calcular_coseno()
        print(f'COSENO = {self.coseno}')
        self.seno = self.calcular_seno()
        print(f'SENO = {self.seno}')

        self.matriz_rigidez_global = self.construir_matriz_global_rigidez()
        print(f'ELEMENTO No. {self.id_elemento}')
        print(self.matriz_rigidez_global)

    def calcular_longitud(self):
        # Nudo Inicial
        inicio = self.nudo_inicio.id_nudo
        x_inicio = self.nudo_inicio.coor_x
        y_inicio = self.nudo_inicio.coor_y

        # Nudo Fin
        fin = self.nudo_fin.id_nudo
        x_fin = self.nudo_fin.coor_x
        y_fin = self.nudo_fin.coor_y

        # Calcular longitud
        elemento_longitud = ((y_fin - y_inicio)**2 + (x_fin - x_inicio)**2)**(0.5)
        return elemento_longitud

    def calcular_coseno(self):
        # Longitud
        _longitud = self.longitud
        # Nudo Inicial
        x_inicio = self.nudo_inicio.coor_x

        # Nudo Final
        x_fin = self.nudo_fin.coor_x

        # Calcular Coseno
        coseno = (x_fin - x_inicio) / _longitud
        return coseno

    def calcular_seno(self):
        # Longitud
        _longitud = self.longitud
        # Nudo Inicial
        y_inicio =self.nudo_inicio.coor_y



        # Nudo Final
        y_fin = self.nudo_fin.coor_y

        # Calcular Seno
        seno = (y_fin - y_inicio) / _longitud
        return seno

    def construir_matriz_global_rigidez(self):
        matriz_rigidez = []

        # Primera Fila
        primera_fila = []
        primera_fila.append(self.area*self.modulo_elas/self.longitud * self.coseno**2 + 12*self.modulo_elas*self.inercia/self.longitud**3*self.seno**2)
        primera_fila.append((self.area*self.modulo_elas/self.longitud - 12*self.modulo_elas*self.inercia/(self.longitud**3))*self.coseno*self.seno)
        primera_fila.append(-6*self.modulo_elas*self.inercia/self.longitud**2 * self.seno)
        primera_fila.append(-(self.area*self.modulo_elas/self.longitud * self.coseno**2 + 12*self.modulo_elas*self.inercia/(self.longitud**3)*self.seno**2))
        primera_fila.append(-(self.area*self.modulo_elas/self.longitud - 12*self.modulo_elas*self.inercia/self.longitud**3)*self.coseno*self.seno)
        primera_fila.append(-6*self.modulo_elas*self.inercia/self.longitud**2*self.seno)

        matriz_rigidez.append(primera_fila)

        #Segunda Fila
        segunda_fila = []
        segunda_fila.append((self.area*self.modulo_elas/self.longitud - 12*self.modulo_elas*self.inercia/self.longitud**3)*self.coseno*self.seno)
        segunda_fila.append(self.area*self.modulo_elas/self.longitud*self.seno**2 + 12*self.modulo_elas*self.inercia/self.longitud**3 * self.coseno**2)
        segunda_fila.append(6*self.modulo_elas*self.inercia/self.longitud**2*self.coseno)
        segunda_fila.append(-((self.area*self.modulo_elas/self.longitud - 12*self.modulo_elas*self.inercia/self.longitud**3)*self.coseno*self.seno))
        segunda_fila.append(-(self.area*self.modulo_elas/self.longitud*self.seno**2 + 12*self.modulo_elas*self.inercia/self.longitud**3 * self.coseno**2))
        segunda_fila.append(6*self.modulo_elas*self.inercia/self.longitud**2*self.coseno)

        matriz_rigidez.append(segunda_fila)

        # Tercer Fila
        tercera_fila = []
        tercera_fila.append(-6*self.modulo_elas*self.inercia/self.longitud**2 * self.seno)
        tercera_fila.append(6*self.modulo_elas*self.inercia/self.longitud**2 * self.coseno)
        tercera_fila.append(4*self.modulo_elas*self.inercia/self.longitud)
        tercera_fila.append(6*self.modulo_elas*self.inercia/self.longitud**2 * self.seno)
        tercera_fila.append(-6*self.modulo_elas*self.inercia/self.longitud**2 * self.coseno)
        tercera_fila.append(2*self.modulo_elas*self.inercia/self.longitud)

        matriz_rigidez.append(tercera_fila)


        # Cuarta Fila
        cuarta_fila = []
        cuarta_fila.append(-(self.modulo_elas*self.area/self.longitud*self.coseno**2 + 12*self.modulo_elas*self.inercia/self.longitud**3*self.seno**2))
        cuarta_fila.append(-((self.modulo_elas*self.area/self.longitud - 12*self.modulo_elas*self.inercia/self.longitud**3)*self.coseno*self.seno))
        cuarta_fila.append(6*self.modulo_elas*self.inercia/self.longitud**2 * self.seno)
        cuarta_fila.append(self.modulo_elas*self.area/self.longitud*self.coseno + 12*self.modulo_elas*self.inercia/self.longitud**3*self.seno)
        cuarta_fila.append((self.modulo_elas*self.area/self.longitud - 12*self.modulo_elas*self.inercia/self.longitud**3)*self.coseno*self.seno)
        cuarta_fila.append(6*self.modulo_elas*self.inercia/self.longitud**2 * self.seno)

        matriz_rigidez.append(cuarta_fila)


        # Quinta Fila
        quinta_fila = []
        quinta_fila.append(-((self.modulo_elas*self.area/self.longitud - 12*self.modulo_elas*self.inercia/self.longitud**3)*self.coseno*self.seno))
        quinta_fila.append(-(self.modulo_elas*self.area/self.longitud*self.seno**2 + 12*self.modulo_elas*self.inercia/self.longitud**3*self.coseno**2))
        quinta_fila.append(-6*self.modulo_elas*self.inercia/self.longitud**2*self.coseno)
        quinta_fila.append((self.modulo_elas*self.area/self.longitud - 12*self.modulo_elas*self.inercia/self.longitud**3)*self.coseno*self.seno)
        quinta_fila.append(self.modulo_elas*self.area/self.longitud*self.seno**2 + 12*self.modulo_elas*self.inercia/self.longitud**3*self.coseno**2)
        quinta_fila.append(-6*self.modulo_elas*self.inercia/self.longitud**2*self.coseno)

        matriz_rigidez.append(quinta_fila)


        # Sexta Fila
        sexta_fila = []
        sexta_fila.append(-6*self.modulo_elas*self.inercia/self.longitud**2 * self.seno)
        sexta_fila.append(6*self.modulo_elas*self.inercia/self.longitud**2 * self.coseno)
        sexta_fila.append(2*self.modulo_elas*self.inercia/self.longitud)
        sexta_fila.append(6*self.modulo_elas*self.inercia/self.longitud**2 * self.seno)
        sexta_fila.append(-6*self.modulo_elas*self.inercia/self.longitud**2 * self.coseno)
        sexta_fila.append(4*self.modulo_elas*self.inercia/self.longitud)

        matriz_rigidez.append(sexta_fila)

        return matriz_rigidez

class Reactions():
    def __init__(self, id_joint,rx, ry):
        self.id_joint = id_joint
        self.rx = rx
        self.ry = ry




