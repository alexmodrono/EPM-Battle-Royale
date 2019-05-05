"""
Programas de muestra con Python/Pygame
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

De:
http://programarcadegames.com/python_examples/f.php?file=Plataforma_moving.py

Vídeo explicativo: http://youtu.be/YKdOD5VkY48

Parte de la serie:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=Plataforma_jumper.py
http://programarcadegames.com/python_examples/f.php?file=Plataforma_scroller.py
http://programarcadegames.com/python_examples/f.php?file=Plataforma_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/
"""

import pygame

"""
Constantes globales
"""

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Dimensiones de la pantalla
LARGO_PANTALLA  = 800
ALTO_PANTALLA = 600


class Protagonista(pygame.sprite.Sprite):
    """ Esta clase representa la barra inferior que controla el protagonista. """


    # -- Métodos
    def __init__(self):
        """ Función Constructor  """

        #  Llama al constructor padre
        super().__init__()

        # Crea una imagen del bloque y lo rellena con color rojo.
        # También podríamos usar una imagen guardada en disco
        largo = 40
        alto = 60
        self.image = pygame.Surface([largo, alto])
        self.image.fill(ROJO)

        # Establecemos una referencia hacia la imagen rectangular
        self.rect = self.image.get_rect()

        # Establecemos el vector velocidad del protagonista
        self.cambio_x = 0
        self.cambio_y = 0

        # Lista de todos los sprites contra los que podemos botar
        self.nivel = None

    def update(self):
        """ Desplazamos al protagonista.  """
        # Gravedad
        self.calc_grav()

        # Desplazar izquierda/derecha
        self.rect.x += self.cambio_x

        # Comprobamos si hemos chocado contra algo
        lista_impactos_bloques = pygame.sprite.spritecollide(self, self.nivel.listade_plataformas, False)
        for bloque in lista_impactos_bloques:
            # Si nos estamos desplazando hacia la derecha, hacemos que nuestro lado derecho sea el lado
            # izquierdo del objeto que hemos tocado
            if self.cambio_x > 0:
                self.rect.right = bloque.rect.left
            elif self.cambio_x < 0:
                # En caso contrario, si nos desplazamos hacia la izquierda, hacemos lo opuesto.
                self.rect.left = bloque.rect.right

        #  Desplazar arriba/izquierda
        self.rect.y += self.cambio_y

        # Comprobamos si hemos chocado contra algo
        lista_impactos_bloques = pygame.sprite.spritecollide(self, self.nivel.listade_plataformas, False)
        for bloque in lista_impactos_bloques:

            # Restablecemos nuestra posición basándonos en la parte superior/inferior del objeto.
            if self.cambio_y > 0:
                self.rect.bottom = bloque.rect.top
            elif self.cambio_y < 0:
                self.rect.top = bloque.rect.bottom

            # Detenemos nuestro movimiento vertical
            self.cambio_y = 0

            if isinstance(bloque, PlataformaEnMovimiento):
                self.rect.x += bloque.cambio_x

    def calc_grav(self):
        """ Calculamos el efecto de la gravedad.  """
        if self.cambio_y == 0:
            self.cambio_y = 1
        else:
            self.cambio_y += .35

        # Observamos si nos encontramos sobre el suelo.
        if self.rect.y >= ALTO_PANTALLA - self.rect.height and self.cambio_y >= 0:
            self.cambio_y = 0
            self.rect.y = ALTO_PANTALLA - self.rect.height

    def jump(self):
        """ Llamado cuando el usuario pulsa el botón de 'saltar'. """

        # Descendemos un poco y observamos si hay una plataforma debajo nuestro.
        # Descendemos 2 píxels (con una plataforma que está  descendiendo, no funciona bien
    # si solo descendemos uno).
        self.rect.y += 2
        lista_impactos_plataforma = pygame.sprite.spritecollide(self, self.nivel.listade_plataformas, False)
        self.rect.y -= 2

        # Si está listo para saltar, aumentamos nuestra velocidad hacia arriba
        if len(lista_impactos_plataforma) > 0 or self.rect.bottom >= ALTO_PANTALLA:
            self.cambio_y = -10

    # Movimiento controlado por el protagonista:
    def ir_izquierda(self):
        """ Es llamado cuando el usuario pulsa la flecha izquierda  """
        self.cambio_x = -6

    def ir_derecha(self):
        """ Es llamado cuando el usuario pulsa la flecha  derecha """
        self.cambio_x = 6

    def stop(self):
        """ Es llamado cuando el usuario abandona el teclado """
        self.cambio_x = 0

class Plataforma(pygame.sprite.Sprite):
    """ Plataforma sobre la que el usuario puede saltar. """

    def __init__(self, largo, alto ):
        """ Constructor de plataforma. Asume su construcción cuando el usuario le haya pasado
            un array de 5 números, tal como se ha definido al principio de este código.  """
        super().__init__()

        self.image = pygame.Surface([largo, alto])
        self.image.fill(VERDE)

        self.rect = self.image.get_rect()


class PlataformaEnMovimiento(Plataforma):
    """ Esta es una Plataforma que podemos realmente mover. """
    cambio_x = 0
    cambio_y = 0

    limite_superior = 0
    limite_inferior = 0
    limite_izquierda = 0
    limite_derecha = 0

    protagonista = None

    Nivel = None

    def update(self):
        """ Desplaza la Plataforma.
            Empujará al protagonista fuera de su camino si viene en esta dirección.
            NO gestiona qué sucede si la plataforma empuja al protagonista contra
        otro objeto. Asegúrate de que las plataformas tengan espacio para poder
        empujar al protagonista. En caso contrario, añade el código necesario
        para que pueda gestionarlo si esto no sucede. """

        # Desplazar izquierda/derecha
        self.rect.x += self.cambio_x

        # Comprobamos si hemos chocado contra el protagonista
        impacto = pygame.sprite.collide_rect(self, self.protagonista)
        if impacto:
            # Hemos impactado contra el protagonista. Lo empujamos a un lado
            # y asumimos que no impactará con ninguna otra cosa.

            # Si nos estamos desplazando hacia la derecha, establece que nuestro lado
        # derecho se coloque al lado izquierdo del objeto contra el que hemos
            # impactado
            if self.cambio_x < 0:
                self.protagonista.rect.right = self.rect.left
            else:
                # En caso contrario (desplazamiento a la izquierda), hacemos lo opuesto
                self.protagonista.rect.left = self.rect.right

        # Desplazar arriba/abajo
        self.rect.y += self.cambio_y

        # Comprobamos si hemos impactado con el protagonista
        impacto = pygame.sprite.collide_rect(self, self.protagonista)
        if impacto:
           # Hemos impactado contra el protagonista. Lo empujamos a un lado
           # y asumimos que no impactará con ninguna otra cosa.

           # Restablecemos nuestra posición basándonos en la parte superior/inferior
       # del objeto
            if self.cambio_y < 0:
                self.protagonista.rect.bottom = self.rect.top
            else:
                self.protagonista.rect.top = self.rect.bottom

        # Comprobamos los límites y vemos si es necesario invertir el sentido

        if self.rect.bottom > self.limite_inferior or self.rect.top < self.limite_superior:
            self.cambio_y *= -1

        cur_pos = self.rect.x - self.nivel.desplazar_escenario
        if cur_pos < self.limite_izquierda or cur_pos > self.limite_derecha:
            self.cambio_x *= -1

class Nivel():
    """ Esta es una súper clase genérica usada para definir un Nivel.
        Crea una clase hija específica para cada Nivel con una info
        específica.  """

    def __init__(self, protagonista):
        """ Constructor. Requerido cuando las Plataformas
            móviles colisionan con el protagonista. """
        self.listade_plataformas = pygame.sprite.Group()
        self.listade_enemigos = pygame.sprite.Group()
        self.protagonista = protagonista

        # Imagen de fondo
        self.imagende_fondo = None

        # Cuán lejos a la izquierda/derecha se ha desplazado el escenario
        self.desplazar_escenario = 0
        self.limitedel_nivel = -1000

    # update todo en este Nivel
    def update(self):
        """ update todo en este Nivel."""
        self.listade_plataformas.update()
        self.listade_enemigos.update()

    def draw(self, pantalla):
        """ dibuja todo en este Nivel. """

        # dibuja la imagen de fondo
        pantalla.fill(AZUL)

        # dibuja todas las listas de sprites que tengamos
        self.listade_plataformas.draw(pantalla)
        self.listade_enemigos.draw(pantalla)

    def escenario_desplazar(self, desplazar_x):
        """ Cuando el usuario se mueve de izquierda/derecha y necesitamos que todo se desplace: """

        # Llevamos la cuenta de la cantidad de desplazamiento
        self.desplazar_escenario += desplazar_x

        # Iteramos a través de todas las listas de sprites y desplazamos
        for plataforma in self.listade_plataformas:
            plataforma.rect.x += desplazar_x

        for enemigo in self.listade_enemigos:
            enemigo.rect.x += desplazar_x

# Creamos las Plataformas para el Nivel
class Nivel_01(Nivel):
    """ Definición para el Nivel 1. """

    def __init__(self, protagonista):
        """ Crear Nivel 1. """

        # Llamada al constructor padre
        Nivel.__init__(self, protagonista)

        self.limitedel_nivel = -1500

        # Array con el largo, alto, x, e y de la Plataforma
        nivel = [ [210, 70, 500, 500],
                  [210, 70, 800, 400],
                  [210, 70, 1000, 500],
                  [210, 70, 1120, 280],
                  ]


        # Iteramos a través del array anterior y añadimos Plataformas
        for plataforma in nivel:
            bloque = Plataforma(plataforma[0], plataforma[1])
            bloque.rect.x = plataforma[2]
            bloque.rect.y = plataforma[3]
            bloque.protagonista = self.protagonista
            self.listade_plataformas.add(bloque)

        # Añadimos una Plataforma móvil personalizada
        bloque = PlataformaEnMovimiento(70, 40)
        bloque.rect.x = 1350
        bloque.rect.y = 280
        bloque.limite_izquierda = 1350
        bloque.limite_derecha = 1600
        bloque.cambio_x = 1
        bloque.protagonista = self.protagonista
        bloque.nivel = self
        self.listade_plataformas.add(bloque)


# Creamos las Plataformas para el Nivel
class Nivel_02(Nivel):
    """ Definición para el Nivel 2. """

    def __init__(self, protagonista):
        """ Crear Nivel 2. """

        # Llamada al constructor padre
        Nivel.__init__(self, protagonista)

        self.limitedel_nivel = -1000

        # Array con el largo, alto, x, e y de la Plataforma
        nivel = [ [210, 70, 500, 550],
                  [210, 70, 800, 400],
                  [210, 70, 1000, 500],
                  [210, 70, 1120, 280],
                  ]


        # Iteramos a través del array anterior y añadimos Plataformas
        for plataforma in nivel:
            bloque = Plataforma(plataforma[0], plataforma[1])
            bloque.rect.x = plataforma[2]
            bloque.rect.y = plataforma[3]
            bloque.protagonista = self.protagonista
            self.listade_plataformas.add(bloque)

        # Añadimos una Plataforma móvil personalizada
        bloque = PlataformaEnMovimiento(70, 70)
        bloque.rect.x = 1500
        bloque.rect.y = 300
        bloque.limite_superior = 100
        bloque.limite_inferior = 550
        bloque.cambio_y = -1
        bloque.protagonista = self.protagonista
        bloque.nivel = self
        self.listade_plataformas.add(bloque)

def main():
    """ Programa Principal """
    pygame.init()

    # Establecemos el alto y largo de la pantalla
    dimensiones = [LARGO_PANTALLA, ALTO_PANTALLA]
    pantalla = pygame.display.set_mode(dimensiones)

    pygame.display.set_caption("Plataformer y Plataformas en Movimiento")

    # Creamos al protagonista
    protagonista = Protagonista()

    # Creamos todos los Niveles
    listade_niveles = []
    listade_niveles.append( Nivel_01(protagonista) )
    listade_niveles.append( Nivel_02(protagonista) )

    # Establecemos el Nivel actual
    nivel_actual_no = 0
    nivel_actual = listade_niveles[nivel_actual_no]

    listade_sprites_activas = pygame.sprite.Group()
    protagonista.nivel = nivel_actual

    protagonista.rect.x = 340
    protagonista.rect.y = ALTO_PANTALLA - protagonista.rect.height
    listade_sprites_activas.add(protagonista)

    # Iteramos hasta que el usuario hace click sobre el botón de salir.
    hecho = False

    # Usado para gestionar cuán rápido se actualiza la pantalla.
    reloj = pygame.time.Clock()

    # -------- Bucle Principal del Programa -----------
    while not hecho:
        for evento in pygame.event.get(): # El usuario realizó alguna acción
            if evento.type == pygame.QUIT:  # Si el usuario hizo click en salir
                hecho = True # Marcamos como hecho y salimos de este bucle

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    protagonista.ir_izquierda()
                if evento.key == pygame.K_RIGHT:
                    protagonista.ir_derecha()
                if evento.key == pygame.K_UP:
                    protagonista.jump()

            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT and protagonista.cambio_x < 0:
                    protagonista.stop()
                if evento.key == pygame.K_RIGHT and protagonista.cambio_x > 0:
                    protagonista.stop()

        # Actualizamos al protagonista.
        listade_sprites_activas.update()

        # Actualizamos los objetos en el Nivel
        nivel_actual.update()

        # Si el protagonista se aproxima al borde derecho, desplazamos el escenario a la izquierda(-x)
        if protagonista.rect.x >= 500:
            diff = protagonista.rect.x - 500
            protagonista.rect.x = 500
            nivel_actual.escenario_desplazar(-diff)

        # Si el protagonista se aproxima al borde izquierdo, desplazamos el escenario a la derecha(+x)
        if protagonista.rect.x <= 120:
            diff = 120 - protagonista.rect.x
            protagonista.rect.x = 120
            nivel_actual.escenario_desplazar(diff)

        # Si el protagonista alcanza el final del Nivel, pasa al siguiente
        posicion_actual = protagonista.rect.x + nivel_actual.desplazar_escenario
        if posicion_actual < nivel_actual.limitedel_nivel:
            if nivel_actual_no < len(listade_niveles)-1:
                protagonista.rect.x = 120
                nivel_actual_no += 1
                nivel_actual = listade_niveles[nivel_actual_no]
                protagonista.nivel = nivel_actual
            else:
                # No hay más Niveles. Esto solo hace que el programa termine.
                # Seguramente quieres que haga algo mejor que esto, no?
                hecho = True

        # TODO EL CÓDIGO DE DIBUJO DEBERÍA IR DEBAJO DE ESTE COMENTARIO
        nivel_actual.draw(pantalla)
        listade_sprites_activas.draw(pantalla)

        # TODO EL CÓDIGO DE DIBUJO DEBERÍA IR ENCIMA DE ESTE COMENTARIO

        # Limitamos a 60 fps
        reloj.tick(60)

        #Avanzamos y actualizamos la pantalla que ya hemos dibujado
        pygame.display.flip()

    # Pórtate bien con el IDLE. Si olvidas esta línea, el programa se 'colgará'
    # al salir.
    pygame.quit()

if __name__ == "__main__":
    main()
