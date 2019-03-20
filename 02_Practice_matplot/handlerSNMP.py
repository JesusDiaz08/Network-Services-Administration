import time
import rrdtool
import datetime
from reportlab.platypus.paragraph import cjkU
import numpy as np
from Notify import *
from getSNMP import consultaSNMP
import matplotlib.pyplot as plt
import threading

class MonitorTool:
    def __init__(self, path_file, name_file):
        self.path_file = path_file
        self.name_file = name_file
        self.starttime = time.time()
    def createReg(self, name):
        file = open(self.path_file + name, "w")
        file.close()

    def update(self, community, ip, OID, name_elem, iterations = 100, interval = 1):
        file = open(self.path_file + name_elem, "a+")
        self.starttime = time.time()
        for i in range(0, iterations):
            val = int(consultaSNMP(community, ip, OID))
            ts = time.time()
            file.write(str(ts) + " " + str(val) + " " + str(i)+"\n")
            time.sleep(interval)
            print("iteration: " + str(i) + " val: " +str(val))
        file.close()

    def timestampToTime(self, timestamp):
        timestamp = float(timestamp)
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def getPoints(self, namefile):
        file = open(self.path_file + namefile, "r")

        x_points = []
        fx_points = []
        time_points = []
        for line in file:
            #print(line)
            timestamp, current_y, current_x = line.replace("\n", "").split(" ")
            x_points.append(float(current_x))
            fx_points.append(float(current_y))
            time_points.append(float(timestamp))
        file.close()
        return [x_points, fx_points, time_points]

    def createGraph(self, points, thresholds):
        plt.axhline(thresholds[0], color = "r")
        plt.axhline(thresholds[1], color = "b")
        plt.axhline(thresholds[2], color = "g")
        plt.savefig(self.path_file + "test.png")
        #plt.show()
        print(points)

    def getThresholds(self, points):
        medium = np.mean(np.array(points))
        low = medium - np.std(np.array(points))
        high = medium + np.std(np.array(points))
        return [np.floor(low), medium, np.ceil(high)]
    def linear_equation(self):
        points = self.getPoints(self.name_file)
        x_points = np.array(points[0])
        fx_points = np.array(points[1])
        labels = points[2]

        x_dist = x_points[:]
        j = 0
        size = len(labels)
        labels_fin = []
        for i in range(0, size, 10):
            labels_fin.append(str(self.timestampToTime(labels[i])))
            print(labels_fin[j])
            x_dist[j] = x_points[i]
            j = j + 1
        A = np.vstack([x_points, np.ones(len(x_points))]).T
        m, b = np.linalg.lstsq(A, fx_points, rcond = None)[0]
        self.slope = m
        self.b = b
        print("m " + str(m) + " " + " b: "+ str(b) )
        plt.fill_between(x_points, fx_points)
        plt.xticks(x_dist, labels_fin, rotation = 'vertical')
        #plt.plot(x_points, fx_points, 'o', label = "Puntos medidos", markersize = 8)
        plt.plot(x_points, m * x_points + b, label = "equation",color = 'r', linewidth = 4)
        plt.legend()
        plt.show()
    def prediction(self, value):
        return self.timestampToTime(self.starttime + (value - self.b) * 3600/ self.slope)


if __name__== "__main__":
    test = MonitorTool("/home/linuxsnmp/Escritorio/", "test.txt")
    #test.createReg()
    #test.update("gr_4cm1", "localhost", "1.3.6.1.2.1.25.3.3.1.2.196608", test.name_file, 100)
    list1 = test.getPoints(test.name_file)
    print(list1)
    print(test.getThresholds(list1[1]))
    test.createGraph(test.getPoints(test.name_file), test.getThresholds(list1[1]))
    test.linear_equation()
    print(test.prediction(100))
    ''''    
    def create(self, type):
        ret = rrdtool.create(self.path_rrd + type+self.name_rrd,
                       "--start", 'N',
                       "--step", '60',
                       "DS:"+ type +":GAUGE:600:U:U",
                       "RRA:AVERAGE:0.5:1:24")
        if ret:
            print(rrdtool.error())

    def update(self, community, ip, OID = '1.3.6.1.2.1.25.3.3.1.2.196608', total = 500, type ="CPUload"):
        print("type upd: "+ type)
        carga_CPU = 0
        i = 0
        she_doesnt_love_you = 1

        while i < total:
            carga_CPU = int(consultaSNMP(community, ip, OID))
            valor = "N:" + str(carga_CPU)
            print(str(i) + "-> " + valor)
            ret = rrdtool.update(self.path_rrd + type + self.name_rrd, valor)
            rrdtool.dump(self.path_rrd + type+self.name_rrd, 'trend.xml')
            time.sleep(1)
            i += 1

        if ret:
            print(rrdtool.error())
            time.sleep(300)

    def create_image(self, path_png, threshold_lower, threshold_upper, threshold_breakpoint, type):

        ultima_lectura = int(rrdtool.last(self.path_rrd + self.name_rrd))
        tiempo_final = ultima_lectura
        tiempo_inicial = tiempo_final - 3600

        ret = rrdtool.graph(path_png + type+ "trend.png",
                            "--start", str(tiempo_inicial),
                            "--end", str(tiempo_final),
                            "--vertical-label="+type,
                            "--title=Uso de " + type,
                            "--color", "ARROW#009900",
                            '--vertical-label', "Uso de CPU (%)",
                            '--lower-limit', threshold_lower,
                            '--upper-limit', threshold_upper,
                            "DEF:carga=" + self.path_rrd + self.name_rrd + ":CPUload:AVERAGE",
                            "AREA:carga#00FF00:Carga CPU",
                            "LINE1:30",
                            "AREA:5#ff000022:stack",
                            "VDEF:CPUlast=carga,LAST",
                            "VDEF:CPUmin=carga,MINIMUM",
                            "VDEF:CPUavg=carga,AVERAGE",
                            "VDEF:CPUmax=carga,MAXIMUM",
                            "LINE2:" + threshold_breakpoint + "#FF0000",
                            "LINE2:" + threshold_upper      + "#0D76FF",
                            "LINE2:" + threshold_lower      + "#00FF00",
                            "COMMENT:Now          Min             Avg             Max",
                            "GPRINT:CPUlast:%12.0lf%s",
                            "GPRINT:CPUmin:%10.0lf%s",
                            "GPRINT:CPUavg:%13.0lf%s",
                            "GPRINT:CPUmax:%13.0lf%s",
                            "VDEF:m=carga,LSLSLOPE",
                            "VDEF:b=carga,LSLINT",
                            'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                            "LINE2:tendencia#FFBB00")

    def deteccion(self, umbrales, type = "CPUload"):
        print("tipo det: "+type)
        ultima_lectura = int(rrdtool.last(self.path_rrd +type+ self.name_rrd))
        tiempo_final = ultima_lectura
        tiempo_inicial = tiempo_final - 900

        if type == "CPUload":

            ret = rrdtool.graphv(self.path_rrd + type + "deteccion.png",
                                 "--start", str(tiempo_inicial),
                                 "--end", str(tiempo_final),
                                 "--title", type,
                                 "--vertical-label=Uso de "+ type+"(%)",
                                 '--lower-limit', '0',
                                 '--upper-limit', '100',
                                 "DEF:carga=" + self.path_rrd +type+ self.name_rrd + ":"+type+":AVERAGE",
                                 "CDEF:umbral25=carga,"+umbrales['go']+",LT,0,carga,IF",
                                 "VDEF:cargaMAX=carga,MAXIMUM",
                                 "VDEF:cargaMIN=carga,MINIMUM",
                                 "VDEF:cargaSTDEV=carga,STDEV",
                                 "VDEF:cargaLAST=carga,LAST",
                                 "AREA:carga#00FF00:"+type,
                                 "AREA:umbral25#FF9F00:Tráfico de carga mayor que "+umbrales['breakpoint'],
                                 "HRULE:25#FF0000:Umbral 1 - "+umbrales['breakpoint']+"%",
                                 "LINE2:" + umbrales['breakpoint'] + "#FF0000",
                                 "LINE2:" + umbrales['set'] + "#0D76FF",
                                 "LINE2:" + umbrales['go'] + "#00FF00",
                                 "PRINT:cargaMAX:%6.2lf %S",
                                 "GPRINT:cargaMIN:%6.2lf %SMIN",
                                 "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                                 "GPRINT:cargaLAST:%6.2lf %SLAST",
                                 "VDEF:m=carga,LSLSLOPE",
                                 "VDEF:b=carga,LSLINT",
                                 'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                                 "LINE2:tendencia#FFBB00",
                                 "PRINT:m:%6.2lf %S",
                                 "PRINT:b:%6.2lf %S")
        elif type == "RAM":

            ret = rrdtool.graphv(self.path_rrd + type + "deteccion.png",
                                 "--start", str(tiempo_inicial),
                                 "--end", str(tiempo_final),
                                 "--title", type,
                                 "--vertical-label=Uso de "+ type+"(%)",
                                 '--lower-limit', '0',
                                 '--upper-limit', '100',
                                 "DEF:carga=" + self.path_rrd +type+ self.name_rrd + ":"+type+":AVERAGE",
                                 "CDEF:umbral25=carga,25,LT,0,carga,IF",
                                 "VDEF:cargaMAX=carga,MAXIMUM",
                                 "VDEF:cargaMIN=carga,MINIMUM",
                                 "VDEF:cargaSTDEV=carga,STDEV",
                                 "VDEF:cargaLAST=carga,LAST",
                                 "AREA:carga#00FF00:"+type,
                                 "AREA:umbral25#FF9F00:Tráfico de carga mayor que 25",
                                 "HRULE:25#FF0000:Umbral 1 - 25%",
                                 "LINE2:" + umbrales['breakpoint'] + "#FF0000",
                                 "LINE2:" + umbrales['set'] + "#0D76FF",
                                 "LINE2:" + umbrales['go'] + "#00FF00",
                                 "PRINT:cargaMAX:%6.2lf %S",
                                 "GPRINT:cargaMIN:%6.2lf %SMIN",
                                 "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                                 "GPRINT:cargaLAST:%6.2lf %SLAST",
                                 "VDEF:m=carga,LSLSLOPE",
                                 "VDEF:b=carga,LSLINT",
                                 'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                                 "LINE2:tendencia#FFBB00",
                                 "PRINT:m:%6.2lf %S",
                                 "PRINT:b:%6.2lf %S")
        print (ret)
        # print(ret.keys())
        # print(ret.items())

        value = ret['print[0]']
        res = formatNumber(value)
        ultimo_valor = float(res)

        slope = float(formatNumber(ret['print[1]'].replace(" ","").replace("k", "")))
        B = float(formatNumber(ret['print[2]']))
        print(slope)
        print(B)
        pre = Prediction(slope, B)
        print(pre.predict(0))


        print(time.ctime(pre.predict(0) +  tiempo_inicial))
        print("inicial: "+time.ctime(tiempo_inicial))
        if ultimo_valor > float(umbrales['breakpoint']):
            nombre_asunto = "Evidencia 3 "
            send_alert_attached(nombre_asunto + "", self.path_rrd, type+"deteccion.png", type+self.name_rrd)


def formatNumber(value):
    print("val: " + value)
    res = 0
    j = 0
    neg = False
    for i in range(0, len(value)):
        if value[i].isdigit() == True:
            res = res + (int(value[i]) * (10 ** (j)))
            j = j + 1
        elif value[i] == '-':
            neg = True
    res = int(str(res)[::-1])
    if neg:
        res = res * -1
    return res / 100
class Prediction:
    def __init__(self, m, b):
        self.m = m
        self.b = b
    def predict(self, val):
        return (val - self.b) / self.m
'''