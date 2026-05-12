import tkinter as tk
from tkinter import ttk, messagebox

from expert_system import ejecutar_sistema_experto
from test_cases import CASOS_DE_PRUEBA

# ---------------------------------------------------------------------------
# Paleta de colores
# ---------------------------------------------------------------------------
BG        = "#F0F4F8"
PANEL     = "#FFFFFF"
HEADER_BG = "#1A3A5C"
HEADER_FG = "#FFFFFF"
SUBHDR_FG = "#A8C7E8"
LABEL_FG  = "#2C3E50"
DIM_FG    = "#7F8C8D"
BTN_BG    = "#2471A3"
BTN_FG    = "#FFFFFF"
BTN2_BG   = "#717D7E"

# (color_hex, nombre_estilo_progressbar)
RISK = {
    "estable":    ("#27AE60", "Estable.Horizontal.TProgressbar"),
    "precaucion": ("#E6AC00", "Precaucion.Horizontal.TProgressbar"),
    "riesgo":     ("#E67E22", "Riesgo.Horizontal.TProgressbar"),
    "critico":    ("#C0392B", "Critico.Horizontal.TProgressbar"),
}


def _risk_key(etiqueta: str) -> str:
    e = etiqueta.lower()
    if "estable"  in e: return "estable"
    if "precauci" in e: return "precaucion"
    if "riesgo"   in e: return "riesgo"
    return "critico"


class MonotributoApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sistema Experto de Monotributo — ARCA 01/02/2026")
        self.root.geometry("1160x710")
        self.root.minsize(960, 640)
        self.root.configure(bg=BG)
        self._setup_styles()
        self._build_header()
        self._build_content()

    # =========================================================================
    # Estilos
    # =========================================================================
    def _setup_styles(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TEntry",   padding=4)
        s.configure("TSpinbox", padding=4)
        for key, (color, style_name) in RISK.items():
            s.configure(style_name, troughcolor="#E0E0E0", background=color, thickness=18)

    # =========================================================================
    # Header
    # =========================================================================
    def _build_header(self):
        hdr = tk.Frame(self.root, bg=HEADER_BG, pady=11)
        hdr.pack(fill="x")
        tk.Label(hdr, text="SISTEMA EXPERTO DE CATEGORIZACIÓN DE MONOTRIBUTO",
                 bg=HEADER_BG, fg=HEADER_FG, font=("Arial", 15, "bold")).pack()
        tk.Label(hdr, text="Normativa ARCA vigente desde 01/02/2026",
                 bg=HEADER_BG, fg=SUBHDR_FG, font=("Arial", 10)).pack()

    # =========================================================================
    # Layout principal
    # =========================================================================
    def _build_content(self):
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True, padx=12, pady=10)

        left  = tk.Frame(outer, bg=PANEL, bd=1, relief="solid")
        right = tk.Frame(outer, bg=PANEL, bd=1, relief="solid")
        left.pack(side="left", fill="y",           padx=(0, 6))
        right.pack(side="left", fill="both", expand=True)

        self._build_input_panel(left)
        self._build_result_panel(right)

    # =========================================================================
    # Panel izquierdo — formulario
    # =========================================================================
    def _build_input_panel(self, parent):
        parent.configure(padx=16, pady=14)

        tk.Label(parent, text="DATOS DEL CONTRIBUYENTE",
                 bg=PANEL, fg=HEADER_BG, font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 10))

        frm = tk.Frame(parent, bg=PANEL)
        frm.pack(fill="x", anchor="w")

        # Contador de fila para grid
        r = [0]
        def nrow():
            v = r[0]; r[0] += 1; return v

        def lbl(text):
            tk.Label(frm, text=text, bg=PANEL, fg=LABEL_FG,
                     font=("Arial", 9)).grid(row=nrow(), column=0, sticky="w")

        def entry_field(var_attr, default=""):
            var = tk.StringVar(value=default)
            setattr(self, var_attr, var)
            ttk.Entry(frm, textvariable=var, width=34).grid(
                row=nrow(), column=0, sticky="w", pady=(2, 8))

        # Nombre
        lbl("Nombre / Identificador")
        entry_field("var_nombre")

        # Actividad
        lbl("Tipo de actividad")
        self.var_actividad = tk.StringVar(value="servicios")
        frm_act = tk.Frame(frm, bg=PANEL)
        frm_act.grid(row=nrow(), column=0, sticky="w", pady=(2, 8))
        for text, val in [("Servicios", "servicios"), ("Venta de cosas muebles", "venta")]:
            tk.Radiobutton(frm_act, text=text, variable=self.var_actividad, value=val,
                           bg=PANEL, font=("Arial", 9),
                           command=self._toggle_precio).pack(side="left", padx=(0, 12))

        # Campos numéricos
        for label, attr in [
            ("Ingresos brutos anuales ($)",                "var_ingresos"),
            ("Superficie afectada (m²)",                   "var_superficie"),
            ("Energía eléctrica consumida anual (kWh)",    "var_energia"),
            ("Alquiler devengado anual ($, 0 si no paga)", "var_alquiler"),
        ]:
            lbl(label)
            entry_field(attr)

        # Precio unitario (oculto por defecto)
        self._lbl_precio = tk.Label(frm, text="Precio unitario máximo de venta ($)",
                                     bg=PANEL, fg=LABEL_FG, font=("Arial", 9))
        self._lbl_precio.grid(row=nrow(), column=0, sticky="w")
        self.var_precio_unit = tk.StringVar(value="0")
        self._ent_precio = ttk.Entry(frm, textvariable=self.var_precio_unit, width=34)
        self._ent_precio.grid(row=nrow(), column=0, sticky="w", pady=(2, 8))
        self._lbl_precio.grid_remove()
        self._ent_precio.grid_remove()

        # Empleados
        lbl("Empleados en relación de dependencia")
        self.var_empleados = tk.StringVar(value="0")
        ttk.Spinbox(frm, textvariable=self.var_empleados, from_=0, to=99,
                    width=10, state="readonly").grid(row=nrow(), column=0, sticky="w", pady=(2, 14))

        # Botones
        frm_btns = tk.Frame(frm, bg=PANEL)
        frm_btns.grid(row=nrow(), column=0, sticky="w")

        tk.Button(frm_btns, text="  CALCULAR  ", bg=BTN_BG, fg=BTN_FG,
                  font=("Arial", 10, "bold"), relief="flat", cursor="hand2",
                  padx=12, pady=7, command=self._calcular).pack(side="left", padx=(0, 8))

        tk.Button(frm_btns, text="Casos de prueba", bg=BTN2_BG, fg=BTN_FG,
                  font=("Arial", 10), relief="flat", cursor="hand2",
                  padx=10, pady=7, command=self._abrir_casos).pack(side="left", padx=(0, 8))

        tk.Button(frm_btns, text="Limpiar", bg="#ECF0F1", fg=BTN2_BG,
                  font=("Arial", 10), relief="solid", cursor="hand2",
                  padx=10, pady=6, command=self._limpiar).pack(side="left")

    def _toggle_precio(self):
        if self.var_actividad.get() == "venta":
            self._lbl_precio.grid()
            self._ent_precio.grid()
        else:
            self._lbl_precio.grid_remove()
            self._ent_precio.grid_remove()

    # =========================================================================
    # Panel derecho — resultados
    # =========================================================================
    def _build_result_panel(self, parent):
        parent.configure(padx=16, pady=14)

        tk.Label(parent, text="DIAGNÓSTICO", bg=PANEL,
                 fg=HEADER_BG, font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 8))

        # Categorías
        frm_cat = tk.Frame(parent, bg=PANEL)
        frm_cat.pack(anchor="w", fill="x")

        tk.Label(frm_cat, text="Categoría por ingresos:", bg=PANEL, fg=DIM_FG,
                 font=("Arial", 10)).grid(row=0, column=0, sticky="w")
        self.lbl_cat_base = tk.Label(frm_cat, text="—", bg=PANEL, fg=LABEL_FG,
                                      font=("Arial", 10, "bold"), width=16, anchor="w")
        self.lbl_cat_base.grid(row=0, column=1, sticky="w", padx=8)

        tk.Label(frm_cat, text="Categoría final:", bg=PANEL, fg=LABEL_FG,
                 font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=(4, 0))
        self.lbl_cat_final = tk.Label(frm_cat, text="—", bg=PANEL, fg=HEADER_BG,
                                       font=("Arial", 16, "bold"), width=16, anchor="w")
        self.lbl_cat_final.grid(row=1, column=1, sticky="w", padx=8)

        ttk.Separator(parent, orient="horizontal").pack(fill="x", pady=8)

        # Obligación mensual
        tk.Label(parent, text="OBLIGACIÓN MENSUAL", bg=PANEL, fg=LABEL_FG,
                 font=("Arial", 10, "bold")).pack(anchor="w")
        frm_obl = tk.Frame(parent, bg=PANEL)
        frm_obl.pack(anchor="w", fill="x", pady=(4, 0))

        self.lbl_obl = []
        for i, (label, bold) in enumerate([
            ("Impuesto integrado:", False),
            ("Aportes SIPA:",       False),
            ("Obra social:",        False),
            ("TOTAL MENSUAL:",      True),
        ]):
            w = "bold" if bold else "normal"
            c = HEADER_BG if bold else LABEL_FG
            tk.Label(frm_obl, text=label, bg=PANEL, fg=c,
                     font=("Arial", 10, w)).grid(row=i, column=0, sticky="w", pady=1)
            v = tk.Label(frm_obl, text="—", bg=PANEL, fg=c,
                         font=("Courier", 10, w), width=20, anchor="e")
            v.grid(row=i, column=1, sticky="e", padx=8, pady=1)
            self.lbl_obl.append(v)

        ttk.Separator(parent, orient="horizontal").pack(fill="x", pady=8)

        # Riesgo fiscal
        tk.Label(parent, text="RIESGO FISCAL  (Módulo Difuso)", bg=PANEL, fg=LABEL_FG,
                 font=("Arial", 10, "bold")).pack(anchor="w")

        frm_risk = tk.Frame(parent, bg=PANEL)
        frm_risk.pack(anchor="w", fill="x", pady=(6, 0))
        self.risk_bar = ttk.Progressbar(frm_risk, length=300, maximum=100,
                                         mode="determinate",
                                         style="Estable.Horizontal.TProgressbar")
        self.risk_bar.pack(side="left")
        self.lbl_risk_num = tk.Label(frm_risk, text="— / 100", bg=PANEL,
                                      fg=DIM_FG, font=("Courier", 10, "bold"), width=10)
        self.lbl_risk_num.pack(side="left", padx=8)

        self.lbl_risk_etiqueta = tk.Label(parent, text="", bg=PANEL, fg=DIM_FG,
                                           font=("Arial", 10, "bold"))
        self.lbl_risk_etiqueta.pack(anchor="w", pady=(4, 0))

        # Presiones
        frm_pres = tk.Frame(parent, bg=PANEL)
        frm_pres.pack(anchor="w", fill="x", pady=(4, 0))
        self.lbl_pres = []
        for i, lbl_txt in enumerate(["Presión ingresos:", "Presión física:", "Presión alquiler:"]):
            tk.Label(frm_pres, text=lbl_txt, bg=PANEL, fg=DIM_FG,
                     font=("Arial", 9)).grid(row=0, column=i * 2,     sticky="w",
                                              padx=(0 if i == 0 else 14, 3))
            v = tk.Label(frm_pres, text="—", bg=PANEL, fg=DIM_FG, font=("Arial", 9, "bold"))
            v.grid(row=0, column=i * 2 + 1, sticky="w")
            self.lbl_pres.append(v)

        ttk.Separator(parent, orient="horizontal").pack(fill="x", pady=8)

        # Alertas
        tk.Label(parent, text="ALERTAS", bg=PANEL, fg=LABEL_FG,
                 font=("Arial", 10, "bold")).pack(anchor="w")
        self.lbl_alertas = tk.Label(parent, text="—", bg=PANEL, fg=DIM_FG,
                                     font=("Arial", 9), justify="left", wraplength=480)
        self.lbl_alertas.pack(anchor="w", pady=(2, 0))

        ttk.Separator(parent, orient="horizontal").pack(fill="x", pady=8)

        # Explicación con scroll
        tk.Label(parent, text="REGLAS ACTIVADAS Y EXPLICACIÓN", bg=PANEL, fg=LABEL_FG,
                 font=("Arial", 10, "bold")).pack(anchor="w")

        frm_txt = tk.Frame(parent, bg=PANEL)
        frm_txt.pack(fill="both", expand=True, pady=(4, 0))
        vsb = ttk.Scrollbar(frm_txt)
        vsb.pack(side="right", fill="y")
        self.txt_expl = tk.Text(frm_txt, bg="#F8F9FA", fg=LABEL_FG, font=("Arial", 9),
                                 relief="solid", bd=1, wrap="word", height=8,
                                 state="disabled", yscrollcommand=vsb.set)
        self.txt_expl.pack(fill="both", expand=True)
        vsb.configure(command=self.txt_expl.yview)

    # =========================================================================
    # Lógica de negocio
    # =========================================================================
    def _calcular(self):
        try:
            caso = self._leer_campos()
        except ValueError as exc:
            messagebox.showerror("Error de validación", str(exc))
            return
        self._mostrar(ejecutar_sistema_experto(caso))

    def _leer_campos(self) -> dict:
        def parse_float(var: tk.StringVar, nombre: str) -> float:
            raw = var.get().replace(",", ".").replace("$", "").replace(" ", "").strip()
            if not raw:
                raise ValueError(f"El campo «{nombre}» es obligatorio.")
            try:
                return float(raw)
            except ValueError:
                raise ValueError(f"«{nombre}» debe ser un número válido.")

        actividad   = self.var_actividad.get()
        precio_unit = parse_float(self.var_precio_unit, "Precio unitario") if actividad == "venta" else 0.0

        try:
            empleados = int(self.var_empleados.get())
        except ValueError:
            raise ValueError("«Empleados» debe ser un número entero.")

        return {
            "nombre":      self.var_nombre.get().strip() or "Caso ingresado",
            "actividad":   actividad,
            "ingresos":    parse_float(self.var_ingresos,   "Ingresos brutos anuales"),
            "superficie":  parse_float(self.var_superficie, "Superficie afectada"),
            "energia":     parse_float(self.var_energia,    "Energía eléctrica consumida"),
            "alquiler":    parse_float(self.var_alquiler,   "Alquiler devengado anual"),
            "precio_unit": precio_unit,
            "empleados":   empleados,
        }

    def _mostrar(self, r: dict):
        # Categorías
        self.lbl_cat_base.configure(text=r["categoria_base"] or "N/A")
        cat_final = r["categoria_final"]
        fg_cat = RISK["critico"][0] if cat_final == "EXCLUIDO" else HEADER_BG
        self.lbl_cat_final.configure(text=cat_final, fg=fg_cat)

        # Obligación mensual
        if r.get("desglose_mensual"):
            d = r["desglose_mensual"]
            for lbl, val in zip(self.lbl_obl,
                                [d["impuesto_integrado"], d["sipa"], d["obra_social"], d["total"]]):
                lbl.configure(text=f"${val:>16,.2f}")
        else:
            for lbl in self.lbl_obl:
                lbl.configure(text="N/A  (excluido)")

        # Riesgo
        riesgo = r["riesgo_numerico"]
        key    = _risk_key(r["riesgo_etiqueta"])
        color, style_name = RISK[key]

        self.risk_bar.configure(value=riesgo, style=style_name)
        self.lbl_risk_num.configure(text=f"{riesgo:.1f} / 100", fg=color)
        self.lbl_risk_etiqueta.configure(text=r["riesgo_etiqueta"], fg=color)

        # Presiones con color según porcentaje
        if r.get("presiones"):
            p = r["presiones"]
            for lbl, val in zip(self.lbl_pres,
                                [p["presion_ingresos"], p["presion_fisica"], p["presion_alquiler"]]):
                pct = val * 100
                c = (RISK["critico"][0]    if pct > 85 else
                     RISK["riesgo"][0]     if pct > 70 else
                     RISK["precaucion"][0] if pct > 50 else
                     RISK["estable"][0])
                lbl.configure(text=f"{pct:.1f}%", fg=c)

        # Alertas
        if r["alertas"]:
            texto = "\n".join(f"→ {a['tipo_alerta']}  (CF={a.get('cf', 1.0)})"
                               for a in r["alertas"])
            self.lbl_alertas.configure(text=texto, fg=RISK["critico"][0])
        else:
            self.lbl_alertas.configure(text="Sin alertas detectadas.", fg=RISK["estable"][0])

        # Explicación
        reglas = "Reglas: " + ", ".join(r["reglas_activadas"])
        expl   = "\n".join(f"{i}. {e}" for i, e in enumerate(r["explicaciones"], 1))
        self._set_txt(reglas + "\n\n" + expl)

    def _set_txt(self, text: str):
        self.txt_expl.configure(state="normal")
        self.txt_expl.delete("1.0", "end")
        self.txt_expl.insert("1.0", text)
        self.txt_expl.configure(state="disabled")

    def _limpiar(self):
        for attr in ("var_nombre", "var_ingresos", "var_superficie", "var_energia", "var_alquiler"):
            getattr(self, attr).set("")
        self.var_actividad.set("servicios")
        self.var_precio_unit.set("0")
        self.var_empleados.set("0")
        self._toggle_precio()
        self.lbl_cat_base.configure(text="—", fg=LABEL_FG)
        self.lbl_cat_final.configure(text="—", fg=HEADER_BG)
        for lbl in self.lbl_obl:
            lbl.configure(text="—")
        self.risk_bar.configure(value=0, style="Estable.Horizontal.TProgressbar")
        self.lbl_risk_num.configure(text="— / 100", fg=DIM_FG)
        self.lbl_risk_etiqueta.configure(text="", fg=DIM_FG)
        for lbl in self.lbl_pres:
            lbl.configure(text="—", fg=DIM_FG)
        self.lbl_alertas.configure(text="—", fg=DIM_FG)
        self._set_txt("")

    # =========================================================================
    # Modal de casos de prueba
    # =========================================================================
    def _abrir_casos(self):
        modal = tk.Toplevel(self.root)
        modal.title("Casos de Prueba")
        modal.geometry("460x390")
        modal.configure(bg=PANEL)
        modal.transient(self.root)
        modal.grab_set()
        modal.resizable(False, False)

        tk.Label(modal, text="Seleccioná un caso de prueba:",
                 bg=PANEL, fg=HEADER_BG, font=("Arial", 11, "bold")).pack(anchor="w", padx=16, pady=(14, 6))

        frm = tk.Frame(modal, bg=PANEL)
        frm.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        vsb = ttk.Scrollbar(frm)
        vsb.pack(side="right", fill="y")
        lb = tk.Listbox(frm, yscrollcommand=vsb.set, font=("Arial", 9),
                         bg="#F8F9FA", fg=LABEL_FG, selectbackground=BTN_BG,
                         selectforeground=BTN_FG, relief="solid", bd=1,
                         activestyle="none", height=14)
        lb.pack(fill="both", expand=True)
        vsb.configure(command=lb.yview)

        for caso in CASOS_DE_PRUEBA:
            lb.insert("end", f"  {caso['nombre']}")

        def ejecutar():
            sel = lb.curselection()
            if not sel:
                messagebox.showwarning("Sin selección", "Seleccioná un caso primero.", parent=modal)
                return
            caso = CASOS_DE_PRUEBA[sel[0]]
            self._cargar_en_formulario(caso)
            self._mostrar(ejecutar_sistema_experto(caso))
            modal.destroy()

        tk.Button(modal, text="Ejecutar caso seleccionado", bg=BTN_BG, fg=BTN_FG,
                  font=("Arial", 10, "bold"), relief="flat", cursor="hand2",
                  padx=12, pady=8, command=ejecutar).pack(pady=(0, 14))

    def _cargar_en_formulario(self, caso: dict):
        self.var_nombre.set(caso["nombre"])
        self.var_actividad.set(caso["actividad"])
        self.var_ingresos.set(str(int(caso["ingresos"])))
        self.var_superficie.set(str(int(caso["superficie"])))
        self.var_energia.set(str(int(caso["energia"])))
        self.var_alquiler.set(str(int(caso["alquiler"])))
        self.var_precio_unit.set(str(int(caso.get("precio_unit", 0))))
        self.var_empleados.set(str(caso.get("empleados", 0)))
        self._toggle_precio()


if __name__ == "__main__":
    root = tk.Tk()
    MonotributoApp(root)
    root.mainloop()
