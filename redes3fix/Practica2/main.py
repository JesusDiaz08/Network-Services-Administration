import handlerSNMP as hs


info_rrdtool = {"path": "/home/linuxsnmp/Escritorio/",
                "name": "trend.rrd"}

community = input("Comunidad: ")
ip        = input("IP: ")


threshold_breakpoint = input("threshold Breakpoint: ")
threshold_upper = input("threshold Upper: ")
threshold_lowe  = input("threshold Lower: ")





h1 = hs.HandlerSNMP(info_rrdtool["path"],
                    info_rrdtool["name"])

h1.create()

h1.update(community, ip)
h1.create_image(info_rrdtool["path"],
                threshold_lowe,
                threshold_upper,
                threshold_breakpoint
                )


def menu():
    print("")