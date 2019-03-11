import time
import rrdtool
from getSNMP import consultaSNMP


class HandlerSNMP:

    def __init__(self, path_rrd, name_rrd):
        self.path_rrd = path_rrd
        self.name_rrd = name_rrd


    def create(self):
        ret = rrdtool.create(self.path_rrd + self.name_rrd,
                       "--start", 'N',
                       "--step", '60',
                       "DS:CPUload:GAUGE:600:U:U",
                       "RRA:AVERAGE:0.5:1:24")
        if ret:
            print(rrdtool.error())

    def update(self, community, ip, OID = '1.3.6.1.2.1.25.3.3.1.2.196608' ):
        carga_CPU = 0

        while 1:
            carga_CPU = int(consultaSNMP(community, ip, OID))
            valor = "N:" + str(carga_CPU)
            print(valor)
            ret = rrdtool.update(self.path_rrd + self.name_rrd, valor)
            rrdtool.dump(self.path_rrd + self.name_rrd, 'trend.xml')
            time.sleep(1)

        if ret:
            print(rrdtool.error())
            time.sleep(300)

    def create_image(self, path_png):

        ultima_lectura = int(rrdtool.last(self.path_rrd + self.name_rrd))
        tiempo_final = ultima_lectura
        tiempo_inicial = tiempo_final - 3600

        ret = rrdtool.graph(path_png + "trend.png",
                            "--start", str(tiempo_inicial),
                            "--end", str(tiempo_final),
                            "--vertical-label=Carga CPU",
                            "--title=Uso de CPU",
                            "--color", "ARROW#009900",
                            '--vertical-label', "Uso de CPU (%)",
                            '--lower-limit', '0',
                            '--upper-limit', '100',
                            "DEF:carga=" + self.name_rrd + self.name_rrd + ":CPUload:AVERAGE",
                            "AREA:carga#00FF00:Carga CPU",
                            "LINE1:30",
                            "AREA:5#ff000022:stack",
                            "VDEF:CPUlast=carga,LAST",
                            "VDEF:CPUmin=carga,MINIMUM",
                            "VDEF:CPUavg=carga,AVERAGE",
                            "VDEF:CPUmax=carga,MAXIMUM",

                            "COMMENT:Now          Min             Avg             Max",
                            "GPRINT:CPUlast:%12.0lf%s",
                            "GPRINT:CPUmin:%10.0lf%s",
                            "GPRINT:CPUavg:%13.0lf%s",
                            "GPRINT:CPUmax:%13.0lf%s",
                            "VDEF:m=carga,LSLSLOPE",
                            "VDEF:b=carga,LSLINT",
                            'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                            "LINE2:tendencia#FFBB00")


