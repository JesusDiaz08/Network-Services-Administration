import rrdtool

time_step  = '60'
time_start = 'N'
type_data  = ":COUNTER"
variables  = [":inoctets", ":outoctets"]
limits     = ":U:U"

properties = [":AVERAGE", ":MIN", ":MAX"]
valid_porcentage = [":1.0", ":0.75", ":0.5", ":0.25"]
num_steps  = [":6", ":1"]
num_rows   = ":600"             #Lenght of Round Robin File

object_in  = "DS" + variables[0] + type_data + ":60" + limits
object_out = "DS" + variables[1] + type_data + ":60" + limits
RoundRobinFile01 = "RRA" + properties[0] + valid_porcentage[-2] + num_steps[0] + num_rows
RoundRobinFile02 = "RRA" + properties[0] + valid_porcentage[-2] + num_steps[1] + num_rows


def createRRD(file_name):

    ret = rrdtool.create(   file_name + ".rrd",
                            "--start", time_start,
                            "--step", time_step,
                            object_in,
                            object_out,
                            RoundRobinFile01,
                            RoundRobinFile02
                        )

    if ret:
        print(rrdtool.error())

"""print(object_in)
print(object_out)
print(RoundRobinFile01)
print(RoundRobinFile02)"""
