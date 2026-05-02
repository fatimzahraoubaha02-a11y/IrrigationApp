import customtkinter as ctk
from typing import Dict, List, Any
import sys
import tkinter as tk
from tkinter import messagebox


class SolutionPage(ctk.CTkFrame):
    """
    Page de solution affichant la formulation du programme linéaire.
    Présente le problème d'optimisation mathématique et les méthodes de résolution.
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

    def __init__(self, parent, controller):
        """
        Initialise la page de solution.
        
        Args:
            parent: Widget parent
            controller: Contrôleur de l'application
        """
        super().__init__(parent, fg_color=self.COLORS["bg"])
        self.controller = controller
        self._result_frame = None
        self._after_ids: List[int] = []
        self.build_ui()

    def destroy(self):
        """
        Nettoie les ressources avant la destruction du widget.
        Annule tous les after_ids en attente.
        """
        for after_id in self._after_ids:
            self.after_cancel(after_id)
        super().destroy()

    def _schedule(self, delay: int, callback):
        """
        Planifie l'exécution d'une fonction après un délai.
        
        Args:
            delay: Délai en millisecondes
            callback: Fonction à exécuter
            
        Returns:
            ID de la tâche planifiée
        """
        after_id = self.after(delay, callback)
        self._after_ids.append(after_id)
        return after_id

    def build_ui(self):
        """
        Construit l'interface utilisateur complète de la page.
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

        ctk.CTkLabel(logo_frame, text="🌿", font=("Segoe UI", 18), text_color="#2e7d32").pack(side="left", padx=(0, 8))
        ctk.CTkLabel(logo_frame, text="NeoFarm", font=("Segoe UI", 14, "bold"), text_color="#2e7d32").pack(side="left")

    def _build_main_content(self):
        """
        Construit le contenu principal avec les sections du programme linéaire.
        """
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=self.COLORS["bg"],
            scrollbar_button_color=self.COLORS["primary_light"],
            scrollbar_button_hover_color=self.COLORS["primary"],
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=0, pady=0)

        self._build_header(self.scrollable_frame)
        self._build_lp_section(self.scrollable_frame)
        self._build_explanation_section(self.scrollable_frame)

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
            text="Programme Linéaire",
            font=("Segoe UI", 28, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(anchor="w")

        self.desc_label = ctk.CTkLabel(
            header_frame,
            text="Formulation mathématique du problème d'optimisation",
            font=("Segoe UI", 15),
            text_color=self.COLORS["text_muted"],
        )
        self.desc_label.pack(anchor="w", pady=(5, 0))

    def _build_lp_section(self, parent):
        """
        Construit la section pour la formulation du programme linéaire.
        
        Args:
            parent: Widget parent pour la section
        """
        self.lp_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.lp_container.pack(fill="x", padx=50, pady=(10, 10))

    def _build_explanation_section(self, parent):
        """
        Construit la section d'explication de la méthode de résolution.
        
        Args:
            parent: Widget parent pour la section
        """
        self.explanation_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.explanation_container.pack(fill="x", padx=50, pady=(10, 20))

    def _build_action_buttons(self):
        """
        Construit les boutons d'action pour la navigation.
        """
        btn_container = ctk.CTkFrame(self, fg_color=self.COLORS["bg"], height=70)
        btn_container.pack(fill="x", side="bottom", padx=0, pady=0)
        btn_container.pack_propagate(False)

        inner = ctk.CTkFrame(btn_container, fg_color="transparent")
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

        self.btn_resoudre = ctk.CTkButton(
            inner,
            text="Résoudre",
            fg_color=self.COLORS["primary_light"],
            hover_color=self.COLORS["primary"],
            width=200,
            height=40,
            font=("Segoe UI", 12, "bold"),
            command=self._on_resoudre,
            corner_radius=10,
        )
        self.btn_resoudre.pack(side="right")

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

    def refresh_data(self):
        for widget in self.lp_container.winfo_children():
            widget.destroy()
        for widget in self.explanation_container.winfo_children():
            widget.destroy()

        parcels = self.controller.get_parcels()
        global_data = self.controller.get_global_model()
        n_parcels = len(parcels)

        self.desc_label.configure(
            text=f"{n_parcels} parcelle — Formulation mathématique du problème d'optimisation"
        )

        if not parcels:
            self._build_empty_state(self.lp_container)
            return

        ctk.CTkLabel(
            self.lp_container,
            text="Formulation Mathématique",
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w", pady=(0, 12))

        self._build_lp_card(self.lp_container, parcels, global_data)

        ctk.CTkLabel(
            self.explanation_container,
            text="Interprétation",
            font=("Segoe UI", 18, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(anchor="w", pady=(0, 12))

        self._build_explanation_card(self.explanation_container)

    def _build_empty_state(self, parent):
        empty_frame = ctk.CTkFrame(parent, fg_color="transparent")
        empty_frame.pack(fill="x", pady=40)

        ctk.CTkLabel(empty_frame, text="[ ]", font=("Segoe UI", 48), text_color=self.COLORS["text_muted"]).pack(pady=(0, 20))
        ctk.CTkLabel(empty_frame, text="Aucune donnée disponible", font=("Segoe UI", 16, "bold"), text_color=self.COLORS["text_muted"]).pack()
        ctk.CTkLabel(empty_frame, text="Veuillez saisir les données des parcelles", font=("Segoe UI", 12), text_color=self.COLORS["text_muted"]).pack(pady=(5, 0))

    def _build_lp_card(self, parent, parcels, global_data):
        """Carte principale du programme linéaire - MEME STYLE que RecapPage."""
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
            text="Programme Linéaire",
            font=("Segoe UI", 15, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(side="left")

        copy_btn = ctk.CTkButton(
            header,
            text="Copier",
            fg_color="transparent",
            hover_color="#E8F5E9",
            width=90,
            height=30,
            font=("Segoe UI", 10, "bold"),
            text_color=self.COLORS["primary"],
            border_width=1,
            border_color=self.COLORS["primary"],
            command=lambda: self._copy_linear_program(parcels, global_data),
            corner_radius=8,
        )
        copy_btn.pack(side="right")
        self._bind_outline_hover(copy_btn)

        self._build_subsection_title(card, "Variables de Décision")

        variables_frame = ctk.CTkFrame(card, fg_color="transparent")
        variables_frame.pack(fill="x", padx=18, pady=(4, 8))
        variables_frame.grid_columnconfigure((0, 1), weight=1)

        for i, p in enumerate(parcels):
            row, col = divmod(i, 2)
            self._build_value_cell(
                variables_frame, row, col,
                f"Variable x{i+1}",
                f"Volume d'eau parcelle {p.get('id', i+1)}",
                f"Min: {self._fmt(p.get('vol_min', 0))} m³"
            )

        self._build_subsection_title(card, "Fonction Objectif")

        obj_frame = ctk.CTkFrame(card, fg_color="#F8FAF9", corner_radius=12)
        obj_frame.pack(fill="x", padx=18, pady=(4, 8))

        terms = []
        for i, p in enumerate(parcels):
            taux = p.get('taux_perte', 0)
            coeff = taux / 100
            terms.append(f"{self._fmt(coeff)}·x{i+1}")

        ctk.CTkLabel(
            obj_frame,
            text="Min w = " + " + ".join(terms),
            font=("Consolas", 13, "bold"),
            text_color=self.COLORS["primary"]
        ).pack(anchor="w", padx=12, pady=(10, 2))

        ctk.CTkLabel(
            obj_frame,
            text="Minimiser le gaspillage total d'eau (m³)",
            font=("Segoe UI", 11),
            text_color=self.COLORS["text_muted"]
        ).pack(anchor="w", padx=12, pady=(2, 10))

        self._build_subsection_title(card, "Contraintes")

        constraints = self._constraints(parcels, global_data)

        constraints_frame = ctk.CTkFrame(card, fg_color="transparent")
        constraints_frame.pack(fill="x", padx=18, pady=(4, 8))
        constraints_frame.grid_columnconfigure((0, 1), weight=1)

        for idx, (constraint, constraint_type) in enumerate(constraints):
            row, col = divmod(idx, 2)
            annotation = self._get_constraint_type_annotation(constraint_type)
            self._build_value_cell(
                constraints_frame, row, col,
                f"Contrainte ({idx + 1})",
                constraint,
                annotation
            )

        self._build_subsection_title(card, "Bornes")

        bounds_frame = ctk.CTkFrame(card, fg_color="transparent")
        bounds_frame.pack(fill="x", padx=18, pady=(4, 14))
        bounds_frame.grid_columnconfigure((0, 1), weight=1)

        for i, p in enumerate(parcels):
            row, col = divmod(i, 2)
            vol_min = p.get('vol_min', 0)
            self._build_value_cell(
                bounds_frame, row, col,
                f"Borne x{i+1}",
                f"x{i+1} ≥ {self._fmt(vol_min)}",
                f"Parcelle {p.get('id', i+1)}"
            )

        n_parcels = len(parcels)
        if n_parcels % 2 == 0:
            row = n_parcels // 2
            col = 0
        else:
            row = n_parcels // 2
            col = 1

        self._build_value_cell(
            bounds_frame, row, col,
            "Non-négativité",
            "xi ≥ 0",
            "Pour toutes les variables"
        )

    def _build_subsection_title(self, parent, text):
        """Titre de sous-section dans la carte."""
        title_frame = ctk.CTkFrame(parent, fg_color="transparent")
        title_frame.pack(fill="x", padx=18, pady=(12, 4))

        ctk.CTkLabel(
            title_frame,
            text=text,
            font=("Segoe UI", 13, "bold"),
            text_color=self.COLORS["primary_light"]
        ).pack(anchor="w")

    def _build_value_cell(self, parent, row: int, col: int, label: str, value, unit: str):
        """Cellule de valeur - IDENTIQUE à RecapPage."""
        cell = ctk.CTkFrame(parent, fg_color="#F8FAF9", corner_radius=12)
        cell.grid(row=row, column=col, padx=6, pady=6, sticky="ew")

        ctk.CTkLabel(
            cell,
            text=label,
            font=("Segoe UI", 11),
            text_color=self.COLORS["text_muted"],
        ).pack(anchor="w", padx=12, pady=(10, 2))

        ctk.CTkLabel(
            cell,
            text=str(value),
            font=("Consolas", 14, "bold"),
            text_color=self.COLORS["text"],
        ).pack(anchor="w", padx=12, pady=(2, 2))

        ctk.CTkLabel(
            cell,
            text=unit,
            font=("Segoe UI", 10),
            text_color=self.COLORS["text_muted"],
        ).pack(anchor="w", padx=12, pady=(0, 10))

    def _build_explanation_card(self, parent):
        """Carte d'interprétation - MEME STYLE que RecapPage."""
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
            text="Objectifs du modèle",
            font=("Segoe UI", 15, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(side="left")

        grid_frame = ctk.CTkFrame(card, fg_color="transparent")
        grid_frame.pack(fill="x", padx=18, pady=(4, 14))
        grid_frame.grid_columnconfigure((0, 1), weight=1)

        explanations = [
            ("", "Minimiser le gaspillage", "Réduire les pertes d'eau"),
            ("", "Respecter les besoins", "Croissance et production"),
            ("", "Volume minimal", "Eau nécessaire par parcelle"),
        ]

        for idx, (icon, title, desc) in enumerate(explanations):
            row, col = divmod(idx, 2)
            cell = ctk.CTkFrame(grid_frame, fg_color="#F8FAF9", corner_radius=12)
            cell.grid(row=row, column=col, padx=6, pady=6, sticky="ew")

            inner = ctk.CTkFrame(cell, fg_color="transparent")
            inner.pack(fill="x", padx=12, pady=10)

            ctk.CTkLabel(inner, text="", font=("Segoe UI", 18)).pack(side="left", padx=(0, 10))

            text_frame = ctk.CTkFrame(inner, fg_color="transparent")
            text_frame.pack(side="left", fill="x", expand=True)

            ctk.CTkLabel(
                text_frame,
                text=title,
                font=("Segoe UI", 12, "bold"),
                text_color=self.COLORS["text"]
            ).pack(anchor="w")

            ctk.CTkLabel(
                text_frame,
                text=desc,
                font=("Segoe UI", 11),
                text_color=self.COLORS["text_muted"]
            ).pack(anchor="w", pady=(2, 0))

    def _fmt(self, value):
        """Formate un nombre sans .00"""
        if value is None:
            return "0"
        if isinstance(value, float):
            if value.is_integer():
                return str(int(value))
            s = f"{value:.10f}".rstrip('0').rstrip('.')
            return s
        return str(value)

    def _constraints(self, parcels, global_data):
        cons = []

        if global_data.get("besoin_total_croissance"):
            growth_terms = []
            for i, p in enumerate(parcels):
                coeff = p.get('coeff_croissance', 1)
                growth_terms.append(f"{self._fmt(coeff)}·x{i+1}")
            constraint = " + ".join(growth_terms) + f" ≥ {self._fmt(global_data['besoin_total_croissance'])}"
            cons.append((constraint, "croissance"))

        if global_data.get("besoin_total_production"):
            production_terms = []
            for i, p in enumerate(parcels):
                coeff = p.get('coeff_production', 1)
                production_terms.append(f"{self._fmt(coeff)}·x{i+1}")
            constraint = " + ".join(production_terms) + f" ≥ {self._fmt(global_data['besoin_total_production'])}"
            cons.append((constraint, "production"))

        for i, p in enumerate(parcels):
            if p.get("vol_min"):
                cons.append((f"x{i+1} ≥ {self._fmt(p['vol_min'])}", "volume_min"))

        return cons

    def _get_constraint_type_annotation(self, constraint_type):
        annotations = {
            "croissance": "Besoin hydrique en croissance",
            "production": "Besoin hydrique en production",
            "volume_min": "Volume minimum par parcelle"
        }
        return annotations.get(constraint_type, "Contrainte technique")

    def _copy_linear_program(self, parcels, global_data):
        try:
            lp_text = self._format_lp_for_copy(parcels, global_data)
            self.clipboard_clear()
            self.clipboard_append(lp_text)
            self._show_copy_feedback()
        except Exception as e:
            self._show_error(f"Erreur lors de la copie: {str(e)}")

    def _format_lp_for_copy(self, parcels, global_data):
        lines = []
        lines.append("PROGRAMME LINEAIRE - OPTIMISATION IRRIGATION")
        lines.append("=" * 55)
        lines.append("")
        lines.append("VARIABLES:")
        for i, p in enumerate(parcels):
            lines.append(f"  x{i+1} = Volume d'eau parcelle {p.get('id', i+1)} (m³)")
        lines.append("")
        lines.append("OBJECTIF:")

        terms = []
        for i, p in enumerate(parcels):
            taux = p.get('taux_perte', 0)
            coeff = taux / 100
            terms.append(f"{self._fmt(coeff)}·x{i+1}")
        lines.append(f"  Min w = {' + '.join(terms)}")
        lines.append("")
        lines.append("CONTRAINTES:")
        constraints = self._constraints(parcels, global_data)
        for i, (constraint, _) in enumerate(constraints, 1):
            lines.append(f"  ({i}) {constraint}")
        lines.append("")
        lines.append("BORNES:")
        for i, p in enumerate(parcels):
            lines.append(f"  x{i+1} ≥ {self._fmt(p.get('vol_min', 0))}")
        lines.append("  xi ≥ 0  (pour tout i)")
        lines.append("")
        lines.append("PARAMETRES:")
        for i, p in enumerate(parcels):
            lines.append(f"  Parcelle {p.get('id', i+1)}:")
            lines.append(f"    Taux de perte: {self._fmt(p.get('taux_perte', 0))}%")
            lines.append(f"    Coeff croissance: {self._fmt(p.get('coeff_croissance', 1))}")
            lines.append(f"    Coeff production: {self._fmt(p.get('coeff_production', 1))}")
            lines.append(f"    Volume min: {self._fmt(p.get('vol_min', 0))} m³")
        if global_data:
            lines.append("  Globaux:")
            if global_data.get('besoin_total_croissance'):
                lines.append(f"    Besoin total croissance: {self._fmt(global_data['besoin_total_croissance'])} m³")
            if global_data.get('besoin_total_production'):
                lines.append(f"    Besoin total production: {self._fmt(global_data['besoin_total_production'])} m³")
        return "\n".join(lines)

    def _show_copy_feedback(self):
        feedback_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=self.COLORS["success"], corner_radius=10)
        feedback_frame.pack(fill="x", padx=50, pady=(5, 10))
        ctk.CTkLabel(feedback_frame, text="Programme linéaire copié dans le presse-papiers", font=("Segoe UI", 12, "bold"), text_color="white").pack(pady=8)
        self._schedule(2000, feedback_frame.destroy)

    def _show_error(self, message: str):
        self._clear_result()
        result_card = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color=self.COLORS["card"],
            corner_radius=15,
            border_width=1,
            border_color=self.COLORS["error"],
        )
        result_card.pack(fill="x", padx=50, pady=10)

        header = ctk.CTkFrame(result_card, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(16, 8))

        ctk.CTkLabel(header, text="Erreur", font=("Segoe UI", 16, "bold"), text_color=self.COLORS["error"]).pack(side="left")
        ctk.CTkLabel(result_card, text=message, font=("Segoe UI", 13), text_color=self.COLORS["text_muted"], justify="left").pack(fill="x", padx=20, pady=(0, 16))

    def _clear_result(self):
        if self._result_frame:
            self._result_frame.destroy()
            self._result_frame = None

        for child in self.scrollable_frame.winfo_children():
            if isinstance(child, ctk.CTkFrame):
                try:
                    if child.cget("border_color") in [self.COLORS["success"], self.COLORS["error"]]:
                        child.destroy()
                except:
                    pass

    def _on_retour(self):
        self.controller.show_page("recap")

    def _on_resoudre(self):
        parcels = self.controller.get_parcels()
        global_data = self.controller.get_global_model()

        if not parcels:
            self._show_error("Pas de données disponibles pour la résolution")
            return

        n_parcels = len(parcels)
        
        if n_parcels == 2:
            try:
                from model.graphique import afficher_graphique
                result = afficher_graphique(parcels, global_data, self.controller)
                
                if result and result.get('success'):
                    self._show_results(result, parcels)
                else:
                    self._show_error("Échec de la résolution avec la méthode graphique")
            except Exception as e:
                self._show_error(f"Erreur lors de la résolution graphique: {str(e)}")
        else:
            self.controller.show_page("dual_simplexe")

    def _show_results(self, result: Dict, parcels: List[Dict]):
        self._clear_result()

        result_card = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color=self.COLORS["card"],
            corner_radius=15,
            border_width=1,
            border_color=self.COLORS["success"],
        )
        result_card.pack(fill="x", padx=50, pady=10)

        header = ctk.CTkFrame(result_card, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(16, 8))

        ctk.CTkLabel(header, text="Solution Optimale", font=("Segoe UI", 16, "bold"), text_color=self.COLORS["success"]).pack(side="left")
        ctk.CTkLabel(header, text=f"Méthode: {result.get('method', 'N/A')}", font=("Segoe UI", 11), text_color=self.COLORS["text_muted"]).pack(side="right")

        values_frame = ctk.CTkFrame(result_card, fg_color="#F8FAF9", corner_radius=12)
        values_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(values_frame, text="Volumes d'eau optimaux:", font=("Segoe UI", 13, "bold"), text_color=self.COLORS["primary"]).pack(anchor="w", padx=15, pady=(12, 8))

        for i, val in enumerate(result.get("solution", [])):
            parcel = parcels[i]
            ctk.CTkLabel(values_frame, text=f"x{i+1} = {self._fmt(val)} m³  (parcelle {parcel.get('id', i+1)})", font=("Consolas", 12), text_color=self.COLORS["text"]).pack(anchor="w", padx=25, pady=2)

        cost_frame = ctk.CTkFrame(result_card, fg_color="transparent")
        cost_frame.pack(fill="x", padx=20, pady=(0, 16))

        ctk.CTkLabel(cost_frame, text="Gaspillage minimal:", font=("Segoe UI", 14, "bold"), text_color=self.COLORS["primary"]).pack(side="left")
        ctk.CTkLabel(cost_frame, text=f"{self._fmt(result.get('cout', 0))} m³", font=("Segoe UI", 14, "bold"), text_color=self.COLORS["primary_light"]).pack(side="left", padx=8)

    def reset(self):
        for widget in self.lp_container.winfo_children():
            widget.destroy()
        for widget in self.explanation_container.winfo_children():
            widget.destroy()
        self.desc_label.configure(text="Formulation mathématique du problème d'optimisation")


def _check_direct_execution():
    if len(sys.argv) > 0 and sys.argv[0].endswith('solution_page.py'):
        print("=" * 60)
        print("ERREUR: Accès direct non autorisé!")
        print("=" * 60)
        print("\nCette page ne peut pas être exécutée directement.")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    _check_direct_execution()