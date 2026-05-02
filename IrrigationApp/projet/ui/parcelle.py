import customtkinter as ctk
from typing import Optional, Callable


class ParcellePage(ctk.CTkFrame):
    """
    Page de saisie du nombre de parcelles.
    Permet à l'utilisateur de définir le nombre de parcelles à optimiser.
    """

    COLORS = {
        "primary": "#0a3d2a",
        "primary_light": "#2e7d32",
        "accent": "#085B0B",
        "bg": "#F5F9F7",
        "card": "#FFFFFF",
        "text": "#333333",
        "text_muted": "#777777",
        "border": "#E0E0E0",
        "success": "#4CAF50",
        "error": "#E53935",
        "warning": "#FF9800",
    }

    MIN_PARCELLES = 2
    MAX_PARCELLES = 100

    CARD_WIDTH = 600
    CARD_HEIGHT = 520
    INPUT_WIDTH = 240
    INPUT_HEIGHT = 42      
    BUTTON_WIDTH = 170
    BUTTON_HEIGHT = 46
    COUNTER_SIZE = 38          
    COUNTER_FONT = 16          
    CONTENT_PADX = 50
    CONTENT_PADY = 40

    def __init__(self, parent, controller):
        """
        Initialise la page de saisie du nombre de parcelles.
        
        Args:
            parent: Widget parent
            controller: Contrôleur de l'application
        """
        super().__init__(parent, fg_color=self.COLORS["bg"])
        self.controller = controller

        self._current_value: Optional[int] = None
        self._is_valid = False
        self._after_ids = []

        self.build_ui()
        self._animate_entry()

    def destroy(self):
        """
        Nettoie les ressources avant la destruction du widget.
        Annule tous les after_ids en attente.
        """
        for after_id in self._after_ids:
            self.after_cancel(after_id)
        super().destroy()

    def _schedule(self, delay, callback):
        """
        Planifie un appel de fonction après un certain délai.
        
        Args:
            delay: Délai en millisecondes
            callback: Fonction à appeler
        
        Returns:
            ID de l'appel planifié
        """
        after_id = self.after(delay, callback)
        self._after_ids.append(after_id)
        return after_id

    def build_ui(self):
        """
        Construit l'interface utilisateur complète de la page.
        """
        self._build_decorative_bg()
        self._build_top_bar()
        self._build_hero_section()
        self._build_footer()

    def _build_hero_section(self):
        self.hero_container = ctk.CTkFrame(self, fg_color="transparent")
        self.hero_container.pack(fill="both", expand=True)

        self.card_wrapper = ctk.CTkFrame(self.hero_container, fg_color="transparent")
        self.card_wrapper.place(relx=0.5, rely=0.52, anchor="center")

        self._build_shadow(self.card_wrapper, layers=3, offset=5, base_color="#d0d0d0")

        self.card = ctk.CTkFrame(
            self.card_wrapper,
            fg_color=self.COLORS["card"],
            corner_radius=18,
            border_width=1,
            border_color=self.COLORS["border"],
            width=self.CARD_WIDTH,
            height=self.CARD_HEIGHT,
        )
        self.card.pack()
        self.card.pack_propagate(False)

        self._build_left_stripe()

        content = ctk.CTkFrame(self.card, fg_color="transparent")
        content.pack(padx=self.CONTENT_PADX, pady=self.CONTENT_PADY, fill="both", expand=True)

        self._build_step_indicator(content)
        self._build_header(content)
        self._build_input_section(content)
        self._build_error_display(content)
        self._build_buttons(content)

    def _build_shadow(self, parent, layers: int, offset: int, base_color: str):
        for i in range(layers):
            color = self._lighten_color(base_color, i * 8)
            layer_offset = offset - i
            shadow = ctk.CTkFrame(
                parent,
                fg_color=color,
                corner_radius=20,
                width=self.CARD_WIDTH,
                height=self.CARD_HEIGHT
            )
            shadow.place(x=layer_offset, y=layer_offset)

    def _build_left_stripe(self):
        ctk.CTkFrame(
            self.card,
            fg_color=self.COLORS["primary_light"],
            width=4,
            corner_radius=2
        ).place(x=0, y=22, relheight=0.88)

    def _build_step_indicator(self, parent):
        step_frame = ctk.CTkFrame(parent, fg_color="transparent")
        step_frame.pack(fill="x", pady=(0, 18))

        ctk.CTkLabel(
            step_frame,
            text="ÉTAPE 2 / 3",
            font=("Segoe UI", 11, "bold"),
            text_color=self.COLORS["primary_light"],
            fg_color="#E8F5E9",
            corner_radius=10,
            padx=10,
            pady=4,
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            step_frame,
            text="Nombre de parcelles",
            font=("Segoe UI", 12),
            text_color=self.COLORS["text_muted"],
        ).pack(side="left")

    def _build_progress_bar(self, parent):
        pass

    def _build_header(self, parent):
        ctk.CTkLabel(
            parent,
            text="Saisir Le nombre de Parcelles",
            font=("Segoe UI", 22, "bold"),
            text_color=self.COLORS["primary"],
        ).pack(pady=(8, 0))

        ctk.CTkLabel(
            parent,
            text=f"Entrez le nombre de parcelles à optimiser",
            font=("Segoe UI", 12),
            text_color=self.COLORS["text_muted"],
        ).pack(pady=(10, 24))

    def _build_input_section(self, parent):
        """Champ de saisie centré avec boutons +/- compacts de part et d'autre."""
        input_row = ctk.CTkFrame(parent, fg_color="transparent")
        input_row.pack()

        self.btn_minus = self._create_counter_button(
            input_row, "−", self._decrement, side="left", padx=(0, 10)
        )

        input_frame = ctk.CTkFrame(input_row, fg_color="transparent")
        input_frame.pack(side="left")

        self.entry = ctk.CTkEntry(
            input_frame,
            width=self.INPUT_WIDTH,
            height=self.INPUT_HEIGHT,
            font=("Segoe UI", 16),         
            placeholder_text=f"Ex: {self.MIN_PARCELLES}",
            justify="center",
            fg_color="#FFFFFF",
            border_color=self.COLORS["border"],
            border_width=1,
            corner_radius=10,
        )
        self.entry.pack()

        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        self.entry.bind("<KeyRelease>", lambda e: self._validate_input())
        self.entry.bind("<Return>", lambda e: self.submit())


        self.btn_plus = self._create_counter_button(
            input_row, "+", self._increment, side="left", padx=(10, 0)
        )

        ctk.CTkLabel(
            parent,
            text=f"Minimum {self.MIN_PARCELLES} parcelles requises",
            font=("Segoe UI", 12),
            text_color=self.COLORS["text_muted"],
        ).pack(pady=(16, 0))

    def _create_counter_button(self, parent, text: str, command: Callable, side: str, padx: tuple):
        """Bouton +/- compact (38x38) avec police réduite."""
        btn = ctk.CTkButton(
            parent,
            text=text,
            font=("Segoe UI", self.COUNTER_FONT, "bold"),
            width=self.COUNTER_SIZE,
            height=self.COUNTER_SIZE,
            corner_radius=10,          
            fg_color="#EFEFEF",
            hover_color="#E0E0E0",
            text_color="#555555",
            command=command,
        )
        btn.pack(side=side, padx=padx)
        return btn

    def _build_error_display(self, parent):
        self.error_label = ctk.CTkLabel(
            parent,
            text="",
            font=("Segoe UI", 12, "bold"),
            text_color=self.COLORS["error"],
        )
        self.error_label.pack(pady=(12, 0))

    def _build_buttons(self, parent):
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(pady=(30, 12))

        self.btn_retour = self._create_outline_button(
            btn_frame,
            text="Retour",
            command=lambda: self.controller.show_page("home"),
        )
        self.btn_retour.pack(side="left", padx=8)

        self.btn_continue = ctk.CTkButton(
            btn_frame,
            text="Continuer",
            fg_color=self.COLORS["primary_light"],
            hover_color=self.COLORS["primary"],
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            corner_radius=10,
            font=("Segoe UI", 13, "bold"),
            command=self.submit,
            state="disabled",
        )
        self.btn_continue.pack(side="left", padx=8)

    def _create_outline_button(self, parent, text: str, command: Callable):
        btn = ctk.CTkButton(
            parent,
            text=text,
            fg_color="transparent",
            hover_color="#E8F5E9",
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            corner_radius=10,
            font=("Segoe UI", 13, "bold"),
            text_color=self.COLORS["primary"],
            border_width=2,
            border_color=self.COLORS["primary"],
            command=command,
        )

        btn.bind("<Enter>", lambda e: btn.configure(text_color="#1b5e20", border_color="#1b5e20"))
        btn.bind("<Leave>", lambda e: btn.configure(text_color=self.COLORS["primary"], border_color=self.COLORS["primary"]))
        return btn

    def _build_footer(self):
        footer = ctk.CTkFrame(
            self,
            fg_color=self.COLORS["primary"],
            height=48,
            corner_radius=0
        )
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        ctk.CTkLabel(
            footer,
            text="NeoFarm  2026 — Solutions d'irrigation intelligente",
            font=("Segoe UI", 11),
            text_color="#88bfa3",
        ).pack(expand=True)

    def _on_focus_in(self, event=None):
        self.entry.configure(border_color=self.COLORS["primary_light"], border_width=2)

    def _on_focus_out(self, event=None):
        self.entry.configure(border_color=self._get_border_color(), border_width=1)

    def _increment(self):
        current = self._get_current_value() or self.MIN_PARCELLES - 1
        self._set_value(min(current + 1, self.MAX_PARCELLES))

    def _decrement(self):
        current = self._get_current_value() or self.MIN_PARCELLES + 1
        self._set_value(max(current - 1, 1))

    def _get_current_value(self) -> Optional[int]:
        try:
            text = self.entry.get().strip()
            return int(text) if text else None
        except ValueError:
            return None

    def _set_value(self, value: int):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(value))
        self._validate_input()

    def _validate_input(self):
        value = self._get_current_value()
        self._current_value = value

        if value is None:
            self._show_error("")
            self._set_continue_state(False)
        elif value < self.MIN_PARCELLES:
            self._show_error(f"Minimum {self.MIN_PARCELLES} parcelles requises")
            self._set_continue_state(False)
        elif value > self.MAX_PARCELLES:
            self._show_error(f"Maximum {self.MAX_PARCELLES} parcelles autorisees")
            self._set_continue_state(False)
        else:
            self._show_error("")
            self._set_continue_state(True)

    def _show_error(self, message: str):
        self.error_label.configure(text=message)

    def _set_continue_state(self, enabled: bool):
        self._is_valid = enabled
        state = "normal" if enabled else "disabled"
        self.btn_continue.configure(state=state)

        if enabled:
            self.btn_continue.configure(fg_color=self.COLORS["primary_light"], text_color="white")
        else:
            self.btn_continue.configure(fg_color="#BDBDBD", text_color="#757575")

    def _get_border_color(self) -> str:
        return self.COLORS["error"] if self.error_label.cget("text") else self.COLORS["border"]

    def submit(self):
        if not self._is_valid or self._current_value is None:
            self._shake_card()
            return

        self.controller.set_parcel_count(self._current_value)
        self.controller.show_page("parcel_details")

    def _shake_card(self):
        original_x = 0
        shake_offsets = [-10, 10, -8, 8, -6, 6, -4, 4, -2, 2, 0]

        def do_shake(index=0):
            if index < len(shake_offsets):
                self.card_wrapper.place_configure(x=original_x + shake_offsets[index])
                self._schedule(40, lambda: do_shake(index + 1))
            else:
                self.card_wrapper.place_configure(x=original_x)

        do_shake()

    def _animate_entry(self):
        start_y, end_y = 0.65, 0.52
        duration, steps = 650, 32
        delay = duration // steps

        def step(i):
            if i <= steps:
                progress = i / steps
                eased = 1 - (1 - progress) ** 3
                current_y = start_y - (start_y - end_y) * eased
                self.card_wrapper.place_configure(rely=current_y)
                self._schedule(delay, lambda: step(i + 1))

        step(0)

    def _lighten_color(self, hex_color: str, amount: int) -> str:
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = tuple(min(255, c + amount) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)

    def reset(self):
        self.entry.delete(0, "end")
        self._show_error("")
        self._set_continue_state(False)
        self._current_value = None

    def set_value(self, value: int):
        self._set_value(value)

    def _build_decorative_bg(self):
        pass

    def refresh_parcels(self):
        """Méthode appelée par le contrôleur pour marquer cette étape comme complétée."""
        pass

    def refresh_data(self):
        """Restaure le nombre de parcelles lorsque l'on retourne sur cette page."""
        parcel_count = self.controller.get_parcel_count()
        if parcel_count and parcel_count > 0:
            self._set_value(parcel_count)
            self._validate_input()

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