import tkinter as tk
from tkinter import ttk, messagebox
import math
from scipy.stats import chi2, norm

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
    chi2_lower = chi2.ppf(0.025, n - 1)
    chi2_upper = chi2.ppf(0.975, n - 1)

    msg = f"📊 PRUEBA DE VARIANZA\n\n"
    msg += f"Varianza muestral: {var:.4f}\n"
    msg += f"Estadístico Chi²: {chi2_stat:.4f}\n"
    msg += f"Límites: [{chi2_lower:.4f}, {chi2_upper:.4f}]\n\n"

    if chi2_lower <= chi2_stat <= chi2_upper:
        msg += "✅ Se acepta la hipótesis de uniformidad en la varianza."
    else:
        msg += "❌ Se rechaza la hipótesis de uniformidad en la varianza."
    return msg

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

        # limpiar tabla
        for row in tree.get_children():
            tree.delete(row)

        if metodo == "Cuadrados Medios":
            seed = int(entry_seed1.get())
            if seed < 1000 or seed > 9999:
                messagebox.showerror("Error", "La semilla debe ser un número de 4 dígitos.")
                return
            resultados = cuadrados_medios(seed, n)

        elif metodo == "Productos Medios":
            seed1 = int(entry_seed1.get())
            seed2 = int(entry_seed2.get())
            if not (1000 <= seed1 <= 9999 and 1000 <= seed2 <= 9999):
                messagebox.showerror("Error", "Ambas semillas deben ser números de 4 dígitos.")
                return
            resultados = productos_medios(seed1, seed2, n)

        # llenar tabla
        for i, Y, operacion, X, r in resultados:
            tree.insert("", "end", values=(i, Y, operacion, X, f"{r:.4f}"))

    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.")

def ejecutar_pruebas():
    if not resultados:
        messagebox.showerror("Error", "Primero genere números.")
        return
    msg = prueba_media(resultados) + "\n\n" + prueba_varianza(resultados)
    messagebox.showinfo("Resultados de las Pruebas", msg)

# ---------------- INTERFAZ ----------------
root = tk.Tk()
root.title("Generador de Números Aleatorios - Cuadrados y Productos Medios")
root.geometry("950x600")

frame_inputs = tk.LabelFrame(root, text="Configuración", padx=10, pady=10)
frame_inputs.pack(fill="x", pady=10)

tk.Label(frame_inputs, text="Método:").grid(row=0, column=0, padx=5, pady=5)
combo_metodo = ttk.Combobox(frame_inputs, values=["Cuadrados Medios", "Productos Medios"], state="readonly")
combo_metodo.current(0)
combo_metodo.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Semilla 1:").grid(row=0, column=2, padx=5, pady=5)
entry_seed1 = tk.Entry(frame_inputs, width=8)
entry_seed1.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_inputs, text="Semilla 2 (solo productos):").grid(row=0, column=4, padx=5, pady=5)
entry_seed2 = tk.Entry(frame_inputs, width=8)
entry_seed2.grid(row=0, column=5, padx=5, pady=5)

tk.Label(frame_inputs, text="Cantidad n:").grid(row=0, column=6, padx=5, pady=5)
entry_n = tk.Entry(frame_inputs, width=8)
entry_n.grid(row=0, column=7, padx=5, pady=5)

btn_generar = tk.Button(frame_inputs, text="Generar", command=generar, bg="#4CAF50", fg="white")
btn_generar.grid(row=0, column=8, padx=10, pady=5)

btn_pruebas = tk.Button(frame_inputs, text="Ejecutar Pruebas", command=ejecutar_pruebas, bg="#2196F3", fg="white")
btn_pruebas.grid(row=0, column=9, padx=10, pady=5)

columns = ("i", "Entrada", "Operación", "Xi", "ri")
tree = ttk.Treeview(root, columns=columns, show="headings", height=18)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=170, anchor="center")

tree.pack(pady=10, fill="both", expand=True)

resultados = []

root.mainloop()
