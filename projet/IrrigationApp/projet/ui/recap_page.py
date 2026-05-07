import customtkinter as ctk
from typing import Dict, List, Any


class RecapPage(ctk.CTkFrame):

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
        "nom": ("Nom de la parcelle", ""),
        "taux_perte": ("Taux de perte d'eau", "%"),
        "coeff_croissance": ("Besoin hydrique croissance", "coeff"),
        "coeff_production": ("Besoin hydrique production", "coeff"),
        "vol_min": ("Volume minimal d'eau", "m³"),
    }

    GLOBAL_LABELS = {
        "besoin_total_croissance": ("Besoin minimal total en croissance", "m³"),
        "besoin_total_production": ("Besoin minimal total en production", "m³"),
    }

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=self.COLORS["bg"])
        self.controller = controller
        self._after_ids: List[int] = []
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
        self._build_global_section(self.scrollable_frame)

    def _build_header(self, parent):
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=50, pady=(30, 20))

        ctk.CTkLabel(
            header_frame,
            text="Récapitulatif des données",
            font=("Segoe UI", 28, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(anchor="w")

        self.desc_label = ctk.CTkLabel(
            header_frame,
            text="Vérifiez vos données avant de lancer la résolution",
            font=("Segoe UI", 15),
            text_color=self.COLORS["text_muted"],
        )
        self.desc_label.pack(anchor="w", pady=(5, 0))

    def _build_parcels_section(self, parent):
        """Section récapitulative des parcelles."""
        self.parcels_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.parcels_container.pack(fill="x", padx=50, pady=(10, 10))

    def _build_global_section(self, parent):
        """Section récapitulative du modèle global."""
        self.global_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.global_container.pack(fill="x", padx=50, pady=(10, 20))

    def _build_action_buttons(self):
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
            width=140,
            height=45,
            font=("Segoe UI", 12, "bold"),
            text_color=self.COLORS["primary"],
            border_width=2,
            border_color=self.COLORS["primary"],
            command=self._on_retour,
            corner_radius=12,
        )
        self.btn_retour.pack(side="left")
        self._bind_outline_hover(self.btn_retour)

        self.btn_resoudre = ctk.CTkButton(
            inner,
            text="Résoudre",
            fg_color=self.COLORS["primary_light"],
            hover_color=self.COLORS["primary"],
            width=140,
            height=45,
            font=("Segoe UI", 12, "bold"),
            command=self._on_resoudre,
            corner_radius=12,
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
        """Charge et affiche les données depuis le contrôleur."""
        for widget in self.parcels_container.winfo_children():
            widget.destroy()
        for widget in self.global_container.winfo_children():
            widget.destroy()

        parcels = self.controller.get_parcels()
        global_data = self.controller.get_global_model()
        n_parcels = len(parcels)

        self.desc_label.configure(
            text=f"{n_parcels} parcelles configurées — Vérifiez vos données avant de lancer la résolution"
        )

        if n_parcels > 0:
            ctk.CTkLabel(
                self.parcels_container,
                text="Données des parcelles",
                font=("Segoe UI", 18, "bold"),
                text_color=self.COLORS["primary"],
            ).pack(anchor="w", pady=(0, 12))

            for parcel in parcels:
                self._build_parcel_recap_card(self.parcels_container, parcel)

        if global_data:
            ctk.CTkLabel(
                self.global_container,
                text="Modèle Global",
                font=("Segoe UI", 18, "bold"),
                text_color=self.COLORS["primary"],
            ).pack(anchor="w", pady=(10, 12))

            self._build_global_recap_card(self.global_container, global_data)

    def _build_parcel_recap_card(self, parent, parcel: Dict[str, Any]):
        """Carte récap d'une parcelle."""
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
            text="  Validé  ",
            font=("Segoe UI", 10, "bold"),
            text_color="white",
            fg_color=self.COLORS["success"],
            corner_radius=10,
        ).pack(side="right")
        
        grid_frame = ctk.CTkFrame(card, fg_color="transparent")
        grid_frame.pack(fill="x", padx=18, pady=(4, 14))
        grid_frame.grid_columnconfigure((0, 1), weight=1)

        fields = [(key, (label, unit)) for key, (label, unit) in self.FIELD_LABELS.items() if key != 'nom']
        for idx, (key, (label, unit)) in enumerate(fields):
            row, col = divmod(idx, 2)
            value = parcel.get(key, "—")
            self._build_value_cell(grid_frame, row, col, label, value, unit)

    def _build_global_recap_card(self, parent, global_data: Dict[str, Any]):
        """Carte récap du modèle global."""
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
            text="  Validé  ",
            font=("Segoe UI", 10, "bold"),
            text_color="white",
            fg_color=self.COLORS["success"],
            corner_radius=10,
        ).pack(side="right")

        grid_frame = ctk.CTkFrame(card, fg_color="transparent")
        grid_frame.pack(fill="x", padx=18, pady=(4, 14))
        grid_frame.grid_columnconfigure((0, 1), weight=1)

        fields = list(self.GLOBAL_LABELS.items())
        for idx, (key, (label, unit)) in enumerate(fields):
            col = idx % 2
            value = global_data.get(key, "—")
            self._build_value_cell(grid_frame, 0, col, label, value, unit)

    def _build_value_cell(self, parent, row: int, col: int, label: str, value, unit: str):
        """Cellule de valeur stylisée."""
        cell = ctk.CTkFrame(parent, fg_color="#F8FAF9", corner_radius=12)
        cell.grid(row=row, column=col, padx=6, pady=6, sticky="ew")

        ctk.CTkLabel(
            cell,
            text=label,
            font=("Segoe UI", 11),
            text_color=self.COLORS["text_muted"],
        ).pack(anchor="w", padx=12, pady=(10, 2))

        if value == "—" or value is None or value == "":
            val_text = "—"
        elif isinstance(value, (int, float)):
            if value == int(value):
                val_text = f"{int(value)} {unit}" if unit else f"{int(value)}"
            else:
                val_text = f"{value:.2f} {unit}" if unit else f"{value:.2f}"
        else:
            val_text = f"{value} {unit}" if unit else str(value)
            
        ctk.CTkLabel(
            cell,
            text=val_text,
            font=("Segoe UI", 14, "bold"),
            text_color=self.COLORS["text"],
        ).pack(anchor="w", padx=12, pady=(2, 10))

    def _on_retour(self):
        """Retourne à la page de saisie des détails."""
        self.controller.show_page("parcel_details")

    def _on_resoudre(self):
        """Affiche la page de solution pour la résolution."""
        success = self.controller.show_page("solution")
        if not success:
            print("Accès à la solution refusé. Veuillez compléter toutes les étapes requises.")

    def reset(self):
        """Réinitialise la page."""
        for widget in self.parcels_container.winfo_children():
            widget.destroy()
        for widget in self.global_container.winfo_children():
            widget.destroy()
        self.desc_label.configure(
            text="Vérifiez vos données avant de lancer la résolution"
        )