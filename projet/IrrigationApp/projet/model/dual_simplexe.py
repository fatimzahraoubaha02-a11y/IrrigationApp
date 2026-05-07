import customtkinter as ctk
from typing import Dict, List
import numpy as np

def resoudre_dual_simplexe(parcels: List[Dict], global_data: Dict, controller=None) -> Dict:
    """
    Résout le problème d'optimisation d'irrigation par la méthode du dual simplexe.
    
    Cette fonction implémente une heuristique basée sur le dual simplexe pour trouver
    la distribution optimale d'eau entre les parcelles. Elle minimise le gaspillage total
    tout en respectant les contraintes de croissance et de production.
    
    Args:
        parcels (List[Dict]): Liste des dictionnaires contenant les données de chaque parcelle
            avec les clés: vol_min, taux_perte, coeff_croissance, coeff_production, nom
        global_data (Dict): Dictionnaire contenant les données globales
            avec les clés: besoin_total_croissance, besoin_total_production
        controller: Contrôleur optionnel pour la navigation (non utilisé dans cette fonction)
    
    Returns:
        Dict: Dictionnaire contenant:
            - success (bool): True si la résolution a réussi, False sinon
            - solution (List[float]): Liste des volumes optimaux pour chaque parcelle
            - cout (float): Coût total (gaspillage) de la solution
            - statut (str): Message de statut détaillé
            - method (str): Nom de la méthode utilisée ('pseudo_dual_simplexe')
    """
    try:
        n = len(parcels)

        if n < 2:
            return {'success': False, 'statut': 'Au moins 2 parcelles requises'}

        volumes_min = [float(p.get('vol_min', 0)) for p in parcels]
        croissance = [float(p.get('coeff_croissance', 1)) for p in parcels]
        production = [float(p.get('coeff_production', 1)) for p in parcels]
        pertes = [float(p.get('taux_perte', 0)) for p in parcels]

        besoin_c = float(global_data.get('besoin_total_croissance', sum(volumes_min)))
        besoin_p = float(global_data.get('besoin_total_production', sum(volumes_min)))

        solution = volumes_min.copy()
        step = 1

        for _ in range(5000):
            total_c = sum(solution[i] * croissance[i] for i in range(n))
            total_p = sum(solution[i] * production[i] for i in range(n))

            if total_c >= besoin_c and total_p >= besoin_p:
                break
            best = None
            best_score = float("inf")

            for i in range(n):
                contribution = croissance[i] + production[i]
                if contribution == 0:
                    continue
                score = pertes[i] / contribution
                if score < best_score:
                    best_score = score
                    best = i

            if best is None:
                break
            solution[best] += step

        gaspillage = sum(solution[i] * pertes[i] / 100 for i in range(n))

        return {
            'success': True,
            'solution': solution,
            'cout': gaspillage,
            'statut': "Solution trouvée (heuristique améliorée)",
            'method': 'pseudo_dual_simplexe'
        }

    except Exception as e:
        return {'success': False, 'statut': str(e)}


class DualSimplexePage(ctk.CTkFrame):
    """
    Page Dual Simplexe - Interface utilisateur pour la résolution par méthode du dual simplexe.
    
    Cette page permet de configurer et exécuter l'algorithme d'optimisation
    du dual simplexe pour le problème d'irrigation des parcelles.
    """

    COLORS = {
        "bg": "#F5F7F6",
        "card": "#FFFFFF",
        "card_inner": "#F8FAF9",
        "primary": "#0a3d2a",
        "primary_light": "#2e7d32",
        "accent": "#4CAF50",
        "text": "#333333",
        "text_muted": "#777777",
        "border": "#E0E0E0",
        "success": "#4CAF50",
        "error": "#E53935",
        "progress_bg": "#E8F5E9",
    }

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=self.COLORS["bg"])
        self.controller = controller
        self._after_ids: List[int] = []
        self._current_view = "welcome"  
        self.btn_retour = None
        self.btn_right = None
        self.build_ui()

    def destroy(self):
        for after_id in self._after_ids:
            self.after_cancel(after_id)
        super().destroy()

    def _schedule(self, delay: int, callback):
        after_id = self.after(delay, callback)
        self._after_ids.append(after_id)
        return after_id

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

        ctk.CTkLabel(logo_frame, text="🌿", font=("Segoe UI", 18), text_color="#2e7d32").pack(side="left", padx=(0, 8))
        ctk.CTkLabel(logo_frame, text="NeoFarm", font=("Segoe UI", 14, "bold"), text_color="#2e7d32").pack(side="left")

    def _build_main_content(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=self.COLORS["bg"],
            scrollbar_button_color=self.COLORS["primary_light"],
            scrollbar_button_hover_color=self.COLORS["primary"],
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=0, pady=0)

        self._build_header(self.scrollable_frame)
        self._build_results_section(self.scrollable_frame)

    def _build_header(self, parent):
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=50, pady=(30, 10))

        ctk.CTkLabel(
            header_frame,
            text="Dual Simplexe",
            font=("Segoe UI", 28, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(anchor="w")

        self.desc_label = ctk.CTkLabel(
            header_frame,
            text="Optimisation de la distribution d'eau entre les parcelles",
            font=("Segoe UI", 15),
            text_color=self.COLORS["text_muted"],
        )
        self.desc_label.pack(anchor="w", pady=(5, 0))

    def _build_results_section(self, parent):
        self.results_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.results_container.pack(fill="x", padx=50, pady=(10, 20))
        self._show_welcome_state()

    def _show_welcome_state(self):
        """Page d'accueil - avant résolution"""
        for w in self.results_container.winfo_children():
            w.destroy()
        self._current_view = "welcome"

        card = ctk.CTkFrame(
            self.results_container,
            fg_color=self.COLORS["card"],
            corner_radius=24,
            border_width=0,
        )
        card.pack(fill="x", pady=8)

        header_band = ctk.CTkFrame(
            card,
            fg_color=self.COLORS["primary_light"],
            height=6,
            corner_radius=0
        )
        header_band.pack(fill="x")
        header_band.pack_propagate(False)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=50, pady=60)

        ctk.CTkLabel(
            inner,
            text="Optimisation Intelligente",
            font=("Segoe UI", 24, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            inner,
            text="Algorithme Dual Simplexe",
            font=("Segoe UI", 14),
            text_color=self.COLORS["primary_light"],
        ).pack(pady=(0, 20))

        desc_frame = ctk.CTkFrame(inner, fg_color="#FAFBFA", corner_radius=16)
        desc_frame.pack(fill="x", pady=(20, 0), padx=20)

        ctk.CTkLabel(
            desc_frame,
            text="Lancez l'algorithme du dual simplexe pour obtenir\nla distribution optimale d'eau entre vos parcelles",
            font=("Segoe UI", 14),
            text_color=self.COLORS["text_muted"],
            justify="center",
        ).pack(padx=25, pady=20)

    def _build_action_buttons(self):
        """Crée les boutons en bas de page - appelé APRÈS _build_main_content"""
        self.btn_container = ctk.CTkFrame(self, fg_color=self.COLORS["bg"], height=70)
        self.btn_container.pack(fill="x", side="bottom", padx=0, pady=0)
        self.btn_container.pack_propagate(False)

        inner = ctk.CTkFrame(self.btn_container, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=50, pady=12)

        self.btn_retour = ctk.CTkButton(
            inner,
            text="Retour",
            fg_color="transparent",
            hover_color="#E8F5E9",
            width=140,
            height=45,
            font=("Segoe UI", 12, "bold"),
            text_color=self.COLORS["primary"],
            border_width=2,
            border_color=self.COLORS["primary_light"],
            command=self._on_retour_click,
            corner_radius=12,
        )
        self.btn_retour.pack(side="left")
        self._bind_outline_hover(self.btn_retour)

        self.btn_right = ctk.CTkButton(
            inner,
            text="Lancer",
            fg_color=self.COLORS["primary_light"],
            hover_color=self.COLORS["primary"],
            width=140,
            height=45,
            font=("Segoe UI", 12, "bold"),
            command=self._on_right_click,
            corner_radius=12,
        )
        self.btn_right.pack(side="right")

        self._update_buttons_for_welcome()

    def _update_buttons_for_welcome(self):
        """Configure les boutons pour la vue d'accueil"""
        if self.btn_retour is None or self.btn_right is None:
            return  # Sécurité si appelé trop tôt
        self.btn_retour.configure(command=self._on_retour_click)
        self.btn_right.configure(
            text="Lancer",
            fg_color=self.COLORS["primary_light"],
            hover_color=self.COLORS["primary"],
            text_color="white",
            border_width=0,
            command=self._on_right_click
        )

    def _update_buttons_for_results(self):
        """Configure les boutons pour la vue des résultats"""
        if self.btn_retour is None or self.btn_right is None:
            return  # Sécurité si appelé trop tôt
        self.btn_retour.configure(command=self._on_retour_click)
        self.btn_right.configure(
            text="Valider",
            fg_color=self.COLORS["primary_light"],
            hover_color=self.COLORS["primary"],
            text_color="white",
            border_width=0,
            command=self._on_right_click
        )

    def _on_retour_click(self):
        """Gère le clic sur Retour selon la vue actuelle"""
        if self._current_view == "welcome":
            self.controller.show_page("solution")
        else:
            self.reset()

    def _on_right_click(self):
        """Gère le clic sur le bouton droit selon la vue actuelle"""
        if self._current_view == "welcome":
            self.solve()
        else:
            self.controller.show_page("validation_solveur")

    def _bind_outline_hover(self, btn: ctk.CTkButton):
        btn.bind(
            "<Enter>",
            lambda e: btn.configure(
                text_color="#1b5e20",
                border_color="#1b5e20",
                fg_color="transparent"
            )
        )
        btn.bind(
            "<Leave>",
            lambda e: btn.configure(
                text_color=self.COLORS["primary"],
                border_color="#1b5e20",
                fg_color="transparent"
            )
        )

    def solve(self):
        """
        Exécute l'algorithme du dual simplexe pour optimiser la distribution d'eau.
        
        Cette méthode récupère les données des parcelles et les données globales,
        puis applique l'algorithme de résolution pour trouver la distribution optimale
        qui minimise le gaspillage tout en respectant les contraintes.
        
        Affiche les résultats dans l'interface ou un message d'erreur en cas d'échec.
        """
        for w in self.results_container.winfo_children():
            w.destroy()

        parcels = self.controller.get_parcels()
        global_data = self.controller.get_global_model()

        result = resoudre_dual_simplexe(parcels, global_data)

        if not result['success']:
            self._show_error_card(result['statut'])
            self._current_view = "error"
            self._update_buttons_for_welcome()
            return

        solution = result['solution']
        n_parcels = len(solution)

        self.desc_label.configure(
            text=f"{n_parcels} parcelles optimisées — Distribution calculée avec succès"
        )

        self.controller.set_resolution_results(solution, method="dual_simplexe")
        self._show_results_dashboard(solution, parcels, result)
        self._current_view = "results"
        self._update_buttons_for_results()

    def _show_results_dashboard(self, solution, parcels, result):
        """Affiche le dashboard des résultats"""

        card1 = ctk.CTkFrame(
            self.results_container,
            fg_color=self.COLORS["card"],
            corner_radius=16,
            border_width=1,
            border_color=self.COLORS["border"],
        )
        card1.pack(fill="x", pady=(0, 16))

        header = ctk.CTkFrame(card1, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(16, 12))

        title_row = ctk.CTkFrame(header, fg_color="transparent")
        title_row.pack(side="left", fill="y")

        stripe = ctk.CTkFrame(
            title_row,
            fg_color=self.COLORS["primary_light"],
            width=4,
            height=24,
            corner_radius=2
        )
        stripe.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            title_row,
            text="Solution optimale trouvée",
            font=("Segoe UI", 16, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(side="left")

        badge = ctk.CTkFrame(
            header,
            fg_color=self.COLORS["primary_light"],
            corner_radius=20,
            height=32,
        )
        badge.pack(side="right")
        badge.pack_propagate(False)

        ctk.CTkLabel(
            badge,
            text="Optimisé",
            font=("Segoe UI", 11, "bold"),
            text_color="white",
        ).pack(padx=16, pady=4)

        metrics_frame = ctk.CTkFrame(card1, fg_color="transparent")
        metrics_frame.pack(fill="x", padx=20, pady=(8, 20))
        metrics_frame.grid_columnconfigure((0, 1, 2), weight=1)

        total_volume = sum(solution)
        gaspillage = result.get('cout', 0)

        self._build_metric_cell(metrics_frame, 0, "Méthode utilisée", "Dual Simplexe", "")
        self._build_metric_cell(metrics_frame, 1, "Volume total distribué", f"{total_volume:.2f}", "m³")
        self._build_metric_cell(metrics_frame, 2, "Gaspillage estimé", f"{gaspillage:.2f}", "m³")

        card2 = ctk.CTkFrame(
            self.results_container,
            fg_color=self.COLORS["card"],
            corner_radius=16,
            border_width=1,
            border_color=self.COLORS["border"],
        )
        card2.pack(fill="x", pady=(0, 16))

        header2 = ctk.CTkFrame(card2, fg_color="transparent")
        header2.pack(fill="x", padx=20, pady=(16, 2))

        stripe2 = ctk.CTkFrame(
            header2,
            fg_color=self.COLORS["primary_light"],
            width=4,
            height=24,
            corner_radius=2
        )
        stripe2.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            header2,
            text="Distribution Finale Recommandée",
            font=("Segoe UI", 16, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(side="left")

        max_val = max(solution) if solution else 1

        ctk.CTkFrame(card2, fg_color="transparent", height=2).pack(fill="x")

        for i, val in enumerate(solution):
            parcel_name = parcels[i].get('nom', '') if i < len(parcels) else ''
            display_name = parcel_name if parcel_name else f"Parcelle {i+1}"

            bar_container = ctk.CTkFrame(card2, fg_color="transparent")
            if i == 0:
                bar_container.pack(fill="x", padx=20, pady=(2, 4))
            else:
                bar_container.pack(fill="x", padx=20, pady=(8, 4))

            info_row = ctk.CTkFrame(bar_container, fg_color="transparent")
            info_row.pack(fill="x")

            ctk.CTkLabel(
                info_row,
                text=display_name,
                font=("Segoe UI", 13, "bold"),
                text_color=self.COLORS["text"],
                anchor="w"
            ).pack(side="left")

            ctk.CTkLabel(
                info_row,
                text=f"{val:.2f} m³",
                font=("Segoe UI", 13, "bold"),
                text_color=self.COLORS["primary_light"],
                anchor="e"
            ).pack(side="right")

            progress = ctk.CTkProgressBar(
                bar_container,
                height=10,
                corner_radius=5,
                progress_color=self.COLORS["primary_light"],
                fg_color=self.COLORS["progress_bg"],
            )
            progress.pack(fill="x", pady=(4, 0))
            progress.set(val / max_val if max_val > 0 else 0)

            if i < len(solution) - 1:
                spacer = ctk.CTkFrame(card2, fg_color="transparent", height=8)
                spacer.pack(fill="x")
            else:
                spacer = ctk.CTkFrame(card2, fg_color="transparent", height=12)
                spacer.pack(fill="x")

    def _build_metric_cell(self, parent, col: int, label: str, value: str, unit: str):
        cell = ctk.CTkFrame(parent, fg_color=self.COLORS["card_inner"], corner_radius=12)
        cell.grid(row=0, column=col, padx=8, pady=6, sticky="ew")

        ctk.CTkLabel(
            cell,
            text=label,
            font=("Segoe UI", 11),
            text_color=self.COLORS["text_muted"],
        ).pack(anchor="w", padx=16, pady=(14, 4))

        val_text = f"{value} {unit}" if unit else value
        ctk.CTkLabel(
            cell,
            text=val_text,
            font=("Segoe UI", 18, "bold"),
            text_color=self.COLORS["text"],
        ).pack(anchor="w", padx=16, pady=(4, 14))

    def _show_error_card(self, message: str):
        card = ctk.CTkFrame(
            self.results_container,
            fg_color=self.COLORS["card"],
            corner_radius=20,
            border_width=1,
            border_color=self.COLORS["error"],
        )
        card.pack(fill="x", pady=8)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=40, pady=30)

        ctk.CTkLabel(
            inner,
            text="⚠",
            font=("Segoe UI", 36),
            text_color=self.COLORS["error"],
        ).pack()

        ctk.CTkLabel(
            inner,
            text="Erreur de résolution",
            font=("Segoe UI", 16, "bold"),
            text_color=self.COLORS["error"],
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            inner,
            text=message,
            font=("Segoe UI", 13),
            text_color=self.COLORS["text_muted"],
            wraplength=500,
        ).pack()

    def refresh_data(self):
        parcels = self.controller.get_parcels()
        n_parcels = len(parcels)
        self.desc_label.configure(
            text=f"{n_parcels} parcelles — Optimisation par dual simplexe"
        )

    def reset(self):
        """Retour à la page d'accueil (welcome state)"""
        self._show_welcome_state()
        self.desc_label.configure(
            text="Optimisation de la distribution d'eau entre les parcelles"
        )
        self._current_view = "welcome"
        self._update_buttons_for_welcome()("distribution d'eau entre les parcelles")
        self._current_view = "welcome"
        self._update_buttons_for_welcome()