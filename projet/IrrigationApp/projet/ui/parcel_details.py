import customtkinter as ctk
from typing import Dict, List, Optional, Callable, Any


class ParcelDetailsPage(ctk.CTkFrame):
    """Page de configuration detaillee des parcelles et du modele global."""

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

    FIELD_CONFIG = {
        "nom": {
            "label": "Nom de la parcelle",
            "unit": None,
            "placeholder": "Ex: Tomates Serre ",
            "help": "Nom unique pour identifier la parcelle (1-50 caracteres, sans chiffres)",
            "type": "string",
            "min_len": 1, "max_len": 50,
        },
        "taux_perte": {
            "label": "Taux de perte d'eau",
            "unit": "%",
            "placeholder": "Ex: 5.0",
            "help": "Pourcentage d'eau perdue par evaporation",
            "min": 0, "max": 100,
        },
        "coeff_croissance": {
            "label": "Besoin hydrique croissance",
            "unit": "coeff",
            "placeholder": "Ex: 1.2",
            "help": "Coefficient multiplicateur en phase de croissance",
            "min": 0.1, "max": 10,
        },
        "coeff_production": {
            "label": "Besoin hydrique production",
            "unit": "coeff",
            "placeholder": "Ex: 1.5",
            "help": "Coefficient multiplicateur en phase de production",
            "min": 0.1, "max": 10,
        },
        "vol_min": {
            "label": "Volume minimal d'eau",
            "unit": "m3",
            "placeholder": "Ex: 100.0",
            "help": "Volume d'eau minimum requis pour la parcelle",
            "min": 1, "max": 999999,
        },
    }

    GLOBAL_CONFIG = {
        "besoin_total_croissance": {
            "label": "Besoin minimal total en croissance",
            "unit": "m3",
            "placeholder": "Ex: 500.0",
            "help": "Volume d'eau minimal total necessaire pour la phase de croissance",
            "min": 0, "max": 9999999,
        },
        "besoin_total_production": {
            "label": "Besoin minimal total en production",
            "unit": "m3",
            "placeholder": "Ex: 750.0",
            "help": "Volume d'eau minimal total necessaire pour la phase de production",
            "min": 0, "max": 9999999,
        },
    }

    def __init__(self, parent, controller):
        """
        Initialise la page de configuration détaillée des parcelles.
        
        Args:
            parent: Widget parent
            controller: Contrôleur de l'application
        """
        super().__init__(parent, fg_color=self.COLORS["card"])
        self.controller = controller

        self.entries: Dict[int, Dict[str, ctk.CTkEntry]] = {}
        self.status_labels: Dict[int, Dict[str, ctk.CTkLabel]] = {}
        self.parcel_badges: Dict[int, ctk.CTkLabel] = {}
        self.global_entries: Dict[str, ctk.CTkEntry] = {}
        self.global_status: Dict[str, ctk.CTkLabel] = {}
        self._after_ids: List[int] = []
        self._error_frames: List[ctk.CTkFrame] = []

        self.progress_bar = None
        self.progress_text = None
        self.desc_label = None
        self.global_card = None
        self.scrollable_frame = None
        self.global_badge = None

        self.build_ui()

    def destroy(self):
        """
        Nettoie les ressources avant la destruction du widget.
        Annule tous les after_ids en attente.
        """
        for after_id in self._after_ids:
            self.after_cancel(after_id)
        super().destroy()

    def _schedule(self, delay: int, callback: Callable):
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

    def _build_decorative_bg(self):
        """
        Construit l'arrière-plan décoratif (réservé pour usage futur).
        """
        pass

    def build_ui(self):
        """
        Construit l'interface utilisateur complète de la page.
        """
        self._build_decorative_bg()
        self._build_top_bar()
        self._build_main_content()
        self._build_action_buttons()

    def _build_top_bar(self):
        """
        Construit la barre supérieure avec le logo NeoFarm.
        """
        self.top_bar = ctk.CTkFrame(
            self, fg_color="#FFFFFF", corner_radius=0, height=50,
            border_width=1, border_color=self.COLORS["border"]
        )
        self.top_bar.pack(fill="x", side="top")
        self.top_bar.pack_propagate(False)

        logo_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        logo_frame.pack(side="left", padx=20, pady=10)

        ctk.CTkLabel(logo_frame, text="🌿", font=("Segoe UI", 18), text_color="#2e7d32").pack(side="left", padx=(0, 8))
        ctk.CTkLabel(logo_frame, text="NeoFarm", font=("Segoe UI", 14, "bold"), text_color="#2e7d32").pack(side="left")

    def _build_main_content(self):
        """
        Construit le contenu principal avec les formulaires de parcelles.
        """
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=self.COLORS["bg"],
            scrollbar_button_color=self.COLORS["primary_light"],
            scrollbar_button_hover_color=self.COLORS["primary"],
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=0, pady=0)

        self._build_header(self.scrollable_frame)
        self._build_parcel_forms_container(self.scrollable_frame)
        self._build_progress_section(self.scrollable_frame)
        self._build_global_model_section(self.scrollable_frame)

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
            text="Configuration des parcelles",
            font=("Segoe UI", 28, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(anchor="w")

        self.desc_label = ctk.CTkLabel(
            header_frame,
            text=f"Saisissez les donnees pour {self.controller.get_parcel_count()} parcelles",
            font=("Segoe UI", 15),
            text_color=self.COLORS["text_muted"],
        )
        self.desc_label.pack(anchor="w", pady=(5, 0))

    def _build_parcel_forms_container(self, parent):
        """
        Construit le conteneur pour les formulaires de parcelles.
        
        Args:
            parent: Widget parent
        """
        self.forms_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.forms_container.pack(fill="x", padx=50, pady=(10, 10))
        self.create_parcel_forms()

    def create_parcel_forms(self):
        """
        Crée les formulaires pour toutes les parcelles.
        Détruit les formulaires existants et en recrée de nouveaux.
        """
        n_parcels = self.controller.get_parcel_count()
        print(f"create_parcel_forms - n_parcels = {n_parcels}")

        for widget in self.forms_container.winfo_children():
            widget.destroy()

        if n_parcels <= 0:
            self._show_zero_parcel_warning()
            return

        print(f"Création de {n_parcels} formulaires de parcelles")
        for i in range(n_parcels):
            print(f"Création de la parcelle {i}")
            self._build_parcel_card(i)

    def _show_zero_parcel_warning(self):
        """
        Affiche un message d'avertissement quand aucune parcelle n'est configurée.
        """
        warning_frame = ctk.CTkFrame(self.forms_container, fg_color="#FFF8E1", corner_radius=16)
        warning_frame.pack(fill="x", pady=30)

        ctk.CTkLabel(
            warning_frame,
            text="Aucune parcelle configuree",
            font=("Segoe UI", 16, "bold"),
            text_color=self.COLORS["warning"],
        ).pack(pady=(20, 8))

        ctk.CTkLabel(
            warning_frame,
            text="Veuillez d'abord saisir le nombre de parcelles dans l'etape precedente.",
            font=("Segoe UI", 13),
            text_color=self.COLORS["text"],
        ).pack(pady=(0, 8))

        ctk.CTkButton(
            warning_frame,
            text="Retour a la saisie du nombre",
            fg_color=self.COLORS["warning"],
            hover_color="#F57C00",
            command=lambda: self.controller.show_page("parcelles"),
            height=36,
            font=("Segoe UI", 12, "bold"),
            corner_radius=10,
        ).pack(pady=(8, 20))

    def _build_parcel_card(self, parcel_index: int):
        """
        Construit la carte d'une parcelle avec ses champs de saisie.
        
        Args:
            parcel_index: Index de la parcelle à construire
        """
        card = ctk.CTkFrame(
            self.forms_container,
            fg_color=self.COLORS["card"],
            corner_radius=20,
            border_width=1,
            border_color=self.COLORS["border"],
        )
        card.pack(fill="x", pady=10)
        card.grid_columnconfigure((0, 1), weight=1)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(14, 8))

        stripe = ctk.CTkFrame(
            header, fg_color=self.COLORS["primary_light"], width=4, height=24, corner_radius=2
        )
        stripe.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            header,
            text=f"Parcelle {parcel_index + 1}",
            font=("Segoe UI", 15, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(side="left")

        badge = ctk.CTkLabel(
            header,
            text="  Incomplet  ",
            font=("Segoe UI", 10, "bold"),
            text_color="white",
            fg_color=self.COLORS["error"],
            corner_radius=10,
        )
        badge.pack(side="right")
        self.parcel_badges[parcel_index] = badge

        grid_frame = ctk.CTkFrame(card, fg_color="transparent")
        grid_frame.pack(fill="x", padx=18, pady=(4, 12))
        grid_frame.grid_columnconfigure((0, 1), weight=1)

        fields = list(self.FIELD_CONFIG.items())
        parcel_entries = {}
        parcel_status = {}

        for idx, (key, config) in enumerate(fields):
            row, col = divmod(idx, 2)
            field_container = ctk.CTkFrame(grid_frame, fg_color="transparent")
            field_container.grid(row=row, column=col, padx=6, pady=6, sticky="ew")

            label_frame = ctk.CTkFrame(field_container, fg_color="transparent")
            label_frame.pack(fill="x")

            ctk.CTkLabel(
                label_frame,
                text=f"{config['label']}",
                font=("Segoe UI", 11, "bold"),
                text_color=self.COLORS["text"],
            ).pack(side="left")

            unit_text = config.get("unit")
            if unit_text:
                ctk.CTkLabel(
                    label_frame,
                    text=f"({unit_text})",
                    font=("Segoe UI", 10),
                    text_color=self.COLORS["text_muted"],
                ).pack(side="left", padx=(4, 0))

            input_frame = ctk.CTkFrame(field_container, fg_color="transparent")
            input_frame.pack(fill="x", pady=(4, 0))

            entry = ctk.CTkEntry(
                input_frame,
                height=36,
                font=("Segoe UI", 12),
                placeholder_text=config["placeholder"],
                border_color=self.COLORS["border"],
                border_width=2,
                corner_radius=8,
            )
            entry.pack(side="left", fill="x", expand=True)
            entry.bind("<KeyRelease>", lambda e, p=parcel_index, k=key: self._on_field_change(p, k))
            entry.bind("<FocusOut>", lambda e, p=parcel_index, k=key: self._on_field_change(p, k))

            status_icon = ctk.CTkLabel(
                input_frame,
                text="•",
                font=("Segoe UI", 14, "bold"),
                text_color=self.COLORS["text_muted"],
                width=26,
            )
            status_icon.pack(side="right", padx=(6, 0))

            ctk.CTkLabel(
                field_container,
                text=config["help"],
                font=("Segoe UI", 9),
                text_color=self.COLORS["text_muted"],
            ).pack(anchor="w", pady=(2, 0))

            parcel_entries[key] = entry
            parcel_status[key] = status_icon

        self.entries[parcel_index] = parcel_entries
        self.status_labels[parcel_index] = parcel_status

    def _build_progress_section(self, parent):
        """
        Construit la section de progression avec barre et texte.
        
        Args:
            parent: Widget parent
        """
        progress_frame = ctk.CTkFrame(parent, fg_color="transparent")
        progress_frame.pack(fill="x", padx=50, pady=(5, 10))

        self.progress_text = ctk.CTkLabel(
            progress_frame,
            text="Progression : 0 %",
            font=("Segoe UI", 12, "bold"),
            text_color=self.COLORS["primary_light"],
        )
        self.progress_text.pack(anchor="w")

        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            height=6,
            corner_radius=3,
            fg_color="#D0E8D4",
            progress_color=self.COLORS["accent"],
        )
        self.progress_bar.pack(fill="x", pady=(4, 0))
        self.progress_bar.set(0)

    def _build_global_model_section(self, parent):
        """
        Construit la section du modèle global avec les contraintes globales.
        
        Args:
            parent: Widget parent
        """
        self.global_card = ctk.CTkFrame(
            parent,
            fg_color=self.COLORS["card"],
            corner_radius=20,
            border_width=1,
            border_color=self.COLORS["border"],
        )
        self.global_card.pack(fill="x", padx=50, pady=(10, 20))

        header = ctk.CTkFrame(self.global_card, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(14, 8))

        stripe = ctk.CTkFrame(
            header, fg_color=self.COLORS["primary_light"], width=4, height=24, corner_radius=2
        )
        stripe.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            header,
            text="Modele Global",
            font=("Segoe UI", 15, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="Independant des parcelles",
            font=("Segoe UI", 10),
            text_color=self.COLORS["text_muted"],
        ).pack(side="left", padx=(8, 0))

        self.global_badge = ctk.CTkLabel(
            header,
            text="  Incomplet  ",
            font=("Segoe UI", 10, "bold"),
            text_color="white",
            fg_color=self.COLORS["error"],
            corner_radius=10,
        )
        self.global_badge.pack(side="right")

        grid_frame = ctk.CTkFrame(self.global_card, fg_color="transparent")
        grid_frame.pack(fill="x", padx=18, pady=(4, 12))
        grid_frame.grid_columnconfigure((0, 1), weight=1)

        fields = list(self.GLOBAL_CONFIG.items())
        for idx, (key, config) in enumerate(fields):
            col = idx % 2
            self._build_global_field(grid_frame, col, config, key)

    def _build_global_field(self, parent, column: int, config: Dict[str, Any], key: str):
        field_container = ctk.CTkFrame(parent, fg_color="transparent")
        field_container.grid(row=0, column=column, padx=6, pady=6, sticky="ew")

        label_frame = ctk.CTkFrame(field_container, fg_color="transparent")
        label_frame.pack(fill="x")

        ctk.CTkLabel(
            label_frame,
            text=f"{config['label']}",
            font=("Segoe UI", 11, "bold"),
            text_color=self.COLORS["text"],
        ).pack(side="left")

        ctk.CTkLabel(
            label_frame,
            text=f"({config['unit']})",
            font=("Segoe UI", 10),
            text_color=self.COLORS["text_muted"],
        ).pack(side="left", padx=(4, 0))

        input_frame = ctk.CTkFrame(field_container, fg_color="transparent")
        input_frame.pack(fill="x", pady=(4, 0))

        entry = ctk.CTkEntry(
            input_frame,
            height=36,
            font=("Segoe UI", 12),
            placeholder_text=config["placeholder"],
            border_color=self.COLORS["border"],
            border_width=2,
            corner_radius=8,
        )
        entry.pack(side="left", fill="x", expand=True)

        entry.bind("<KeyRelease>", lambda e, k=key: self._on_global_field_change(k))
        entry.bind("<FocusOut>", lambda e, k=key: self._on_global_field_change(k))
        entry.bind("<FocusIn>", lambda e, ent=entry: ent.configure(
            border_color=self.COLORS["primary_light"], border_width=2
        ))

        status_icon = ctk.CTkLabel(
            input_frame,
            text="•",
            font=("Segoe UI", 14, "bold"),
            text_color=self.COLORS["text_muted"],
            width=26,
        )
        status_icon.pack(side="right", padx=(6, 0))

        ctk.CTkLabel(
            field_container,
            text=config["help"],
            font=("Segoe UI", 9),
            text_color=self.COLORS["text_muted"],
        ).pack(anchor="w", pady=(2, 0))

        self.global_entries[key] = entry
        self.global_status[key] = status_icon
        entry._config = config  

    def _build_action_buttons(self):
        """
        Construit les boutons d'action Retour et Continuer.
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

        self.btn_continuer = ctk.CTkButton(
            inner,
            text="Continuer",
            fg_color=self.COLORS["primary_light"],
            hover_color=self.COLORS["primary"],
            width=200,
            height=40,
            font=("Segoe UI", 12, "bold"),
            command=self._on_continuer,
            corner_radius=10,
            state="disabled",
        )
        self.btn_continuer.pack(side="right")

    def _bind_outline_hover(self, btn: ctk.CTkButton):
        """
        Lie les effets de survol pour un bouton avec style outline.
        
        Args:
            btn: Bouton à configurer
        """
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

    def _on_field_change(self, parcel_id: int, field_key: str):
        """
        Gère le changement de valeur dans un champ de parcelle.
        
        Args:
            parcel_id: ID de la parcelle
            field_key: Clé du champ modifié
        """
        entry = self.entries[parcel_id][field_key]
        self._validate_field(entry, field_key, parcel_id)
        self.update_progress()
        self._update_continue_button()

    def _on_global_field_change(self, field_key: str):
        """
        Gère le changement de valeur dans un champ global.
        
        Args:
            field_key: Clé du champ modifié
        """
        entry = self.global_entries[field_key]
        self._validate_global_field(entry, field_key)
        self.update_progress()        # met à jour la progression et le badge global
        self._update_continue_button()

    def _validate_field(self, entry: ctk.CTkEntry, field_key: str, parcel_id: int) -> bool:
        """
        Valide un champ de parcelle avec gestion des erreurs.
        
        Args:
            entry: Champ de saisie à valider
            field_key: Type de champ
            parcel_id: ID de la parcelle
            
        Returns:
            True si le champ est valide, False sinon
        """
        config = self.FIELD_CONFIG[field_key]
        raw = entry.get().strip()
        status_label = self.status_labels[parcel_id][field_key]

        if not raw:
            entry.configure(border_color=self.COLORS["border"], border_width=2)
            status_label.configure(text="•", text_color=self.COLORS["text_muted"])
            return False

        if field_key == "nom":
            try:
                if any(char.isdigit() for char in raw):
                    raise ValueError("Le nom ne doit pas contenir de chiffres")

                min_len = config.get("min_len", 1)
                max_len = config.get("max_len", 50)
                if min_len <= len(raw) <= max_len:
                    entry.configure(border_color=self.COLORS["success"], border_width=2)
                    status_label.configure(text="✓", text_color=self.COLORS["success"])
                    return True
                else:
                    raise ValueError(f"Longueur hors limites ({min_len}-{max_len})")
            except Exception as e:
                entry.configure(border_color=self.COLORS["error"], border_width=2)
                status_label.configure(text="✕", text_color=self.COLORS["error"])
                return False

        try:
            val = float(raw)
            if val < config["min"] or val > config["max"]:
                raise ValueError("Hors limites")
            entry.configure(border_color=self.COLORS["success"], border_width=2)
            status_label.configure(text="✓", text_color=self.COLORS["success"])
            return True
        except (ValueError, TypeError):
            entry.configure(border_color=self.COLORS["error"], border_width=2)
            status_label.configure(text="✕", text_color=self.COLORS["error"])
            return False

    def _validate_global_field(self, entry: ctk.CTkEntry, field_key: str) -> bool:
        """
        Valide un champ global avec gestion des erreurs.
        
        Args:
            entry: Champ de saisie à valider
            field_key: Type de champ
            
        Returns:
            True si le champ est valide, False sinon
        """
        config = entry._config  
        raw = entry.get().strip()
        status_label = self.global_status[field_key]

        if not raw:
            entry.configure(border_color=self.COLORS["border"], border_width=2)
            status_label.configure(text="•", text_color=self.COLORS["text_muted"])
            return False

        try:
            val = float(raw)
            if val < config["min"] or val > config["max"]:
                raise ValueError("Hors limites")
            entry.configure(border_color=self.COLORS["success"], border_width=2)
            status_label.configure(text="✓", text_color=self.COLORS["success"])
            return True
        except (ValueError, TypeError):
            entry.configure(border_color=self.COLORS["error"], border_width=2)
            status_label.configure(text="✕", text_color=self.COLORS["error"])
            return False

    def update_progress(self):
        """
        Met à jour la barre de progression et les badges de statut.
        Calcule le pourcentage de champs valides.
        """
        total_fields = 0
        valid_fields = 0

        for parcel_id, entries in self.entries.items():
            for field_key, entry in entries.items():
                total_fields += 1
                raw = entry.get().strip()
                if raw:
                    try:
                        config = self.FIELD_CONFIG[field_key]
                        if field_key == "nom":
                            min_len = config.get("min_len", 1)
                            max_len = config.get("max_len", 50)
                            if min_len <= len(raw) <= max_len and not any(char.isdigit() for char in raw):
                                valid_fields += 1
                        else:
                            val = float(raw)
                            if config["min"] <= val <= config["max"]:
                                valid_fields += 1
                    except (ValueError, TypeError):
                        pass

        for field_key, entry in self.global_entries.items():
            total_fields += 1
            if self._is_entry_valid(entry, entry._config):  
                valid_fields += 1

        pct = valid_fields / total_fields if total_fields else 0
        self.progress_bar.set(pct)
        self.progress_text.configure(
            text=f"Progression : {int(pct * 100)} %  ({valid_fields}/{total_fields} champs)"
        )

        for parcel_id, entries in self.entries.items():
            parcel_valid = sum(
                1 for field_key, entry in entries.items()
                if self._is_entry_valid(entry, self.FIELD_CONFIG[field_key], field_key)
            )

            badge = self.parcel_badges.get(parcel_id)
            if badge:
                if parcel_valid == len(entries):
                    badge.configure(text="  Complet  ", fg_color=self.COLORS["success"])
                elif parcel_valid > 0:
                    badge.configure(
                        text=f"  {parcel_valid}/{len(entries)}  ",
                        fg_color=self.COLORS["warning"],
                    )
                else:
                    badge.configure(text="  Incomplet  ", fg_color=self.COLORS["error"])

        global_valid = sum(
            1 for field_key, entry in self.global_entries.items()
            if self._is_entry_valid(entry, entry._config)
        )

        if hasattr(self, 'global_badge') and self.global_badge and self.global_badge.winfo_exists():
            total_global = len(self.global_entries)
            if global_valid == total_global and total_global > 0:
                self.global_badge.configure(text="  Complet  ", fg_color=self.COLORS["success"])
            elif global_valid > 0:
                self.global_badge.configure(
                    text=f"  {global_valid}/{total_global}  ",
                    fg_color=self.COLORS["warning"],
                )
            else:
                self.global_badge.configure(text="  Incomplet  ", fg_color=self.COLORS["error"])

    def _is_entry_valid(self, entry: ctk.CTkEntry, config: Dict, field_key: str = "") -> bool:
        """
        Vérifie si un champ de saisie est valide.
        
        Args:
            entry: Champ de saisie à vérifier
            config: Configuration du champ
            field_key: Type de champ (optionnel)
            
        Returns:
            True si le champ est valide, False sinon
        """
        raw = entry.get().strip()
        if not raw:
            return False

        if field_key == "nom":
            min_len = config.get("min_len", 1)
            max_len = config.get("max_len", 50)
            if not (min_len <= len(raw) <= max_len):
                return False
            return not any(char.isdigit() for char in raw)

        try:
            val = float(raw)
            min_val = config.get("min")
            max_val = config.get("max")
            if min_val is None or max_val is None:
                return False
            return min_val <= val <= max_val
        except (ValueError, TypeError):
            return False

    def _update_continue_button(self):
        """
        Met à jour l'état du bouton Continuer selon la validité des champs.
        Active le bouton seulement si tous les champs sont valides.
        """
        parcels_valid = True
        for parcel_id, entries in self.entries.items():
            for field_key, entry in entries.items():
                if not self._is_entry_valid(entry, self.FIELD_CONFIG[field_key], field_key):
                    parcels_valid = False
                    break
            if not parcels_valid:
                break

        global_valid = True
        for field_key, entry in self.global_entries.items():
            if not self._is_entry_valid(entry, entry._config):
                global_valid = False
                break

        is_valid = parcels_valid and global_valid and len(self.entries) > 0 and len(self.global_entries) > 0

        if is_valid:
            self.btn_continuer.configure(
                state="normal",
                fg_color=self.COLORS["primary_light"],
                text_color="white",
            )
        else:
            self.btn_continuer.configure(
                state="disabled",
                fg_color="#BDBDBD",
                text_color="#757575",
            )

    def _on_retour(self):
        """
        Gère le clic sur le bouton Retour.
        Efface les données et retourne à la page précédente.
        """
        self.controller.set_parcels([])
        self.controller.set_global_model({})
        
        self.controller.show_page("parcelles")

    def _on_continuer(self):
        """
        Gère le clic sur le bouton Continuer.
        Valide toutes les données et navigue vers la page récapitulative.
        """
        if not self._validate_all():
            self._shake_global_card()
            return

        parcels = self._collect_parcel_data()
        global_data = self._collect_global_data()

        self.controller.set_parcels(parcels)
        self.controller.set_global_model(global_data)
        self.controller.show_page("recap")

    def _validate_all(self) -> bool:
        """
        Valide tous les champs de toutes les parcelles et les champs globaux.
        
        Returns:
            True si tous les champs sont valides, False sinon
        """
        all_valid = True

        for parcel_id, entries in self.entries.items():
            for field_key, entry in entries.items():
                if not self._validate_field(entry, field_key, parcel_id):
                    all_valid = False

        for field_key, entry in self.global_entries.items():
            if not self._validate_global_field(entry, field_key):
                all_valid = False

        return all_valid

    def _collect_parcel_data(self) -> List[Dict[str, Any]]:
        """
        Collecte les données de toutes les parcelles saisies.
        
        Returns:
            Liste des dictionnaires avec les données de chaque parcelle
        """
        parcels = []
        for parcel_id, entries in self.entries.items():
            parcel_data = {
                "id": parcel_id,
                "nom": entries["nom"].get().strip(),
                "taux_perte": float(entries["taux_perte"].get()),
                "coeff_croissance": float(entries["coeff_croissance"].get()),
                "coeff_production": float(entries["coeff_production"].get()),
                "vol_min": float(entries["vol_min"].get()),
            }
            parcels.append(parcel_data)
        return parcels

    def _collect_global_data(self) -> Dict[str, float]:
        """
        Collecte les données globales saisies.
        
        Returns:
            Dictionnaire avec les besoins totaux en croissance et production
        """
        return {
            "besoin_total_croissance": float(self.global_entries["besoin_total_croissance"].get()),
            "besoin_total_production": float(self.global_entries["besoin_total_production"].get()),
        }

    def _shake_global_card(self):
        """
        Anime la carte globale avec un effet de secousse pour indiquer une erreur.
        """
        if not self.global_card:
            return

        shake_offsets = [-12, 12, -10, 10, -8, 8, -6, 6, -4, 4, -2, 2, 0]

        def do_shake(index=0):
            if index < len(shake_offsets):
                self.global_card.pack_configure(padx=50 + shake_offsets[index])
                self._schedule(30, lambda: do_shake(index + 1))
            else:
                self.global_card.pack_configure(padx=50)

        do_shake()

    def show_error(self, message: str):
        self._clear_errors()

        error_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#FFEBEE", corner_radius=12)
        error_frame.pack(fill="x", padx=50, pady=(5, 10), before=self.global_card)
        self._error_frames.append(error_frame)

        ctk.CTkLabel(
            error_frame,
            text=f"{message}",
            font=("Segoe UI", 12, "bold"),
            text_color=self.COLORS["error"],
        ).pack(padx=16, pady=10)

        self._schedule(5000, self._clear_errors)

    def _clear_errors(self):
        for frame in self._error_frames:
            if frame.winfo_exists():
                frame.destroy()
        self._error_frames.clear()

    def refresh_parcels(self):
        self.entries.clear()
        self.status_labels.clear()
        self.parcel_badges.clear()

        n_parcels = self.controller.get_parcel_count()
        if self.desc_label:
            self.desc_label.configure(text=f"Saisissez les donnees pour {n_parcels} parcelles")

        self.create_parcel_forms()
        self.update_progress()
        self._update_continue_button()

    def refresh_data(self):
        """Restaure les données saisies par l'utilisateur lors du retour à cette page."""
        parcels = self.controller.get_parcels()
        global_data = self.controller.get_global_model()
        n_parcels = self.controller.get_parcel_count()
        
        print(f"refresh_data - n_parcels = {n_parcels}, len(parcels) = {len(parcels) if parcels else 0}")
        
        current_parcels_count = len(self.entries)
        if current_parcels_count != n_parcels:
            print(f"Recréation des formulaires - ancien: {current_parcels_count}, nouveau: {n_parcels}")
            self.refresh_parcels()
        
        for parcel_id, entries in self.entries.items():
            for field_key, entry in entries.items():
                entry.delete(0, "end")
                self._validate_field(entry, field_key, parcel_id)
        
        for field_key, entry in self.global_entries.items():
            entry.delete(0, "end")
            self._validate_global_field(entry, field_key)
        
        if parcels and len(parcels) > 0:
            for parcel in parcels:
                parcel_id = parcel.get('id', 0)
                if parcel_id in self.entries:
                    entries = self.entries[parcel_id]
                    
                    for field_key, entry in entries.items():
                        value = parcel.get(field_key, '')
                        if value is not None and value != '':
                            entry.delete(0, "end")
                            entry.insert(0, str(value))
                            self._validate_field(entry, field_key, parcel_id)
        
        if global_data and len(global_data) > 0:
            for field_key, entry in self.global_entries.items():
                value = global_data.get(field_key, '')
                if value is not None and value != '':
                    entry.delete(0, "end")
                    entry.insert(0, str(value))
                    self._validate_global_field(entry, field_key)
        
        self.update_progress()
        self._update_continue_button()

    def load_demo_data(self):
        n_parcels = self.controller.get_parcel_count()
        if n_parcels <= 0:
            self.show_error("Aucune parcelle configuree !")
            return

        for parcel_id, entries in self.entries.items():
            values = {
                "nom": f"Parcelle {parcel_id + 1}",
                "taux_perte": f"{5.0 + parcel_id * 0.5:.1f}",
                "coeff_croissance": "1.2",
                "coeff_production": "1.5",
                "vol_min": f"{100.0 + parcel_id * 20:.1f}",
            }
            for key, val in values.items():
                entry = entries[key]
                entry.delete(0, "end")
                entry.insert(0, val)
                self._validate_field(entry, key, parcel_id)

        self.global_entries["besoin_total_croissance"].delete(0, "end")
        self.global_entries["besoin_total_croissance"].insert(0, "500.0")
        self._validate_global_field(self.global_entries["besoin_total_croissance"], "besoin_total_croissance")

        self.global_entries["besoin_total_production"].delete(0, "end")
        self.global_entries["besoin_total_production"].insert(0, "750.0")
        self._validate_global_field(self.global_entries["besoin_total_production"], "besoin_total_production")

        self.controller.load_demo_parcels(n_parcels)
        self.update_progress()
        self._update_continue_button()

    def reset(self):
        self.entries.clear()
        self.status_labels.clear()
        self.parcel_badges.clear()

        for entry in self.global_entries.values():
            entry.delete(0, "end")
            entry.configure(border_color=self.COLORS["border"])

        for status in self.global_status.values():
            status.configure(text="•", text_color=self.COLORS["text_muted"])

        if self.global_badge and self.global_badge.winfo_exists():
            self.global_badge.configure(text="  Incomplet  ", fg_color=self.COLORS["error"])

        self._clear_errors()
        self.create_parcel_forms()
        self.update_progress()
        self._update_continue_button()