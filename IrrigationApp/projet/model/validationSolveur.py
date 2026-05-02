import customtkinter as ctk
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpStatus


def solveur_excel_like(parcels, global_data):
    """
    Résout un problème d'optimisation linéaire similaire au Solveur Excel.
    
    Cette fonction minimise le gaspillage total d'eau tout en respectant les contraintes
    de croissance et de production pour chaque parcelle.
    
    Args:
        parcels (List[Dict]): Liste des dictionnaires contenant les données de chaque parcelle
            avec les clés: vol_min, taux_perte, coeff_croissance, coeff_production
        global_data (Dict): Dictionnaire contenant les données globales
            avec les clés: besoin_total_croissance, besoin_total_production
    
    Returns:
        Dict: Dictionnaire contenant:
            - status (str): Statut de la solution (Optimal, Infeasible, etc.)
            - results (List[float]): Liste des volumes optimaux pour chaque parcelle
            - objective (float): Valeur de l'objectif minimisé (gaspillage total)
    """
    model = LpProblem("Excel_Solver", LpMinimize)

    x = [
        LpVariable(f"x{i+1}", lowBound=p.get("vol_min", 0))
        for i, p in enumerate(parcels)
    ]

    model += lpSum(
        x[i] * parcels[i].get("taux_perte", 0) / 100
        for i in range(len(parcels))
    )

    bc = global_data.get("besoin_total_croissance", 0)
    bp = global_data.get("besoin_total_production", 0)
    
    
    if bc > 0:
        model += lpSum(
            x[i] * parcels[i].get("coeff_croissance", 1)
            for i in range(len(parcels))
        ) >= bc

    if bp > 0:
        model += lpSum(
            x[i] * parcels[i].get("coeff_production", 1)
            for i in range(len(parcels))
        ) >= bp
    
    if bc == 0 and bp == 0:
        model += lpSum(x) >= 1

    model.solve()

    return {
        "status": LpStatus[model.status],
        "results": [v.value() for v in x],
        "objective": model.objective.value()
    }


class ValidationSolveurPage(ctk.CTkFrame):
    """
    Page de validation et d'exécution du solveur d'optimisation.
    Design identique à RecapPage pour une cohérence parfaite.
    """

    COLORS = {
        "primary": "#0a3d2a",
        "primary_light": "#2e7d32",
        "accent": "#4CAF50",
        "bg": "#F5F7F6",
        "card": "#FFFFFF",
        "text": "#333333",
        "text_muted": "#777777",
        "border": "#E0E0E0",
        "success": "#4CAF50",
        "error": "#E53935",
        "warning": "#FF9800",
        "info": "#2196F3",
    }

    FIELD_LABELS = {
        "taux_perte": ("Taux de perte d'eau", "%"),
        "coeff_croissance": ("Besoin hydrique croissance", "coeff"),
        "coeff_production": ("Besoin hydrique production", "coeff"),
        "vol_min": ("Volume minimal d'eau", "m³"),
    }

    CONSTRAINT_LABELS = {
        "besoin_total_croissance": ("Besoin minimal total en croissance", "m³"),
        "besoin_total_production": ("Besoin minimal total en production", "m³"),
    }

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=self.COLORS["bg"])
        self.controller = controller
        self.solve_button = None
        self.has_run_solver = False
        self.btn_container = None  # Référence au conteneur de boutons
        self.build_ui()

    def build_ui(self):
        self._build_top_bar()
        self._build_main_content()
        self._build_action_buttons()

    def _build_top_bar(self):
        self.top_bar = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=0,
            height=52,
            border_width=1,
            border_color=self.COLORS["border"]
        )
        self.top_bar.pack(fill="x", side="top")
        self.top_bar.pack_propagate(False)

        logo_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        logo_frame.pack(side="left", padx=22, pady=11)

        ctk.CTkLabel(
            logo_frame, 
            text="🌿", 
            font=("Segoe UI", 18), 
            text_color="#2e7d32"
        ).pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(
            logo_frame, 
            text="NeoFarm", 
            font=("Segoe UI", 14, "bold"), 
            text_color="#2e7d32"
        ).pack(side="left")

    def _build_main_content(self):
        """Contenu principal scrollable."""
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=self.COLORS["bg"],
            scrollbar_button_color=self.COLORS["primary_light"],
            scrollbar_button_hover_color=self.COLORS["primary"],
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=0, pady=0)

        self._build_header(self.scrollable_frame)
        self._build_parcels_section(self.scrollable_frame)
        self._build_constraints_section(self.scrollable_frame)

    def _build_header(self, parent):
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=50, pady=(30, 20))

        ctk.CTkLabel(
            header_frame,
            text="Validation du Solveur Excel",
            font=("Segoe UI", 28, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(anchor="w")

        self.desc_label = ctk.CTkLabel(
            header_frame,
            text="Analysez et optimisez votre solution d'irrigation",
            font=("Segoe UI", 15),
            text_color=self.COLORS["text_muted"],
        )
        self.desc_label.pack(anchor="w", pady=(5, 0))

    def _build_parcels_section(self, parent):
        """Section des parcelles."""
        self.parcels_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.parcels_container.pack(fill="x", padx=50, pady=(10, 10))

    def _build_constraints_section(self, parent):
        """Section des contraintes globales."""
        self.constraints_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.constraints_container.pack(fill="x", padx=50, pady=(10, 20))

    def _build_action_buttons(self):
        """Barre de boutons affichée AVANT le lancement du solveur."""
        self.btn_container = ctk.CTkFrame(
            self, 
            fg_color=self.COLORS["bg"], 
            height=70
        )
        self.btn_container.pack(fill="x", side="bottom", padx=0, pady=0)
        self.btn_container.pack_propagate(False)

        inner = ctk.CTkFrame(self.btn_container, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=50, pady=12)

        self.btn_retour = ctk.CTkButton(
            inner,
            text="Retour",
            fg_color="transparent",
            hover_color="#E8F5E9",
            width=130,
            height=40,
            font=("Segoe UI", 12, "bold"),
            text_color=self.COLORS["primary"],
            border_width=2,
            border_color=self.COLORS["primary"],
            command=self._on_retour,
            corner_radius=10,
        )
        self.btn_retour.pack(side="left")
        self._bind_outline_hover(self.btn_retour)

        self.solve_button = ctk.CTkButton(
            inner,
            text="Lancer Solver",
            fg_color=self.COLORS["primary_light"],
            hover_color=self.COLORS["primary"],
            width=200,
            height=40,
            font=("Segoe UI", 12, "bold"),
            command=self.run_solver,
            corner_radius=10,
        )
        self.solve_button.pack(side="right")

    def _build_result_buttons(self, parent):
        """Boutons affichés APRÈS le lancement du solveur dans le contenu scrollable."""
        btn_container = ctk.CTkFrame(parent, fg_color="transparent", height=70)
        btn_container.pack(fill="x", padx=50, pady=(30, 20))
        btn_container.pack_propagate(False)

        btn_retour = ctk.CTkButton(
            btn_container,
            text="Retour",
            fg_color="transparent",
            hover_color="#E8F5E9",
            width=130,
            height=40,
            font=("Segoe UI", 12, "bold"),
            text_color=self.COLORS["primary"],
            border_width=2,
            border_color=self.COLORS["primary"],
            command=self._on_retour_after_solver,
            corner_radius=10,
        )
        btn_retour.pack(side="left")
        self._bind_outline_hover(btn_retour)

        spacer = ctk.CTkFrame(btn_container, fg_color="transparent")
        spacer.pack(side="left", fill="both", expand=True)

        btn_comparer = ctk.CTkButton(
            btn_container,
            text="Comparer",
            fg_color=self.COLORS["primary_light"],
            hover_color=self.COLORS["primary"],
            width=200,
            height=40,
            font=("Segoe UI", 12, "bold"),
            command=self.go_to_dashboard,
            corner_radius=10,
        )
        btn_comparer.pack(side="right")

    def _bind_outline_hover(self, btn: ctk.CTkButton):
        btn.bind(
            "<Enter>",
            lambda e: btn.configure(text_color="#1b5e20", border_color="#1b5e20")
        )
        btn.bind(
            "<Leave>",
            lambda e: btn.configure(
                text_color=self.COLORS["primary"], border_color=self.COLORS["primary"]
            )
        )

    def _build_parcel_card(self, parent, parcel):
        """Carte d'une parcelle identique à RecapPage."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.COLORS["card"],
            corner_radius=20,
            border_width=1,
            border_color=self.COLORS["border"],
        )
        card.pack(fill="x", pady=8)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(14, 8))

        stripe = ctk.CTkFrame(
            header, fg_color=self.COLORS["primary_light"], width=4, height=24, corner_radius=2
        )
        stripe.pack(side="left", padx=(0, 10))

        parcel_id = parcel.get('id', 0) + 1
        parcel_name = parcel.get('nom', '')
        
        if parcel_name:
            display_text = f"Parcelle {parcel_id}: {parcel_name}"
        else:
            display_text = f"Parcelle {parcel_id}"
        
        ctk.CTkLabel(
            header,
            text=display_text,
            font=("Segoe UI", 15, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="  Configuré  ",
            font=("Segoe UI", 10, "bold"),
            text_color="white",
            fg_color=self.COLORS["primary_light"],
            corner_radius=10,
        ).pack(side="right")
        
        grid_frame = ctk.CTkFrame(card, fg_color="transparent")
        grid_frame.pack(fill="x", padx=18, pady=(4, 14))
        grid_frame.grid_columnconfigure((0, 1), weight=1)

        fields = [(key, (label, unit)) for key, (label, unit) in self.FIELD_LABELS.items()]
        for idx, (key, (label, unit)) in enumerate(fields):
            row, col = divmod(idx, 2)
            value = parcel.get(key, "—")
            self._build_value_cell(grid_frame, row, col, label, value, unit)

    def _build_constraints_card(self, parent, global_data):
        """Carte des contraintes globales identique à RecapPage."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.COLORS["card"],
            corner_radius=20,
            border_width=1,
            border_color=self.COLORS["border"],
        )
        card.pack(fill="x", pady=8)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(14, 8))

        stripe = ctk.CTkFrame(
            header, fg_color=self.COLORS["primary_light"], width=4, height=24, corner_radius=2
        )
        stripe.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            header,
            text="Paramètres globaux",
            font=("Segoe UI", 15, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="  Configuré  ",
            font=("Segoe UI", 10, "bold"),
            text_color="white",
            fg_color=self.COLORS["primary_light"],
            corner_radius=10,
        ).pack(side="right")

        grid_frame = ctk.CTkFrame(card, fg_color="transparent")
        grid_frame.pack(fill="x", padx=18, pady=(4, 14))
        grid_frame.grid_columnconfigure((0, 1), weight=1)

        fields = list(self.CONSTRAINT_LABELS.items())
        for idx, (key, (label, unit)) in enumerate(fields):
            col = idx % 2
            value = global_data.get(key, "—")
            self._build_value_cell(grid_frame, 0, col, label, value, unit)

    def _build_value_cell(self, parent, row: int, col: int, label: str, value, unit: str):
        """Cellule de valeur stylisée identique à RecapPage."""
        cell = ctk.CTkFrame(parent, fg_color="#F8FAF9", corner_radius=12)
        cell.grid(row=row, column=col, padx=6, pady=6, sticky="ew")

        ctk.CTkLabel(
            cell,
            text=label,
            font=("Segoe UI", 11),
            text_color=self.COLORS["text_muted"],
        ).pack(anchor="w", padx=12, pady=(10, 2))

        val_text = f"{value} {unit}" if value != "—" else "—"
        ctk.CTkLabel(
            cell,
            text=val_text,
            font=("Segoe UI", 14, "bold"),
            text_color=self.COLORS["text"],
        ).pack(anchor="w", padx=12, pady=(2, 10))

    def show_result(self, parcels, global_data, result):
        """Affiche les résultats du solveur dans le style RecapPage."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        header_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=50, pady=(30, 20))

        ctk.CTkLabel(
            header_frame,
            text="Résultats de l'Optimisation",
            font=("Segoe UI", 28, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(anchor="w")

        desc = ctk.CTkLabel(
            header_frame,
            text=f"Statut : {result['status']} — Solution trouvée",
            font=("Segoe UI", 15),
            text_color=self.COLORS["text_muted"],
        )
        desc.pack(anchor="w", pady=(5, 0))

        ctk.CTkLabel(
            self.scrollable_frame,
            text="Variables Optimisées",
            font=("Segoe UI", 18, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(anchor="w", padx=50, pady=(20, 12))

        self._build_variables_card(self.scrollable_frame, result['results'])

        ctk.CTkLabel(
            self.scrollable_frame,
            text="Fonction Objectif",
            font=("Segoe UI", 18, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(anchor="w", padx=50, pady=(20, 12))

        self._build_objective_card(self.scrollable_frame, result['objective'])

        self._build_validation_card(self.scrollable_frame, parcels, result['results'])
        
        self._build_result_buttons(self.scrollable_frame)

    def _build_variables_card(self, parent, results):
        """Carte des variables optimisées."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.COLORS["card"],
            corner_radius=20,
            border_width=1,
            border_color=self.COLORS["border"],
        )
        card.pack(fill="x", padx=50, pady=8)

        grid_frame = ctk.CTkFrame(card, fg_color="transparent")
        grid_frame.pack(fill="x", padx=18, pady=(14, 14))
        grid_frame.grid_columnconfigure((0, 1, 2), weight=1)

        for i, v in enumerate(results):
            row, col = divmod(i, 3)
            cell = ctk.CTkFrame(grid_frame, fg_color="#F8FAF9", corner_radius=12)
            cell.grid(row=row, column=col, padx=6, pady=6, sticky="ew")

            ctk.CTkLabel(
                cell,
                text=f"Variable x{i+1}",
                font=("Segoe UI", 11),
                text_color=self.COLORS["text_muted"],
            ).pack(anchor="w", padx=12, pady=(10, 2))

            ctk.CTkLabel(
                cell,
                text=f"{self._format_number(v)} m³",
                font=("Segoe UI", 14, "bold"),
                text_color=self.COLORS["primary"],
            ).pack(anchor="w", padx=12, pady=(2, 10))

    def _build_objective_card(self, parent, objective):
        """Carte de la valeur objectif."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.COLORS["card"],
            corner_radius=20,
            border_width=1,
            border_color=self.COLORS["border"],
        )
        card.pack(fill="x", padx=50, pady=8)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=18, pady=(14, 14))

        ctk.CTkLabel(
            inner,
            text="Valeur minimisée",
            font=("Segoe UI", 11),
            text_color=self.COLORS["text_muted"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            inner,
            text=f"{self._format_number(objective)} m³",
            font=("Segoe UI", 24, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(anchor="w", pady=(5, 0))

    def _build_result_constraints_card(self, parent, parcels, global_data, results):
        """Carte des contraintes vérifiées."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.COLORS["card"],
            corner_radius=20,
            border_width=1,
            border_color=self.COLORS["border"],
        )
        card.pack(fill="x", padx=50, pady=8)

        grid_frame = ctk.CTkFrame(card, fg_color="transparent")
        grid_frame.pack(fill="x", padx=18, pady=(14, 14))
        grid_frame.grid_columnconfigure((0, 1), weight=1)

        c1 = sum(results[i] * parcels[i].get("coeff_croissance", 1)
                 for i in range(len(parcels)))
        c2 = sum(results[i] * parcels[i].get("coeff_production", 1)
                 for i in range(len(parcels)))

        constraints = [
            ("Croissance atteinte", c1, global_data.get('besoin_total_croissance', 0), "m³"),
            ("Production atteinte", c2, global_data.get('besoin_total_production', 0), "m³")
        ]

        for idx, (label, value, required, unit) in enumerate(constraints):
            col = idx % 2
            cell = ctk.CTkFrame(grid_frame, fg_color="#F8FAF9", corner_radius=12)
            cell.grid(row=0, column=col, padx=6, pady=6, sticky="ew")

            ctk.CTkLabel(
                cell,
                text=label,
                font=("Segoe UI", 11),
                text_color=self.COLORS["text_muted"],
            ).pack(anchor="w", padx=12, pady=(10, 2))

            val_text = f"{self._format_number(value)} / {self._format_number(required)} {unit}"
            ctk.CTkLabel(
                cell,
                text=val_text,
                font=("Segoe UI", 14, "bold"),
                text_color=self.COLORS["success"] if value >= required else self.COLORS["error"],
            ).pack(anchor="w", padx=12, pady=(2, 10))

    def _build_validation_card(self, parent, parcels, results):
        """Carte de validation finale."""
        c1 = sum(results[i] * parcels[i].get("coeff_croissance", 1)
                 for i in range(len(parcels)))
        c2 = sum(results[i] * parcels[i].get("coeff_production", 1)
                 for i in range(len(parcels)))
        
        global_data = self.controller.get_global_model()
        bc = global_data.get('besoin_total_croissance', 0)
        bp = global_data.get('besoin_total_production', 0)
        
        ok = all(
            results[i] >= parcels[i].get("vol_min", 0)
            for i in range(len(parcels))
        ) and (bc == 0 or c1 >= bc) and (bp == 0 or c2 >= bp)

        card = ctk.CTkFrame(
            parent,
            fg_color=self.COLORS["card"],
            corner_radius=20,
            border_width=1,
            border_color=self.COLORS["border"],
        )
        card.pack(fill="x", padx=50, pady=(20, 8))

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(14, 8))

        stripe = ctk.CTkFrame(
            header, 
            fg_color=self.COLORS["success"] if ok else self.COLORS["error"], 
            width=4, 
            height=24, 
            corner_radius=2
        )
        stripe.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            header,
            text="Validation",
            font=("Segoe UI", 15, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(side="left")

        status_text = "  Validé  " if ok else "  Invalide  "
        status_color = self.COLORS["success"] if ok else self.COLORS["error"]
        
        ctk.CTkLabel(
            header,
            text=status_text,
            font=("Segoe UI", 10, "bold"),
            text_color="white",
            fg_color=status_color,
            corner_radius=10,
        ).pack(side="right")

        msg = "Solution optimale validée avec succès" if ok else "Solution invalide — Vérifiez les contraintes"
        ctk.CTkLabel(
            card,
            text=msg,
            font=("Segoe UI", 13),
            text_color=status_color,
        ).pack(anchor="w", padx=18, pady=(4, 14))

    def _format_number(self, value):
        """Formate un nombre sans décimales inutiles."""
        if isinstance(value, (int, float)):
            if value == int(value):
                return str(int(value))
            else:
                return f"{value:.2f}".rstrip('0').rstrip('.')
        return str(value)

    def run_solver(self):
        """Lance le solveur et affiche les résultats."""
        if not self.has_run_solver:
            parcels = self.controller.get_parcels()
            global_data = self.controller.get_global_model()

            if not parcels:
                self._show_error()
                return

            result = solveur_excel_like(parcels, global_data)
            
            if result.get('results'):
                self.controller.set_solver_results(result['results'])
                
                if hasattr(self.controller, '_completed_steps'):
                    self.controller._completed_steps.add("solveur_excel")
            
            self._hide_action_buttons()
            
            self.show_result(parcels, global_data, result)
            
            self.has_run_solver = True

    def _show_error(self):
        """Affiche un message d'erreur."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        header_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=50, pady=(30, 20))

        ctk.CTkLabel(
            header_frame,
            text="Erreur",
            font=("Segoe UI", 28, "bold"),
            text_color=self.COLORS["error"],
        ).pack(anchor="w")

        card = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color=self.COLORS["card"],
            corner_radius=20,
            border_width=1,
            border_color=self.COLORS["border"],
        )
        card.pack(fill="x", padx=50, pady=8)

        ctk.CTkLabel(
            card,
            text="Aucune donnée disponible pour la résolution",
            font=("Segoe UI", 14),
            text_color=self.COLORS["text"],
        ).pack(padx=18, pady=20)

    def _hide_action_buttons(self):
        """Cache la barre de boutons d'action inférieure (Retour + Lancer Solver)."""
        if self.btn_container and self.btn_container.winfo_exists():
            self.btn_container.pack_forget()

    def _show_action_buttons(self):
        """Réaffiche la barre de boutons d'action inférieure."""
        if hasattr(self, 'btn_container'):
            if self.btn_container.winfo_exists():
                self.btn_container.pack(fill="x", side="bottom", padx=0, pady=0)
            else:
                self._build_action_buttons()
        else:
            self._build_action_buttons()

    def _on_retour(self):
        """Retourne à la page précédente (RecapPage)."""
        self.controller.show_page("solution")

    def _on_retour_after_solver(self):
        """
        Retourne à l'état AVANT le lancement du solveur.
        Réinitialise la page pour montrer à nouveau les données initiales.
        """
        self.reset()

    def go_to_dashboard(self):
        """Redirige vers le dashboard de comparaison."""
        if "dashboard" in self.controller.pages:
            dashboard_page = self.controller.pages["dashboard"]
            if hasattr(dashboard_page, 'clear_results'):
                dashboard_page.clear_results()
        self.controller.show_page("dashboard")

    def reset(self):
        """Réinitialise la page à son état initial (avant solveur)."""
        self.has_run_solver = False
        
        
        self.refresh_data()

    def refresh_data(self):
        """Rafraîchit les données affichées à l'état initial."""
        self.has_run_solver = False
        
        self._show_action_buttons()
        
        if hasattr(self, 'scrollable_frame') and self.scrollable_frame:
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()

        self._build_header(self.scrollable_frame)
        self._build_parcels_section(self.scrollable_frame)
        self._build_constraints_section(self.scrollable_frame)

        parcels = self.controller.get_parcels()
        global_data = self.controller.get_global_model()
        n_parcels = len(parcels)

        if hasattr(self, 'desc_label') and self.desc_label:
            self.desc_label.configure(
                text=f"{n_parcels} parcelles configurées — Analysez et optimisez votre solution"
            )

        if n_parcels > 0 and hasattr(self, 'parcels_container') and self.parcels_container:
            ctk.CTkLabel(
                self.parcels_container,
                text="Données des parcelles",
                font=("Segoe UI", 18, "bold"),
                text_color=self.COLORS["primary"],
            ).pack(anchor="w", pady=(0, 12))

            for parcel in parcels:
                self._build_parcel_card(self.parcels_container, parcel)

        if global_data and hasattr(self, 'constraints_container') and self.constraints_container:
            ctk.CTkLabel(
                self.constraints_container,
                text="Contraintes Globales",
                font=("Segoe UI", 18, "bold"),
                text_color=self.COLORS["primary"],
            ).pack(anchor="w", pady=(10, 12))

            self._build_constraints_card(self.constraints_container, global_data)