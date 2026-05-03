# pylabo

Este es un paquete de Python para abstraer algunas cuestiones técnicas de los
laboratorios de enseñanza (labos 1, 2 y 3) y avanzados (labos 4 y 5). Por ahora
no está para nada documentado.

---

La idea de este paquete es usar dataframes de
[pandas](https://pandas.pydata.org/) para abstraer las mediciones. Después de
todo, la mayoría de los datos crudos y resultados se pueden guardar como csv.
Hay módulos para
- hacer plots (`pylabo.plot`)
- hacer ajustes (`pylabo.fit`)
que intentan abstraen el boilerplate de matplotlib y scipy y que permiten
trabajar con dataframes fácilmente. También hay un pequeño módulo olvidado para interactuar con Google Sheets. Lo usé únicamente en labo 2, cuando todavía hacíamos mediciones a mano, para crear archivos csv de manera más automática.

El módulo `pylabo.visa` es un wrapper de
[PyVISA](https://github.com/pyvisa/pyvisa). Contiene clases que abstraen
algunos instrumentos específicos. Las más pulidas son las del osciloscopio
(Tektronix TDS1002B) y del amplificador lock-in (SR830). 

También hay un pequeño modulo (`pylabo.logs`) para hacer logs con colores y algunas herramientas sueltas para lidiar con los dataframes (transformada de Fourier, unpacking, etc.).
