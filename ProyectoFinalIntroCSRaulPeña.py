

#Se importan los módulos pyglet (para manejo de eventos)
#cocos (un módulo que facilita el desarrollo de videojuegos)
#cocos.actions permite realizar acciones, como mover un objeto o poner otra acción en espera
#cocos.collision_model para la detección de colisiones
#cocos.euclid es un módulo para transformar y crear vectores, facilita el uso de algunas funciones de cocos
#from collections import defaultdict es un diccionario con algunas funciones extra, ayuda a prevenir errores
import pyglet
import cocos
from cocos.actions import *
import cocos.collision_model
import cocos.euclid
from collections import defaultdict



#Aqui se crean dos clases de texto para poder dar la información.
#La clase Etiqueta es más estética, se usa para dar los mensajes de victoria o derrota
#La clase información es más formal, se usa para dar instrucciones.
class Etiqueta(cocos.text.Label):


    #Esta etiqueta toma como atributos
    #un texto, una posición en x, una posición en y
    #y un color, que se da en forma de tupla
    #que contiene los valores
    #(R,G,B, opacidad)
    #Este color es blanco por defecto.
    def __init__(self, texto, x, y, c =(255,255,255,255)):


        #Se utiliza una fuente propia del módulo cocos, llamada "consolas", y un tamaño de letra 14
        #Los valores anchor_x y anchor_y representan los puntos en los que el texto
        #Se "ancla" a la ventana, que sirven para indicar donde debe medirse su posición
        super().__init__(texto, (x,y), font_name = "Consolas", font_size = 14, color = c, anchor_x = "center", anchor_y = "center")


#Similar al anterior, solo que el color por defecto es negro en lugar de blanco
#Y la fuente es times new roman
class Informacion(cocos.text.Label):
    def __init__(self, texto, x, y, c =(0,0,0,255)):
        super().__init__(texto, (x,y), font_name = "times new roman", font_size = 10, color = c, anchor_x = "center", anchor_y = "center")


#Se crea la clase de la capa principal del juego.
class Capajuego(cocos.layer.Layer):

    #is_event_handler es una característica del módulo cocos, que permite a la clase
    #manejar los eventos de colisión y cuando se oprime una tecla
    is_event_handler = True
    def __init__(self) :
        super().__init__()

        #Los atributos velocidad horizontal(vx) y velocidad vertical(vy)
        #se asignan primero para poder ser utilizados en las instrucciones
        #que se crean justo después
        self.vx = 0
        self.vy = 0

        #Se crean las instrucciones para el jugador
        #así como los indicadores de velocidad vertical y horizontal
        self.tinstrucciones1 = Informacion("Oprima las flechas direccionales",100, 470)
        self.tinstrucciones2 = Informacion("para cambiar las velocidades del lanzamiento", 130, 460)
        self.velenx = Informacion(f"velocidad en X = {self.vx}",100, 440)
        self.veleny = Informacion(f"velocidad en Y = {self.vy}",100, 430)
        self.tinstrucciones3 = Informacion("Oprima la barra espaciadora para lanzar",120, 420)

         #Se obtienen las medidas de la ventana
        self.ancho_ventana, self.alto_ventana = cocos.director.director.get_window_size()

        #Se crea un sprite que servirá de fondo, cargando una imagen.
        self.fondo = cocos.sprite.Sprite("Fondo.png")

        #Se ubica el sprite en el centro de la pantalla.
        self.fondo.position = 320, 240
        #Se añade el sprite a la capa
        self.add(self.fondo)

        #Se añaden las instrucciones a la capa.
        #Debe hacerse en este orden porque de añadirse las instrucciones primero
        #el fondo quedaría por encima de ellas
        self.add(self.tinstrucciones1)
        self.add(self.tinstrucciones2)
        self.add(self.velenx)
        self.add(self.veleny)
        self.add(self.tinstrucciones3)

        #Se crea el sprite del jugador, y se lo ubica en las coordenadas y = 50, x = 50
        #y se lo reduce a 30% del tamaño de la imagen original
        self.pajaroenojado = cocos.sprite.Sprite('pajaroenojado.png')
        self.pajaroenojado.position = 50, 50
        self.pajaroenojado.scale = 0.3

        #Se le da al sprite una forma sólida, que permite que el manejador de colisiones sepa donde está.
        #se utiliza el submódulo euclid para crear un vector que pueda ubicar el manejador de colisiones
        #cocos.collision_model.CircleShape indica que el colisionador tiene forma de circulo
        #cocos.euclid.Vector2 transforma los dos componentes de la posición del sprite
        #(que se almacenan normalmente como una tupla) en un vector 2D
        #y se le asigna un radio al colisionador
        #que es la longitud del sprite del jugador
        #multiplicado por 0.2 (para ajustarse mejor a la reducción que se le hizo al sprite)
        #y dividido entre 2, para obtener el radio del sprite
        self.pajaroenojado.cshape = cocos.collision_model.CircleShape(cocos.euclid.Vector2(self.pajaroenojado.position[0],self.pajaroenojado.position[1] ), self.pajaroenojado.width*0.2/2)

        #Se añade el sprite del jugador a la capa
        self.add(self.pajaroenojado)



        #Se crea el sprite de la jaula que servirá como objetivo para el jugador
        #Se le asigna la posición y = 500, x=340
        #Y se la reduce a 30% del tamaño de la imagen original
        self.Jaula = cocos.sprite.Sprite('Jaula.png')
        self.Jaula.position = 500, 340
        self.Jaula.scale = 0.3

        #Se le asigna un colisionador a la jaula
        #En este caso, en forma de rectángulo (cocos.collision_model.AARectShape)
        #Al ser rectangular, se le dan un alto y un ancho
        #Que son la altura del sprite, reducida y dividida entre 2
        #Y el ancho del sprite, reducido y dividido entre 2
        self.Jaula.cshape = cocos.collision_model.AARectShape(cocos.euclid.Vector2(self.Jaula.position[0],self.Jaula.position[1]), self.Jaula.width*0.3/2 + 10, self.Jaula.height*0.3/2)

        #Se crea el sprite de un pájaro encerrado
        #Se le asigna una posición dentro de la jaula
        #Y se lo reduce al 20% del tamaño de la imagen original
        self.pajaroencerrado = cocos.sprite.Sprite('pajaronotanenojado.png')
        self.pajaroencerrado.position = 500, 350
        self.pajaroencerrado.scale = 0.2

        #Se añade al pájaro encerrado primero
        #Y luego la jaula
        #Para que esta última quede por encima del pájaro
        self.add(self.pajaroencerrado)
        self.add(self.Jaula)

        #Se crea el manejador de colisiones
        self.Collmanager = cocos.collision_model.CollisionManagerBruteForce()

        #Se crea un defaultdict para registrar que teclas están pulsadas
        #El default dict tiene la característica de que, si se pide información de una llave no existe
        #En lugar de generar un error, la crea con un valor por defecto.
        #En este caso, al darle como argumento el tipo de objeto int, creara un 0 como valor por defecto.
        self.teclas_pulsadas = defaultdict(int)

        #Se crean algunos atributos más que servirán para llevar control sobre los eventos en el juego
        #El atributo Iniciado verifica si ya se "lanzó" el pájaro
        self.Iniciado = False

        #El atributo Jauladestruida verifica si se destruyó la jaula
        self.Jauladestruida = False

        #Estos atributos son valores para los cálculos físicos, como la fuerza
        #horizontal (Fx), la fuerza vertical, o gravedad, (Fy), la masa(m) y una segunda fuerza
        #vertical (Fyp) que más tarde afectará al pájaro que está encerrado.
        self.Fx = 0
        self.Fy = -49
        self.m = 1
        self.Fyp = 75

        #Se utiliza la función schedule, que recibe una función (self.update)
        #y la llama cada frame
        self.schedule(self.update)

    #Se sobrescribe la función on_key_press de cocos, que
    #es llamada cada vez que se presiona una tecla.
    #El argumento k es un valor número que identifica la tecla que se pulsó
    #Y el argumento m se refiere a los "modificadores" (shift, ctrl, alt, etc)
    def on_key_press(self, k, m):


        #Se le pide que, cuando sea llamada,
        #le asigne a la tecla que se pulsó
        #un valor de 1 en el diccionario teclas_pulsadas
        self.teclas_pulsadas[k] = 1


        #Si la tecla pulsada es igual a
        #la tecla espacio
        #(pyglet.window.key obtiene el valor numérico
        #con el que se identifica una tecla, en este caso
        #la barra espaciadora)
        if k == pyglet.window.key.SPACE:


            #Cuando se oprime la barra espaciadora
            #Se cambia el valor de Iniciado a True
            self.Iniciado = True

            #Y se eliminan las instrucciones de la pantalla
            self.remove(self.tinstrucciones1)
            self.remove(self.tinstrucciones2)
            self.remove(self.tinstrucciones3)
            self.remove(self.velenx)
            self.remove(self.veleny)

    #Se sobrescribe la función on_key_release de cocos, que
    #es llamada cada vez que se suelta una tecla.
    #Posee los mismos argumentos que la funcion on_key_press
    def on_key_release(self, k, m):

        #Cuando una tecla se suelta, le asigna a su valor
        #en el diccionario teclas_pulsadas un 0
        self.teclas_pulsadas[k] = 0


    #Se sobrescribe la función update de cocos
    #que recibe como argumentos un objeto (En este caso, él mismo)
    #y delta time, que es el tiempo real que ha pasado desde la última vez
    #que se llamó esta función
    #Esta función está programada para ejecutarse una vez por frame
    def update(self, deltat):

        #Verifica si todavia no se ha "lanzado" al pajaro
        #para evitar que el jugador manipule la trayectoria del pajaro
        #despues de haberlo lanzado
        if self.Iniciado == False:

            #Verifica si alguna de las flechas direccionales está siendo presionada
            #En caso de que la flecha derecha esté pulsada
            #aumenta la velocidad inicial en x (vx) en 0.3
            #por cada frame que la tecla permanezca pulsada
            if self.teclas_pulsadas[pyglet.window.key.RIGHT] == 1:
                self.vx += 0.3

            #En caso de que la flecha izquierda esté pulsada
            #reduce la velocidad inicial en x (vx) en 0.3
            #por cada frame que la tecla permanezca pulsada
            if self.teclas_pulsadas[pyglet.window.key.LEFT] == 1:
                self.vx -= 0.3

            #En caso de que la flecha arriba esté pulsada
            #aumenta la velocidad inicial en y (vy) en 0.3
            #por cada frame que la tecla permanezca pulsada
            if self.teclas_pulsadas[pyglet.window.key.UP] == 1:
                self.vy += 0.3

            #En caso de que la flecha abajo esté pulsada
            #reduce la velocidad inicial en y (vy) en 0.3
            #por cada frame que la tecla permanezca pulsada
            if self.teclas_pulsadas[pyglet.window.key.DOWN] == 1:
                self.vy -= 0.3

        #Actualiza el texto de las instrucciones
        self.velenx.element.text = f"velocidad en X= {int(self.vx)}"
        self.veleny.element.text = f"velocidad en Y = {int(self.vy)}"

        #Elimina los objetos que el manejador de colisiones pudiera tener
        self.Collmanager.clear()

        #Agrega los objetos que la capa tiene registrados como children
        #el _, node implica que solo registra el segundo valor que cada objeto
        #puesto que el primero es un valor que no necesitamos
        for _, node in self.children:
            self.Collmanager.add(node)

        #Verifica si la jaula no ha sido destruida todavía, y si ya se lanzó al pájaro
        #Ya que este código solo se ejecuta mientras Jauladestruida == False,
        #En cuanto la jaula se destruya, el pájaro dejará de moverse
        if self.Jauladestruida == False and self.Iniciado == True:

            #Verifica si el pájaro y la jaula no están chocando
            if self.Collmanager.they_collide(self.pajaroenojado, self.Jaula):

                #En caso de estarlo, destruye la jaula y cambia el valor de
                #Jauladestruida a True
                self.remove(self.Jaula)
                self.Jauladestruida = True

            #Obtiene la posición del pájaro y la guarda en la variable posicion
            #Esto es más que nada para economizar código
            position =  self.pajaroenojado.position

            #Crea una nueva x a partir del cálculo físico de la trayectoria
            #en x del sprite
            #Usando la velocidad en x (vx) y la diferencia de tiempo desde
            #la última vez que esta función fue llamada (deltat)
            newx = (self.pajaroenojado.position[0] + self.vx*deltat)

            #En caso de que la fuerza en x o la masa del objeto cambiasen
            #Aqui se cambiaria la velocidad en x del objeto
            #Por ahora, ese cambio se mantiene en 0
            self.vx = self.vx + deltat*self.Fx/self.m

            #Crea una nueva y a partir del cálculo físico de la trayectoria
            #en y del sprite
            #Usando la velocidad en y (vy) y la diferencia de tiempo desde
            #la última vez que esta función fue llamada (deltat)
            newy = (self.pajaroenojado.position[1] + self.vy*deltat)

            #Verifica si la nueva coordenada en y es menor que un limite
            if newy <= 40:

                #En caso de serlo, se hace "rebotar" al pájaro
                #Se multiplica por -0.95 para cambiar la dirección de la velocidad en y
                #por eso es negativo
                #Y se supone que es un choque que no es perfectamente elástico,
                #por lo que se pierde 5% de la velocidad con cada rebote
                self.vy *= -0.95

            #Se actualiza la velocidad en y del objeto
            self.vy = self.vy + deltat*self.Fy/self.m

            #Se cambia la posición del sprite acorde a los cálculos realizados anteriormente
            #En forma de tupla, puesto que así es como se almacena la posición del sprite
            #en cocos
            self.pajaroenojado.position = (newx, newy)

            #Se cambia la posición del colisionador del pájaro, para que acompañe
            #al sprite en todo momento
            self.pajaroenojado.cshape.center = cocos.euclid.Vector2(newx,newy)

        #Se define la función cerrarventana, que será
        #util para marcar el fin del juego
        def cerrarventana():

            #Se utiliza el submódulo cocos.director
            #que tiene control sobre la ventana del juego
            #y se le pide que la cierre
            cocos.director.director.window.close()

        #Verifica si la Jaula ya fue destruida
        if self.Jauladestruida == True:

            #Cambia el valor de velocidad en x (vx)
            self.vx = -75

            #Aumenta la velocidad secundaria en y (Fyp)
            #en 5 cada frame
            self.Fyp += 5

            #Realiza los cálculos para cambiar la posición del pájaro que estaba
            #encerrado, usando el mismo código que se utiliza para
            #el movimiento del pájaro del jugador
            position =  self.pajaroencerrado.position
            newx = (self.pajaroencerrado.position[0] + self.vx*deltat)
            self.vx = self.vx + deltat*self.Fx/self.m

            #El único cambia es que en el cálculo de y, en lugar de usar
            # Fy, utiliza Fyp, que, al estar aumentando, da la ilusión
            #de que el pájaro que estaba encerrado está volando.
            newy = (self.pajaroencerrado.position[1] + self.vy*deltat)
            self.vy = self.vy + deltat*self.Fyp/self.m
            self.pajaroencerrado.position = (newx, newy)

            #Añade una etiqueta de la clase que se había creado al principio
            #para marcar la victoria
            self.add(Etiqueta('¡Victoria!', 400, 325))

            #Se utiliza la función “do” del módulo cocos
            #Para pedirle que realice determinadas acciones en un orden especifico
            #En este caso esperar (Para esto es la función Delay) 3 segundos
            #y luego ejecutar la función "cerrarventana" que se había definido previamente
            self.do(Delay(3) + CallFunc(cerrarventana))

        #Verifica si el pájaro ya fue lanzado, pero todavía no se ha destruido la jaula
        if self.Iniciado == True and self.Jauladestruida == False:

            #Verifica si la nueva posición en x (newx) es menor que el límite derecho de la ventana
            # que se mide con el ancho de la ventana, restado a la mitad del ancho del sprite (para encontrar el centro)
            #Y se le suma 50 pixeles, para dar un poco más de margen al jugador
            if self.ancho_ventana + 50 - self.pajaroenojado.width/2 < newx:

                #En caso de que el jugador toque el limite derecho de la pantalla,
                #Se crea una etiqueta de la clase que se habia creado al principio
                #Para marcar la derrota
                self.add(Etiqueta('¡Has perdido!', 325, 235))

                #Y se le pide que espere 3 segundos y luego
                #ejecute la función cerrarventana
                self.do(Delay(3) + CallFunc(cerrarventana))

#En caso de que el programa sea ejecutado directamente
#desde un .exe o desde el archivo .py
#(es decir, si es el proceso principal o "__main__")
#Se ejecuta este pedazo de código
if __name__ == "__main__":

    #Se utiliza el submódulo cocos.director para crear una nueva ventana
    #con el título ‘Proyecto Raul Peña'
    cocos.director.director.init(caption = 'Proyecto Raul Peña')

    #Se crea una escena con una única capa
    #Una capa de la clase "Capajuego"
    Escena = cocos.scene.Scene(Capajuego())

    #Y finalmente se le pide al director que ejecute la escena.
    cocos.director.director.run(Escena)
