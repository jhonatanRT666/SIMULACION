import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import stats
import math
from scipy.stats import norm

# ---------------- MÉTODOS DE GENERACIÓN ----------------
def cuadrados_medios(seed, n):
    resultados = []
    Y = seed
    for i in range(n):
        Y2 = Y ** 2
        Y2_str = str(Y2).zfill(8)
        X = int(Y2_str[2:6])
        r = X / 10000
        resultados.append((i, Y, f"{Y}^2={Y2}", X, r))
        Y = X
    return resultados

def productos_medios(seed1, seed2, n):
    resultados = []
    s0, s1 = seed1, seed2
    for i in range(n):
        Yi = s0 * s1
        Yi_str = str(Yi).zfill(8)
        X = int(Yi_str[2:6])
        r = X / 10000
        resultados.append((i, f"{s0}*{s1}", Yi, X, r))
        s0, s1 = s1, X
    return resultados

def multiplicador_constante(seed, a, n):
    resultados = []
    X = seed
    for i in range(n):
        Yi = a * X
        Yi_str = str(Yi).zfill(8)
        X = int(Yi_str[2:6])
        r = X / 10000
        resultados.append((i, f"{a}*{X if i>0 else seed}", Yi, X, r))
    return resultados

# ---------------- PRUEBAS ESTADÍSTICAS ----------------
def prueba_media(resultados):
    r_vals = [r for _, _, _, _, r in resultados]
    n = len(r_vals)
    r_mean = sum(r_vals) / n
    Z = (r_mean - 0.5) / math.sqrt(1 / (12 * n))
    Z_crit = norm.ppf(1 - 0.05/2)

    msg = f"📊 PRUEBA DE MEDIA\n\n"
    msg += f"Media muestral: {r_mean:.4f}\n"
    msg += f"Estadístico Z: {Z:.4f}\n"
    msg += f"Límites: [{-Z_crit:.4f}, {Z_crit:.4f}]\n\n"

    if -Z_crit <= Z <= Z_crit:
        msg += "✅ Se acepta la hipótesis de uniformidad en la media."
    else:
        msg += "❌ Se rechaza la hipótesis de uniformidad en la media."
    return msg

def prueba_varianza(resultados):
    r_vals = [r for _, _, _, _, r in resultados]
    n = len(r_vals)
    r_mean = sum(r_vals) / n
    var = sum((x - r_mean)**2 for x in r_vals) / (n - 1)

    chi2_stat = (n - 1) * var / (1/12)
    chi2_lower = stats.chi2.ppf(0.025, n - 1)
    chi2_upper = stats.chi2.ppf(0.975, n - 1)

    msg = f"📊 PRUEBA DE VARIANZA\n\n"
    msg += f"Varianza muestral: {var:.4f}\n"
    msg += f"Estadístico Chi²: {chi2_stat:.4f}\n"
    msg += f"Límites: [{chi2_lower:.4f}, {chi2_upper:.4f}]\n\n"

    if chi2_lower <= chi2_stat <= chi2_upper:
        msg += "✅ Se acepta la hipótesis de uniformidad en la varianza."
    else:
        msg += "❌ Se rechaza la hipótesis de uniformidad en la varianza."
    return msg

# ---------------- NUEVA PRUEBA DE UNIFORMIDAD ----------------
class PruebaUniformidadApp(ctk.CTk):
    def __init__(self, datos=None):
        super().__init__()
        self.title("Prueba de Uniformidad")
        self.geometry("800x700")
        self.resizable(True, True)
        self.configure(bg_color="black")
        self.datos = datos or []

        frame = ctk.CTkFrame(self, fg_color="black")
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Prueba de Uniformidad (Chi²)", 
                     font=("Helvetica", 18, "bold"), text_color="white").pack(pady=10)

        self.m_entry = ctk.CTkEntry(frame, width=200, placeholder_text="Número de intervalos (m)")
        self.m_entry.insert(0, "10")
        self.m_entry.pack(pady=5)
        
        self.alpha_entry = ctk.CTkEntry(frame, width=200, placeholder_text="Nivel de confianza (α)")
        self.alpha_entry.insert(0, "0.95")
        self.alpha_entry.pack(pady=5)

        self.resultado_text = scrolledtext.ScrolledText(frame, width=80, height=10, bg="black", fg="white",
                                                        font=("Courier", 10), wrap=tk.WORD)
        self.resultado_text.pack(pady=10, fill="both", expand=True)

        btn_frame = ctk.CTkFrame(frame, fg_color="black")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame,text="Ejecutar Prueba",command=self.ejecutar_prueba).pack(side="left",padx=5)
        ctk.CTkButton(btn_frame,text="Mostrar Histograma",command=self.mostrar_histograma).pack(side="left",padx=5)
        ctk.CTkButton(btn_frame,text="Exportar a .txt",command=self.exportar_resultados).pack(side="left",padx=5)
        ctk.CTkButton(frame, text="Volver al generador", command=self.destroy).place(x=600,y=10)

        self.canvas=None

    def ejecutar_prueba(self):
        try:
            m=int(self.m_entry.get())
            alpha=float(self.alpha_entry.get())
            if len(self.datos)==0:
                messagebox.showwarning("Advertencia","No hay datos generados.")
                return
            intervalos=np.linspace(0,1,m+1)
            frecuencia_esperada=len(self.datos)/m
            frecuencia_observada=np.zeros(m)
            for x in self.datos:
                i=np.searchsorted(intervalos,x,side='right')-1
                if 0<=i<m:
                    frecuencia_observada[i]+=1
            chi_calculado=sum((frecuencia_observada-frecuencia_esperada)**2/frecuencia_esperada)
            df=m-1
            chi_critico=stats.chi2.ppf(alpha,df)
            resultado=f"""
Resultados de la Prueba de Uniformidad (Chi²):

Número de observaciones (n): {len(self.datos)}
Número de intervalos (m): {m}
Grados de libertad: {df}
Nivel de confianza: {alpha}

Frecuencia Esperada por intervalo: {frecuencia_esperada:.2f}

Chi² calculado: {chi_calculado:.4f}
Chi² crítico ({alpha}, {df}): {chi_critico:.4f}

Conclusión: 
{"✅ Se acepta H0 (uniformidad)" if chi_calculado < chi_critico else "❌ Se rechaza H0 (no uniformidad)"}
"""
            self.resultado_text.delete(1.0, tk.END)
            self.resultado_text.insert(tk.END,resultado)
        except Exception as e:
            messagebox.showerror("Error",f"{e}")

    def mostrar_histograma(self):
        try:
            m=int(self.m_entry.get())
            if len(self.datos)==0:
                messagebox.showwarning("Advertencia","No hay datos generados.")
                return
            fig,ax=plt.subplots(figsize=(8,5),dpi=100)
            n,bins,patches=ax.hist(self.datos,bins=m,edgecolor='green',color='green',alpha=0.8,rwidth=0.8)
            esperada=len(self.datos)/m
            ax.axhline(y=esperada,color='red',linestyle='--',linewidth=1.5,label=f'Frecuencia Esperada ({esperada:.2f})')
            kde=stats.gaussian_kde(self.datos)
            x_kde=np.linspace(0,1,100)
            y_kde=kde(x_kde)
            ax.plot(x_kde,y_kde*len(self.datos),color='yellow',linewidth=1.5,label='KDE')
            ax.set_xlabel("Intervalos (0,1)")
            ax.set_ylabel("Frecuencia Observada")
            ax.set_title("Histograma de Frecuencias con KDE")
            ax.legend()
            if self.canvas:
                self.canvas.get_tk_widget().destroy()
            self.canvas=FigureCanvasTkAgg(fig,master=self)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(pady=10,fill="both",expand=True)
        except Exception as e:
            messagebox.showerror("Error",f"{e}")

    def exportar_resultados(self):
        try:
            contenido=self.resultado_text.get(1.0,tk.END)
            with open("prueba_uniformidad.txt","w",encoding="utf-8") as f:
                f.write(contenido)
            messagebox.showinfo("Éxito","Resultados exportados a 'prueba_uniformidad.txt'")
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo exportar: {e}")

# ---------------- CONTROL DE INTERFAZ ----------------
def generar():
    try:
        metodo = combo_metodo.get()
        n = int(entry_n.get())
        if n <= 0:
            messagebox.showerror("Error", "La cantidad de números debe ser mayor que 0.")
            return

        global resultados
        resultados = []

        for row in tree.get_children():
            tree.delete(row)

        if metodo == "Cuadrados Medios":
            seed = int(entry_seed1.get())
            resultados = cuadrados_medios(seed, n)

        elif metodo == "Productos Medios":
            seed1 = int(entry_seed1.get())
            seed2 = int(entry_seed2.get())
            resultados = productos_medios(seed1, seed2, n)

        elif metodo == "Multiplicador Constante":
            seed = int(entry_seed1.get())
            a = int(entry_const.get())
            resultados = multiplicador_constante(seed, a, n)

        for i, Y, operacion, X, r in resultados:
            tree.insert("", "end", values=(i, Y, operacion, X, f"{r:.4f}"))

    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.")

def ejecutar_prueba_media():
    if not resultados:
        messagebox.showerror("Error", "Primero genere números.")
        return
    messagebox.showinfo("Resultado Prueba Media", prueba_media(resultados))

def ejecutar_prueba_varianza():
    if not resultados:
        messagebox.showerror("Error", "Primero genere números.")
        return
    messagebox.showinfo("Resultado Prueba Varianza", prueba_varianza(resultados))

def ejecutar_prueba_uniformidad():
    if not resultados:
        messagebox.showerror("Error", "Primero genere números.")
        return
    r_vals = [r for _, _, _, _, r in resultados]
    PruebaUniformidadApp(datos=r_vals).mainloop()

# ---------------- INTERFAZ PRINCIPAL ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Generador de Números Aleatorios")
root.geometry("1100x650")

frame_inputs = ctk.CTkFrame(root)
frame_inputs.pack(fill="x", pady=10)

ctk.CTkLabel(frame_inputs, text="Método:").grid(row=0, column=0, padx=5, pady=5)
combo_metodo = ttk.Combobox(frame_inputs, values=["Cuadrados Medios", "Productos Medios", "Multiplicador Constante"], state="readonly")
combo_metodo.current(0)
combo_metodo.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(frame_inputs, text="Semilla 1:").grid(row=0, column=2, padx=5, pady=5)
entry_seed1 = ctk.CTkEntry(frame_inputs, width=80)
entry_seed1.grid(row=0, column=3, padx=5, pady=5)

ctk.CTkLabel(frame_inputs, text="Semilla 2 (productos):").grid(row=0, column=4, padx=5, pady=5)
entry_seed2 = ctk.CTkEntry(frame_inputs, width=80)
entry_seed2.grid(row=0, column=5, padx=5, pady=5)

ctk.CTkLabel(frame_inputs, text="Constante (multiplicador):").grid(row=0, column=6, padx=5, pady=5)
entry_const = ctk.CTkEntry(frame_inputs, width=80)
entry_const.grid(row=0, column=7, padx=5, pady=5)

ctk.CTkLabel(frame_inputs, text="Cantidad n:").grid(row=0, column=8, padx=5, pady=5)
entry_n = ctk.CTkEntry(frame_inputs, width=80)
entry_n.grid(row=0, column=9, padx=5, pady=4)

btn_generar = ctk.CTkButton(frame_inputs, text="Generar", command=generar, width=140, height=35, corner_radius=12)
btn_generar.grid(row=2, column=0, padx=10, pady=15)

btn_prueba_media = ctk.CTkButton(frame_inputs, text="Prueba Media", command=ejecutar_prueba_media, width=140, height=35, corner_radius=12)
btn_prueba_media.grid(row=2, column=1, padx=10, pady=15)

btn_prueba_varianza = ctk.CTkButton(frame_inputs, text="Prueba Varianza", command=ejecutar_prueba_varianza, width=140, height=35, corner_radius=12)
btn_prueba_varianza.grid(row=2, column=2, padx=10, pady=15)

btn_prueba_uniformidad = ctk.CTkButton(frame_inputs, text="Prueba Uniformidad", command=ejecutar_prueba_uniformidad, width=160, height=35, corner_radius=12)
btn_prueba_uniformidad.grid(row=2, column=3, padx=10, pady=15)

columns = ("i", "Entrada", "Operación", "Xi", "ri")
tree = ttk.Treeview(root, columns=columns, show="headings", height=18)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=170, anchor="center")

tree.pack(pady=10, fill="both", expand=True)

resultados = []

root.mainloop()
