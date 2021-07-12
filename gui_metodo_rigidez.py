import sys

from solucion import Solucion

from PyQt5.QtWidgets import (QApplication,
                              QMainWindow,
                              QPushButton,
                              QLabel,
                              QVBoxLayout,
                              QGridLayout,
                              QWidget,
                              QLineEdit,
                              QDialog,
                              QTableWidget,
                              QTableWidgetItem)

class ResultadossWindow(QWidget):
    def __init__(self, desplazamientos, reacciones):
        super().__init__()

        layout = QVBoxLayout()

        self.lbl_titulo = QLabel('Desplazamientos')
        layout.addWidget(self.lbl_titulo)
        self.table_desplazamientos = QTableWidget()
        self.table_desplazamientos.setRowCount(len(desplazamientos))
        self.table_desplazamientos.setColumnCount(2)
        self.table_desplazamientos.setHorizontalHeaderLabels(['Desplazamiento', 'Resultado'])
        layout.addWidget(self.table_desplazamientos)

        self.lbl_reacciones = QLabel('Reacciones')
        layout.addWidget(self.lbl_reacciones)
        self.table_reacciones = QTableWidget()
        self.table_reacciones.setRowCount(len(reacciones))
        self.table_reacciones.setColumnCount(2)
        self.table_reacciones.setHorizontalHeaderLabels(['Reaccion', 'Resultado'])
        layout.addWidget(self.table_reacciones)

        self.setLayout(layout)


        # Imprimir resultados en Table
        contador = 0
        for key, value in desplazamientos.items():
            self.table_desplazamientos.setItem(contador, 0, QTableWidgetItem(key))
            self.table_desplazamientos.setItem(contador, 1, QTableWidgetItem(str(round(value,4))))
            contador += 1

        # Imprimir reacciones en Table
        contador = 0
        for key, value in reacciones.items():
            self.table_reacciones.setItem(contador, 0, QTableWidgetItem(key))
            self.table_reacciones.setItem(contador, 1, QTableWidgetItem(str(round(value,2))))
            contador += 1


    


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.w = None # No hay ventana secundaria todavia

        layout = QVBoxLayout()
        layout1 = QGridLayout()
        layout2 = QGridLayout()
        layout3 = QGridLayout()
        layout4 = QGridLayout()

        lbl_titulo = QLabel('Marco Estructural - Método de Rigidez')
        layout.addWidget(lbl_titulo)
        lbl_datos = QLabel('Datos de Entrada: ')
        layout.addWidget(lbl_datos)

        # Longitud A
        lbl_A =QLabel('A = ')
        self.txt_A = QLineEdit()
        layout1.addWidget(lbl_A, 0, 0)
        layout1.addWidget(self.txt_A, 0, 1)

        # Longitud B
        lbl_B = QLabel('B = ')
        self.txt_B = QLineEdit()
        layout1.addWidget(lbl_B, 1, 0)
        layout1.addWidget(self.txt_B,1,1)

        # Area de los ELementos
        lbl_Ar = QLabel('Ar = ')
        self.txt_Ar = QLineEdit()
        layout1.addWidget(lbl_Ar, 2, 0)
        layout1.addWidget(self.txt_Ar, 2, 1)

        # Modulo de Elasticidad
        lbl_E = QLabel('E = ')
        self.txt_E = QLineEdit()
        layout1.addWidget(lbl_E, 3, 0)
        layout1.addWidget(self.txt_E,3,1)

        # Inercia
        lbl_I = QLabel('I = ')
        self.txt_I = QLineEdit()
        layout1.addWidget(lbl_I, 4, 0)
        layout1.addWidget(self.txt_I, 4, 1)

        layout.addLayout(layout1)

        #Cargas Aplicadas en los Nudos
        lbl_carga_nudos = QLabel('Cargas Aplicadas en Nudos')
        layout.addWidget(lbl_carga_nudos)
        lbl_Fx1 = QLabel('Fx1 =')
        self.txt_Fx1 = QLineEdit()
        lbl_Fy1 = QLabel('Fy1 =')
        self.txt_Fy1 = QLineEdit()
        lbl_Fx2 = QLabel('Fx2 =')
        self.txt_Fx2 = QLineEdit()
        lbl_Fy2 = QLabel('Fy2 =')
        self.txt_Fy2 = QLineEdit()
        lbl_Fx3 = QLabel('Fx3 =')
        self.txt_Fx3 = QLineEdit()
        lbl_Fy3 = QLabel('Fy3 =')
        self.txt_Fy3 = QLineEdit()
       
        layout4.addWidget(lbl_Fx1, 1, 0)
        layout4.addWidget(self.txt_Fx1, 1,1)
        layout4.addWidget(lbl_Fy1, 2, 0)
        layout4.addWidget(self.txt_Fy1, 2,1)
        layout4.addWidget(lbl_Fx2, 3, 0)
        layout4.addWidget(self.txt_Fx2, 3,1)
        layout4.addWidget(lbl_Fy2, 4, 0)
        layout4.addWidget(self.txt_Fy2, 4,1)
        layout4.addWidget(lbl_Fx3, 5, 0)
        layout4.addWidget(self.txt_Fx3, 5,1)
        layout4.addWidget(lbl_Fy3, 6, 0)
        layout4.addWidget(self.txt_Fy3, 6,1)
        
        layout.addLayout(layout4)
        

        # Cargas Distribuidas
        lbl_carga_dist = QLabel('Cargas Distribuidas')
        layout.addWidget(lbl_carga_dist)

        lbl_w1 = QLabel('w1 = ')
        self.txt_w1 = QLineEdit()
        lbl_w2 = QLabel('w2 = ')
        self.txt_w2 = QLineEdit()
        
        layout2.addWidget(lbl_w1, 1, 0)
        layout2.addWidget(self.txt_w1, 1, 1)
        layout2.addWidget(lbl_w2, 2, 0)
        layout2.addWidget(self.txt_w2, 2,1)

        layout.addLayout(layout2)

        # Cargas Puntuales
        lbl_carga_puntual = QLabel('Cargas Puntuales')
        layout.addWidget(lbl_carga_puntual)

        lbl_p1 = QLabel('P1 = ')
        self.txt_p1 = QLineEdit()
        lbl_a1 = QLabel('a1 = ')
        self.txt_a1 = QLineEdit()
        lbl_b1 = QLabel('b1 = ')
        self.txt_b1 = QLineEdit()
        lbl_p2 = QLabel('P2 = ')
        self.txt_p2 = QLineEdit()
        lbl_a2 = QLabel('a2 = ')
        self.txt_a2 = QLineEdit()
        lbl_b2 = QLabel('b2 = ')
        self.txt_b2 = QLineEdit()
        

        layout3.addWidget(lbl_p1, 1, 0)
        layout3.addWidget(self.txt_p1, 1, 1)
        layout3.addWidget(lbl_a1, 2, 0)
        layout3.addWidget(self.txt_a1, 2, 1)
        layout3.addWidget(lbl_b1, 3, 0)
        layout3.addWidget(self.txt_b1, 3,1)
        layout3.addWidget(lbl_p2, 4, 0)
        layout3.addWidget(self.txt_p2, 4, 1)
        layout3.addWidget(lbl_a2, 5, 0)
        layout3.addWidget(self.txt_a2, 5, 1)
        layout3.addWidget(lbl_b2, 6, 0)
        layout3.addWidget(self.txt_b2, 6,1)
        


        layout.addLayout(layout3)

        # Boton Calcular
        self.btn_calcular = QPushButton('Calcular')
        self.btn_calcular.clicked.connect(self.calcular)
        layout.addWidget(self.btn_calcular)

        widget = QWidget()
        widget.setLayout(layout)

        self.setWindowTitle('Metodo de Rigidez')
        self.setCentralWidget(widget)

    def calcular(self):
        # Lectura de las variables
        valor_A = float(self.txt_A.text())
        valor_B = float(self.txt_B.text())
        valor_Ar = float(self.txt_Ar.text())
        valor_E = float(self.txt_E.text())
        valor_I = float(self.txt_I.text())
        valor_w1 = float(self.txt_w1.text())
        valor_w2 = float(self.txt_w2.text())
        valor_p1 = float(self.txt_p1.text())
        valor_a1 = float(self.txt_a1.text())
        valor_b1 = float(self.txt_b1.text())
        valor_p2 = float(self.txt_p2.text())
        valor_a2 = float(self.txt_a2.text())
        valor_b2 = float(self.txt_b2.text())
        valor_Fx1 = float(self.txt_Fx1.text())
        valor_Fy1 = float(self.txt_Fy1.text())
        valor_Fx2 = float(self.txt_Fx2.text())
        valor_Fy2 = float(self.txt_Fy2.text())
        valor_Fx3 = float(self.txt_Fx3.text())
        valor_Fy3 = float(self.txt_Fy3.text())








        datos_entrada = {
            'valor_A': valor_A,
            'valor_B': valor_B,
            'valor_Ar': valor_Ar,
            'valor_E': valor_E,
            'valor_I': valor_I,
            'valor_w1': valor_w1,
            'valor_w2': valor_w2,
            'valor_p1': valor_p1,
            'valor_a1': valor_a1,
            'valor_b1': valor_b1,
            'valor_p2': valor_p2,
            'valor_a2': valor_a2,
            'valor_b2': valor_b2,
            'valor_Fx1': valor_Fx1,
            'valor_Fy1': valor_Fy1,
            'valor_Fx2': valor_Fx2,
            'valor_Fy2': valor_Fy2,
            'valor_Fx3': valor_Fx3,
            'valor_Fy3': valor_Fy3
        }

        resultado = Solucion(datos_entrada)
        self.desplazamientos = resultado.get_desplazamientos()
        self.reacciones = resultado.get_reacciones()
        print(self.desplazamientos)
        print(self.reacciones)
        print(resultado.resolver())

        if self.w is None:
            self.w = ResultadossWindow(self.desplazamientos, self.reacciones)
            self.w.show()

        


        


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()

if __name__ == '__main__':
    main()



