import handlerSNMP as hs
from six.moves import tkinter as tk

class GUI(tk.Frame):
    def __init__(self, parent = None):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()

        self.commmnity_lbl = tk.Label(self.parent, text = "Comunidad")

        self.commmnity_lbl.pack()
        self.commmnity_lbl.place(relx=.1, rely=.1, anchor="c")

        self.com_text = tk.Entry(self.parent)
        self.com_text.insert(0, "gr_4cm1")
        self.com_text.pack()
        self.com_text.place(relx=.3, rely = 0.1, anchor = "c")


        self.ip_lbl = tk.Label(self.parent, text = "IP:")
        self.ip_lbl.pack()
        self.ip_lbl.place(relx =.1, rely = 0.15, anchor = "c")

        self.ip_text = tk.Entry(self.parent)
        self.ip_text.insert(0, "localhost")
        self.ip_text.pack()
        self.ip_text.place(relx = .3, rely = .15, anchor = "c")

        self.btn_start = tk.Button(self.parent, text = "Start", command = self.start)
        self.btn_start.pack()
        self.btn_start.place(relx=0.1, rely=.25, anchor="c")

        #self. = tk.

    def init_ui(self):
        self.parent.title("Monitoreo")
    def start(self):
        path_rrd = "/home/linuxsnmp/Escritorio/"
        name_rrd = "trend.rrd"

        h1 = hs.HandlerSNMP(path_rrd, name_rrd)

        h1.create()

        commmnity = self.com_text.get()
        ip = self.ip_text.get()
        self.umbrales = {"breakpoint": "70", "set": "20", "go": "10"}
        h1.update(commmnity, ip, OID = 'iso.3.6.1.2.1.25.3.3.1.2.196608')
        h1.create_image(path_rrd,
                        self.umbrales["breakpoint"],
                        self.umbrales["set"],
                        self.umbrales["go"])

        h1.deteccion(self.umbrales)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("600x400")
    app = GUI(parent = root)
    app.mainloop()
    root.destroy()

