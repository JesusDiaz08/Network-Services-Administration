import handlerSNMP as hs

path_rrd = "/home/linuxsnmp/Escritorio/"
name_rrd = "trend.rrd"

h1 = hs.HandlerSNMP(path_rrd, name_rrd)

h1.create()
commmnity = "grupo4cm3"
ip = "localhost"

h1.update(commmnity, ip)
h1.create_image(path_rrd)