import customtkinter as ctk
from typing import Dict, List, Any


class DashboardPage(ctk.CTkFrame):
    """
    Page principale du dashboard affichant les résultats de résolution.
    Présente un tableau comparatif des différentes méthodes d'optimisation.
    """
    COLORS = {
        "vert_fonce": "#0a3d2a",
        "vert_clair": "#2e7d32",
        "vert_hover": "#1b5e20",
        "vert_pale": "#E8F5E9",
        "vert_tres_pale": "#FDFFFE",
        "blanc": "#FFFFFF",
        "text_principal": "#1a1a1a",
        "text_secondaire": "#555555",
        "text_tertiaire": "#888888",
        "bordure": "#C8E6C9",
        "bordure_grise": "#F5F5F5",
        "success": "#10b981",
        "error": "#E53935",
        "warning": "#FF9800",
        "info": "#0a3d2a",
        "bleu_ciel": "#0a3d2a",
        "vert_olive": "#6A994E",
    }

    def __init__(self, parent, controller):
        """
        Initialise la page dashboard.
        
        Args:
            parent: Widget parent
            controller: Contrôleur de l'application
        """
        super().__init__(parent, fg_color=self.COLORS["blanc"])
        self.controller = controller
        self.results_container = None
        self.build_ui()

    def build_ui(self):
        """
        Construit l'interface utilisateur complète du dashboard.
        """
        self._build_top_bar()
        self._build_main_content()
        self._build_action_buttons()

    def _build_top_bar(self):
        """
        Construit la barre supérieure avec le logo NeoFarm.
        """
        self.top_bar = ctk.CTkFrame(
            self,
            fg_color=self.COLORS["blanc"],
            corner_radius=0,
            height=52,
            border_width=1,
            border_color=self.COLORS["bordure"]
        )
        self.top_bar.pack(fill="x", side="top")
        self.top_bar.pack_propagate(False)

        logo_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        logo_frame.pack(side="left", padx=22, pady=11)

        ctk.CTkLabel(
            logo_frame, 
            text="🌿", 
            font=("Segoe UI", 18), 
            text_color=self.COLORS["vert_clair"]
        ).pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(
            logo_frame, 
            text="NeoFarm", 
            font=("Segoe UI", 14, "bold"), 
            text_color=self.COLORS["vert_clair"]
        ).pack(side="left")

    def _build_main_content(self):
        """
        Construit le contenu principal scrollable du dashboard.
        """
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=self.COLORS["blanc"],
            scrollbar_button_color=self.COLORS["vert_clair"],
            scrollbar_button_hover_color=self.COLORS["vert_hover"],
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=0, pady=0)

        self._build_header(self.scrollable_frame)
        self.results_container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.results_container.pack(fill="x", padx=50, pady=(20, 20))

    def _build_header(self, parent):
        """
        Construit l'en-tête avec le titre et la description.
        
        Args:
            parent: Widget parent pour l'en-tête
        """
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=50, pady=(30, 20))

        ctk.CTkLabel(
            header_frame,
            text="Tableau de Bord Comparatif",
            font=("Segoe UI", 28, "bold"),
            text_color=self.COLORS["vert_fonce"],
        ).pack(anchor="w")

        self.desc_label = ctk.CTkLabel(
            header_frame,
            text="Comparaison des résultats de résolution et du solveur",
            font=("Segoe UI", 15),
            text_color=self.COLORS["text_secondaire"],
        )
        self.desc_label.pack(anchor="w", pady=(5, 0))

    def _build_action_buttons(self):
        """Barre de boutons d'action."""
        btn_container = ctk.CTkFrame(
            self, 
            fg_color="transparent", 
            height=70
        )
        btn_container.pack(fill="x", side="bottom", padx=0, pady=0)
        btn_container.pack_propagate(False)

        inner = ctk.CTkFrame(btn_container, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=50, pady=12)

        btn_retour = ctk.CTkButton(
            inner,
            text="Retour",
            fg_color="transparent",
            hover_color=self.COLORS["vert_pale"],
            width=140,
            height=45,
            font=("Segoe UI", 12, "bold"),
            text_color=self.COLORS["vert_fonce"],
            border_width=2,
            border_color=self.COLORS["vert_fonce"],
            command=self._on_retour,
            corner_radius=12,
        )
        btn_retour.pack(side="left")
        self._bind_outline_hover(btn_retour)

        btn_nouveau = ctk.CTkButton(
            inner,
            text="Nouvelle Analyse",
            fg_color=self.COLORS["vert_clair"],
            hover_color=self.COLORS["vert_hover"],
            width=140,
            height=45,
            font=("Segoe UI", 12, "bold"),
            command=self._on_nouvelle_analyse,
            corner_radius=12,
        )
        btn_nouveau.pack(side="right")

    def _bind_outline_hover(self, btn: ctk.CTkButton):
        """Ajoute l'effet hover pour les boutons outline."""
        btn.bind(
            "<Enter>",
            lambda e: btn.configure(text_color=self.COLORS["vert_hover"], border_color=self.COLORS["vert_hover"])
        )
        btn.bind(
            "<Leave>",
            lambda e: btn.configure(
                text_color=self.COLORS["vert_fonce"], border_color=self.COLORS["vert_fonce"]
            )
        )

    def refresh_data(self):
        """Rafraîchit les données du dashboard."""
        if self.results_container:
            for widget in self.results_container.winfo_children():
                widget.destroy()

        resolution_results = self.controller.get_resolution_results()
        solver_results = self.controller.get_solver_results()
        parcels = self.controller.get_parcels()

        n_parcels = len(parcels)
        if hasattr(self, 'desc_label'):
            self.desc_label.configure(
                text=f"{n_parcels} parcelles — Comparaison des méthodes d'optimisation"
            )

        
        if resolution_results and solver_results and len(resolution_results) > 0 and len(solver_results) > 0:
            self._display_comparison_results(resolution_results, solver_results, parcels)
        else:
            self._display_no_results_message()

    def _display_comparison_results(self, resolution_results: Dict[int, float], 
                                 solver_results: Dict[int, float], parcels: List[dict]):
        """Affiche les résultats comparatifs."""
        
        self._build_comparison_card(resolution_results, solver_results, parcels)
        
        self._build_water_distribution_card(resolution_results, solver_results, parcels)
        
        self._build_conclusion_card(resolution_results, solver_results, parcels)

    def _build_comparison_card(self, resolution_results: Dict[int, float], 
                            solver_results: Dict[int, float], parcels: List[dict]):
        """Carte de comparaison des résultats."""
        card = ctk.CTkFrame(
            self.results_container,
            fg_color=self.COLORS["blanc"],
            corner_radius=20,
            border_width=1,
            border_color=self.COLORS["bordure"],
        )
        card.pack(fill="x", pady=8)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(14, 8))

        stripe = ctk.CTkFrame(
            header, fg_color=self.COLORS["vert_clair"], width=4, height=24, corner_radius=2
        )
        stripe.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            header,
            text="Données Utilisateur Saisies",
            font=("Segoe UI", 15, "bold"),
            text_color=self.COLORS["vert_fonce"],
        ).pack(side="left")

        table_frame = ctk.CTkFrame(card, fg_color="transparent")
        table_frame.pack(fill="x", padx=18, pady=(8, 14))

        header_table = ctk.CTkFrame(table_frame, fg_color=self.COLORS["vert_fonce"], corner_radius=8)
        header_table.pack(fill="x", pady=(0, 3))

        headers = ["Parcelle", "Volume Min", "Taux Perte", "Coeff Croissance", "Coeff Production"]
        widths = [100, 120, 120, 140, 140]
        for col, (header, w) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(
                header_table,
                text=header,
                font=("Segoe UI", 11, "bold"),
                text_color="white",
                width=w
            ).pack(side="left", padx=5, pady=8)

        for i, parcel in enumerate(parcels):
            row_color = self.COLORS["blanc"] if i % 2 == 0 else self.COLORS["vert_pale"]
            row_frame = ctk.CTkFrame(table_frame, fg_color=row_color, corner_radius=6)
            row_frame.pack(fill="x", pady=2)

            parcel_id = parcel.get('id', i) + 1
            parcel_name = parcel.get('nom', f'P{parcel_id}')
            
            user_volume = parcel.get('vol_min', 0)
            user_taux_perte = parcel.get('taux_perte', 0)
            user_coeff_croissance = parcel.get('coeff_croissance', 0)
            user_coeff_production = parcel.get('coeff_production', 0)
            
            values = [
                parcel_name,
                f"{user_volume:.2f} m³",
                f"{user_taux_perte:.1f}%",
                f"{user_coeff_croissance:.2f}",
                f"{user_coeff_production:.2f}"
            ]
            for val, w in zip(values, widths):
                ctk.CTkLabel(
                    row_frame,
                    text=val,
                    font=("Segoe UI", 11),
                    text_color=self.COLORS["text_principal"],
                    width=w
                ).pack(side="left", padx=5, pady=7)

    def _build_water_distribution_card(self, resolution_results: Dict[int, float], 
                                      solver_results: Dict[int, float], parcels: List[dict]):
        """Carte de distribution d'eau pour P1 et P2."""
        card = ctk.CTkFrame(
            self.results_container,
            fg_color=self.COLORS["blanc"],
            corner_radius=20,
            border_width=1,
            border_color=self.COLORS["bordure"],
        )
        card.pack(fill="x", pady=8)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(14, 8))

        stripe = ctk.CTkFrame(
            header, fg_color=self.COLORS["info"], width=4, height=24, corner_radius=2
        )
        stripe.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            header,
            text="Distribution d'Eau par Parcelle",
            font=("Segoe UI", 15, "bold"),
            text_color=self.COLORS["vert_fonce"],
        ).pack(side="left")

        dist_frame = ctk.CTkFrame(card, fg_color="transparent")
        dist_frame.pack(fill="x", padx=18, pady=(8, 14))

        for i in range(len(parcels)):
            col_frame = ctk.CTkFrame(dist_frame, fg_color=self.COLORS["bordure_grise"], corner_radius=12)
            col_frame.pack(side="left", fill="both", expand=True, padx=(0 if i == 0 else 6, 0), pady=5)

            parcel = parcels[i]
            parcel_id = parcel.get('id', i) + 1
            parcel_name = parcel.get('nom', f'P{parcel_id}')
            
            res_val = resolution_results.get(i, 0)
            sol_val = solver_results.get(i, 0)
            
            ctk.CTkLabel(
                col_frame,
                text=parcel_name,
                font=("Segoe UI", 14, "bold"),
                text_color=self.COLORS["vert_fonce"]
            ).pack(pady=(10, 5))

            ctk.CTkLabel(
                col_frame,
                text="Méthode Résolution",
                font=("Segoe UI", 11),
                text_color=self.COLORS["text_secondaire"]
            ).pack(anchor="w", padx=12)
            
            ctk.CTkLabel(
                col_frame,
                text=f"{res_val:.2f} m³",
                font=("Segoe UI", 16, "bold"),
                text_color=self.COLORS["bleu_ciel"]
            ).pack(anchor="w", padx=12, pady=(2, 8))

            ctk.CTkLabel(
                col_frame,
                text="Solveur Excel",
                font=("Segoe UI", 11),
                text_color=self.COLORS["text_secondaire"]
            ).pack(anchor="w", padx=12)
            
            ctk.CTkLabel(
                col_frame,
                text=f"{sol_val:.2f} m³",
                font=("Segoe UI", 16, "bold"),
                text_color=self.COLORS["vert_olive"]
            ).pack(anchor="w", padx=12, pady=(2, 10))

    def _build_conclusion_card(self, resolution_results: Dict[int, float], 
                             solver_results: Dict[int, float], parcels: List[dict]):
        """Carte de conclusion sur le gaspillage."""
        card = ctk.CTkFrame(
            self.results_container,
            fg_color=self.COLORS["blanc"],
            corner_radius=20,
            border_width=1,
            border_color=self.COLORS["bordure"],
        )
        card.pack(fill="x", pady=8)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(14, 8))

        stripe = ctk.CTkFrame(
            header, fg_color=self.COLORS["warning"], width=4, height=24, corner_radius=2
        )
        stripe.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            header,
            text="Conclusion sur le Gaspillage",
            font=("Segoe UI", 15, "bold"),
            text_color=self.COLORS["vert_fonce"],
        ).pack(side="left")

        conclusion_frame = ctk.CTkFrame(card, fg_color="transparent")
        conclusion_frame.pack(fill="x", padx=18, pady=(8, 14))

        res_gaspillage = 0
        sol_gaspillage = 0
        
        for i in range(len(parcels)):
            parcel = parcels[i]
            taux_perte = parcel.get('taux_perte', 0)
            res_val = resolution_results.get(i, 0)
            sol_val = solver_results.get(i, 0)
            res_gasp_i = res_val * taux_perte / 100
            sol_gasp_i = sol_val * taux_perte / 100
            res_gaspillage += res_gasp_i
            sol_gaspillage += sol_gasp_i
            print(f"Parcelle {i}: taux_perte={taux_perte}%, res_val={res_val}, sol_val={sol_val}")
            print(f"Gaspillage P{i+1}: résolution={res_gasp_i:.2f}, solveur={sol_gasp_i:.2f}")
        

        conclusion_text = self._generate_conclusion_text(res_gaspillage, sol_gaspillage, parcels)
        
        conclusion_label = ctk.CTkLabel(
            conclusion_frame,
            text=conclusion_text,
            font=("Segoe UI", 13),
            text_color=self.COLORS["text_principal"],
            wraplength=700,
            justify="left"
        )
        conclusion_label.pack(pady=10)

        details_frame = ctk.CTkFrame(conclusion_frame, fg_color=self.COLORS["bordure_grise"], corner_radius=12)
        details_frame.pack(fill="x", pady=(10, 0))

        details_inner = ctk.CTkFrame(details_frame, fg_color="transparent")
        details_inner.pack(fill="x", padx=15, pady=10)

        for i in range(len(parcels)):
            parcel = parcels[i]
            parcel_id = parcel.get('id', i) + 1
            parcel_name = parcel.get('nom', f'P{parcel_id}')
            taux_perte = parcel.get('taux_perte', 0)
            
            res_val = resolution_results.get(i, 0)
            sol_val = solver_results.get(i, 0)
            
            res_gasp_i = res_val * taux_perte / 100
            sol_gasp_i = sol_val * taux_perte / 100
            
            detail_text = f"{parcel_name}: {res_gasp_i:.2f} m³ (résolution) vs {sol_gasp_i:.2f} m³ (solveur)"
            
            ctk.CTkLabel(
                details_inner,
                text=detail_text,
                font=("Segoe UI", 11),
                text_color=self.COLORS["text_secondaire"]
            ).pack(anchor="w", pady=2)

    def _calculate_gaspillage(self, results: Dict[int, float], parcels: List[dict]) -> float:
        """Calcule le gaspillage total pour une méthode."""
        total_gaspillage = 0
        for i, parcel in enumerate(parcels):
            volume = results.get(i, 0)
            taux_perte = parcel.get('taux_perte', 0)
            gaspillage = volume * taux_perte / 100
            total_gaspillage += gaspillage
        return total_gaspillage

    def _generate_conclusion_text(self, res_gaspillage: float, sol_gaspillage: float, parcels: List[dict]) -> str:
        """Génère le texte de conclusion sur le gaspillage."""
        
        parcel_names = []
        for i, parcel in enumerate(parcels):
            parcel_names.append(parcel.get('nom', f"Parcelle {parcel.get('id', i+1)}"))
        
        if len(parcel_names) <= 2:
            parcels_text = " et ".join(parcel_names)
        else:
            parcels_text = ", ".join(parcel_names[:-1]) + " et " + parcel_names[-1]
        
        if res_gaspillage < sol_gaspillage:
            diff = sol_gaspillage - res_gaspillage
            return (f"Pour {parcels_text}, la méthode de résolution minimise le gaspillage d'eau "
                   f"avec {res_gaspillage:.2f} m³ contre {sol_gaspillage:.2f} m³ pour le solveur Excel, "
                   f"soit une économie de {diff:.2f} m³.")
        elif sol_gaspillage < res_gaspillage:
            diff = res_gaspillage - sol_gaspillage
            return (f"Pour {parcels_text}, le solveur Excel minimise le gaspillage d'eau "
                   f"avec {sol_gaspillage:.2f} m³ contre {res_gaspillage:.2f} m³ pour la méthode de résolution, "
                   f"soit une économie de {diff:.2f} m³.")
        else:
            return (f"Pour {parcels_text}, les deux méthodes donnent des résultats équivalents "
                   f"avec un gaspillage identique de {res_gaspillage:.2f} m³.")

    def _display_no_results_message(self):
        """Affiche un message lorsque aucun résultat n'est disponible."""
        card = ctk.CTkFrame(
            self.results_container,
            fg_color=self.COLORS["blanc"],
            corner_radius=20,
            border_width=1,
            border_color=self.COLORS["bordure"],
        )
        card.pack(fill="x", pady=8)

        ctk.CTkLabel(
            card,
            text="Aucun résultat disponible pour la comparaison",
            font=("Segoe UI", 16),
            text_color=self.COLORS["text_secondaire"],
        ).pack(pady=30)

        ctk.CTkLabel(
            card,
            text="Veuillez d'abord exécuter les méthodes de résolution et le solveur",
            font=("Segoe UI", 13),
            text_color=self.COLORS["text_secondaire"],
        ).pack(pady=(0, 30))

    def clear_results(self):
        """Efface les résultats actuels."""
        if self.results_container:
            for widget in self.results_container.winfo_children():
                widget.destroy()

    def _on_retour(self):
        """Retour à la page précédente."""
        self.controller.show_page("validation_solveur")

    def _on_nouvelle_analyse(self):
        """Démarre une nouvelle analyse."""
        self.controller._last_resolution_results = {}
        self.controller._last_solver_results = {}
        
        self.controller._parcels = []
        self.controller._global_model = {}
        
        self.controller._completed_steps = set()
        
        self.controller.show_page("home")