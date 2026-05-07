import customtkinter as ctk


class SavoirPlusPage(ctk.CTkFrame):

    COLORS = {
        "vert_fonce": "#0a3d2a",
        "vert_clair": "#2e7d32",
        "vert_hover": "#1b5e20",
        "vert_pale": "#E8F5E9",
        "vert_tres_pale": "#F5FBF8",
        "blanc": "#FFFFFF",
        "text_principal": "#1a1a1a",
        "text_secondaire": "#555555",
        "text_tertiaire": "#888888",
        "bordure": "#C8E6C9",
        "bordure_grise": "#E8EBE9",
        "success": "#10b981",
        "info": "#2e7d32",
        "warning": "#1b5e20",
        "danger": "#0a3d2a",
    }

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=self.COLORS["vert_tres_pale"])
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        self._build_top_bar()
        self._build_content()
        self._build_footer()

    def _build_top_bar(self):
        self.top_bar = ctk.CTkFrame(
            self, fg_color="#FFFFFF", corner_radius=0, height=50,
            border_width=1, border_color=self.COLORS["bordure_grise"]
        )
        self.top_bar.pack(fill="x", side="top")
        self.top_bar.pack_propagate(False)

        logo_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        logo_frame.pack(side="left", padx=20, pady=10)

        ctk.CTkLabel(logo_frame, text="🌿", font=("Segoe UI", 18), text_color="#2e7d32").pack(side="left", padx=(0, 8))
        ctk.CTkLabel(logo_frame, text="NeoFarm", font=("Segoe UI", 14, "bold"), text_color="#2e7d32").pack(side="left")
        ctk.CTkLabel(
            self.top_bar,
            text="En savoir plus",
            font=("Segoe UI", 13),
            text_color="#888888"
        ).pack(side="right", padx=20, pady=10)

    def _build_content(self):
        self.scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_button_color=self.COLORS["vert_clair"],
            scrollbar_button_hover_color=self.COLORS["vert_hover"],
        )
        self.scroll.pack(fill="both", expand=True, padx=0, pady=0)

        self.main_container = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.main_container.pack(fill="x", expand=True, padx=80)

        self._build_hero()
        self._build_workflow()
        self._build_details()
        self._build_methods()
        self._build_validation()
        self._build_cta()

    def _build_hero(self):
        hero = ctk.CTkFrame(
            self.main_container, fg_color=self.COLORS["vert_fonce"],
            corner_radius=20
        )
        hero.pack(fill="x", pady=(20, 0))

        content = ctk.CTkFrame(hero, fg_color="transparent")
        content.pack(fill="x", padx=45, pady=40)

        badge = ctk.CTkFrame(content, fg_color="#0f5238", corner_radius=15)
        badge.pack(anchor="w")
        ctk.CTkLabel(
            badge,
            text="SYSTEME D'OPTIMISATION INTELLIGENT",
            font=("Segoe UI", 10, "bold"),
            text_color="#6ee7b7",
        ).pack(padx=16, pady=6)

        ctk.CTkLabel(
            content,
            text="Optimisez votre irrigation",
            font=("Segoe UI", 34, "bold"),
            text_color="white",
        ).pack(anchor="w", pady=(22, 0))

        ctk.CTkLabel(
            content,
            text="en 4 etapes simples",
            font=("Segoe UI", 34, "bold"),
            text_color="#a7f3d0",
        ).pack(anchor="w")

        ctk.CTkLabel(
            content,
            text="De la saisie de vos parcelles a la validation mathematique,\n"
                 "NeoFarm guide chaque etape avec precision et transparence.",
            font=("Segoe UI", 14),
            text_color="#b7e4c7",
            wraplength=600, justify="left",
        ).pack(anchor="w", pady=(12, 0))

        stats = ctk.CTkFrame(content, fg_color="transparent")
        stats.pack(anchor="w", pady=(28, 0))

        for val, lbl in [("Dual Simplexe", "Algorithme"), ("Methode graphique", "Resolution"), ("100%", "Validation")]:
            card = ctk.CTkFrame(
                stats, fg_color="#0f5238", corner_radius=12,
                width=150, height=70
            )
            card.pack(side="left", padx=(0, 12))
            card.pack_propagate(False)

            ctk.CTkLabel(
                card, text=val,
                font=("Segoe UI", 13, "bold"), text_color="white"
            ).place(relx=0.5, rely=0.35, anchor="center")
            ctk.CTkLabel(
                card, text=lbl,
                font=("Segoe UI", 10), text_color="#a7f3d0"
            ).place(relx=0.5, rely=0.72, anchor="center")

    def _build_workflow(self):
        wf_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        wf_container.pack(fill="x", pady=(35, 0))

        ctk.CTkLabel(
            wf_container,
            text="Workflow complet",
            font=("Segoe UI", 22, "bold"),
            text_color=self.COLORS["vert_fonce"]
        ).pack(anchor="w", pady=(0, 20))

        wf_row = ctk.CTkFrame(wf_container, fg_color="transparent")
        wf_row.pack(fill="x")

        steps = [
            ("1", "Saisie", "Nombre de parcelles", "#389F3F"),
            ("2", "Configuration", "Donnees par parcelle", "#2e7d32"),
            ("3", "Resolution", "Simplexe ou Graphique", "#1e6c20"),
            ("4", "Validation", "Verification Solver", "#1d521f"),
        ]

        for i, (num, title, desc, color) in enumerate(steps):
            card = ctk.CTkFrame(
                wf_row, fg_color="white",
                corner_radius=16, border_width=1,
                border_color=self.COLORS["bordure_grise"]
            )
            card.pack(
                side="left", expand=True, fill="both",
                padx=(0 if i == 0 else 10, 10 if i < 3 else 0)
            )

            glow = ctk.CTkFrame(card, fg_color=color, corner_radius=16, height=3)
            glow.pack(fill="x")

            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=16, pady=18)

            num_bg = ctk.CTkFrame(
                inner, fg_color=color,
                corner_radius=10, width=32, height=32
            )
            num_bg.pack(pady=(2, 10))
            num_bg.pack_propagate(False)
            ctk.CTkLabel(
                num_bg, text=num,
                font=("Segoe UI", 13, "bold"), text_color="white"
            ).place(relx=0.5, rely=0.5, anchor="center")

            icon_circle = ctk.CTkFrame(
                inner, fg_color=self.COLORS["vert_tres_pale"],
                corner_radius=20, width=40, height=40
            )
            icon_circle.pack(pady=(0, 8))
            icon_circle.pack_propagate(False)
            ctk.CTkLabel(
                icon_circle, text="◆",
                font=("Segoe UI", 16), text_color=color
            ).place(relx=0.5, rely=0.5, anchor="center")

            ctk.CTkLabel(
                inner, text=title,
                font=("Segoe UI", 14, "bold"),
                text_color=self.COLORS["text_principal"]
            ).pack()
            ctk.CTkLabel(
                inner, text=desc,
                font=("Segoe UI", 11),
                text_color=self.COLORS["text_tertiaire"]
            ).pack(pady=(4, 0))

    def _build_details(self):
        details = ctk.CTkFrame(self.main_container, fg_color="transparent")
        details.pack(fill="x", pady=(35, 0))

        ctk.CTkLabel(
            details,
            text="Details du processus",
            font=("Segoe UI", 22, "bold"),
            text_color=self.COLORS["vert_fonce"]
        ).pack(anchor="w", pady=(0, 20))

        detail_steps = [
            (
                "01", "Saisie du nombre de parcelles",
                "L'utilisateur entre le nombre de parcelles a optimiser. Le systeme genere automatiquement les champs de configuration pour chaque parcelle.",
                "#1b5e20", "#E8F5E9", "Automatique"
            ),
            (
                "02", "Configuration des parcelles",
                "Pour chaque parcelle, renseignez les parametres agronomiques essentiels : taux de perte, besoins hydriques (croissance & production), et volume minimal.",
                "#2e7d32", "#E8F5E9", "4 parametres"
            ),
            (
                "03", "Resolution par optimisation",
                "L'algorithme calcule la repartition optimale de l'eau. Deux methodes sont disponibles : Graphique (2D) et Dual Simplexe (programmation lineaire).",
                "#4caf50", "#E8F5E9", "2 methodes"
            ),
            (
                "04", "Validation avec Solver",
                "La solution est verifiee par un solver independant qui confirme l'optimalite. Un rapport complet est genere avec les volumes d'eau alloues par parcelle.",
                "#81c784", "#E8F5E9", "100% fiable"
            ),
        ]

        for num, title, desc, color, bg, badge in detail_steps:
            card = ctk.CTkFrame(
                details, fg_color="white",
                corner_radius=16, border_width=1,
                border_color=self.COLORS["bordure_grise"]
            )
            card.pack(fill="x", pady=8)

            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=24, pady=(18, 8))

            left_header = ctk.CTkFrame(header, fg_color="transparent")
            left_header.pack(side="left")

            num_circle = ctk.CTkFrame(
                left_header, fg_color=color,
                corner_radius=12, width=28, height=28
            )
            num_circle.pack(side="left", padx=(0, 12))
            num_circle.pack_propagate(False)
            ctk.CTkLabel(
                num_circle, text=num,
                font=("Segoe UI", 11, "bold"), text_color="white"
            ).place(relx=0.5, rely=0.5, anchor="center")

            ctk.CTkLabel(
                left_header, text=title,
                font=("Segoe UI", 16, "bold"),
                text_color=self.COLORS["text_principal"]
            ).pack(side="left")

            ctk.CTkLabel(
                header, text=badge,
                font=("Segoe UI", 10, "bold"),
                text_color=color, fg_color=bg,
                corner_radius=6, padx=10, pady=3
            ).pack(side="right")

            ctk.CTkLabel(
                card, text=desc,
                font=("Segoe UI", 12),
                text_color=self.COLORS["text_secondaire"],
                wraplength=700, justify="left"
            ).pack(anchor="w", padx=24, pady=(0, 18))

    def _build_methods(self):
        methods = ctk.CTkFrame(self.main_container, fg_color="transparent")
        methods.pack(fill="x", pady=(35, 0))

        ctk.CTkLabel(
            methods,
            text="Methodes de resolution",
            font=("Segoe UI", 22, "bold"),
            text_color=self.COLORS["vert_fonce"]
        ).pack(anchor="w", pady=(0, 20))

        grid = ctk.CTkFrame(methods, fg_color="transparent")
        grid.pack(fill="x")
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)

        card1 = ctk.CTkFrame(
            grid, fg_color="white",
            corner_radius=16, border_width=1,
            border_color=self.COLORS["bordure_grise"]
        )
        card1.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        h1 = ctk.CTkFrame(card1, fg_color="#2e7d32", corner_radius=0, height=55)
        h1.pack(fill="x")
        h1.pack_propagate(False)
        h1.configure(corner_radius=16)

        ctk.CTkLabel(
            h1, text="Methode Graphique",
            font=("Segoe UI", 15, "bold"), text_color="white"
        ).pack(side="left", padx=22, pady=14)

        ctk.CTkLabel(
            h1, text="2D",
            font=("Segoe UI", 10, "bold"), text_color="#2e7d32",
            fg_color="white", corner_radius=8,
            padx=10, pady=3
        ).pack(side="right", padx=22)

        c1 = ctk.CTkFrame(card1, fg_color="transparent")
        c1.pack(fill="x", padx=22, pady=18)

        ctk.CTkLabel(
            c1,
            text="Visualisation 2D de la region realisable et recherche du point optimal a l'intersection des contraintes. Ideal pour 2 variables.",
            font=("Segoe UI", 12), text_color=self.COLORS["text_secondaire"],
            wraplength=340, justify="left"
        ).pack(anchor="w")

        ctk.CTkLabel(
            c1, text="Avantages",
            font=("Segoe UI", 12, "bold"), text_color=self.COLORS["success"]
        ).pack(anchor="w", pady=(14, 4))
        for p in ["Visual intuitif", "Comprehension geometrique", "Rapide pour 2D"]:
            row = ctk.CTkFrame(c1, fg_color="transparent")
            row.pack(fill="x", pady=1)
            ctk.CTkLabel(
                row, text="●",
                font=("Segoe UI", 8), text_color=self.COLORS["success"], width=16
            ).pack(side="left")
            ctk.CTkLabel(
                row, text=p,
                font=("Segoe UI", 11), text_color=self.COLORS["text_secondaire"]
            ).pack(side="left")

        ctk.CTkLabel(
            c1, text="Limites",
            font=("Segoe UI", 12, "bold"), text_color=self.COLORS["danger"]
        ).pack(anchor="w", pady=(12, 4))
        for p in ["Limite a 2 variables", "Moins precis", "Difficile a l'echelle"]:
            row = ctk.CTkFrame(c1, fg_color="transparent")
            row.pack(fill="x", pady=1)
            ctk.CTkLabel(
                row, text="●",
                font=("Segoe UI", 8), text_color=self.COLORS["danger"], width=16
            ).pack(side="left")
            ctk.CTkLabel(
                row, text=p,
                font=("Segoe UI", 11), text_color=self.COLORS["text_secondaire"]
            ).pack(side="left")

        card2 = ctk.CTkFrame(
            grid, fg_color="white",
            corner_radius=16, border_width=1,
            border_color=self.COLORS["bordure_grise"]
        )
        card2.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        h2 = ctk.CTkFrame(card2, fg_color=self.COLORS["vert_clair"], corner_radius=0, height=55)
        h2.pack(fill="x")
        h2.pack_propagate(False)
        h2.configure(corner_radius=16)

        ctk.CTkLabel(
            h2, text="Dual Simplexe",
            font=("Segoe UI", 15, "bold"), text_color="white"
        ).pack(side="left", padx=22, pady=14)

        ctk.CTkLabel(
            h2, text="N-D",
            font=("Segoe UI", 10, "bold"), text_color=self.COLORS["vert_clair"],
            fg_color="white", corner_radius=8,
            padx=10, pady=3
        ).pack(side="right", padx=22)

        c2 = ctk.CTkFrame(card2, fg_color="transparent")
        c2.pack(fill="x", padx=22, pady=18)

        ctk.CTkLabel(
            c2,
            text="Algorithme de programmation lineaire qui minimise la fonction objectif en respectant toutes les contraintes. Optimal pour N parcelles.",
            font=("Segoe UI", 12), text_color=self.COLORS["text_secondaire"],
            wraplength=340, justify="left"
        ).pack(anchor="w")

        ctk.CTkLabel(
            c2, text="Avantages",
            font=("Segoe UI", 12, "bold"), text_color=self.COLORS["success"]
        ).pack(anchor="w", pady=(14, 4))
        for p in ["N variables illimite", "Solution exacte", "Tres rapide"]:
            row = ctk.CTkFrame(c2, fg_color="transparent")
            row.pack(fill="x", pady=1)
            ctk.CTkLabel(
                row, text="●",
                font=("Segoe UI", 8), text_color=self.COLORS["success"], width=16
            ).pack(side="left")
            ctk.CTkLabel(
                row, text=p,
                font=("Segoe UI", 11), text_color=self.COLORS["text_secondaire"]
            ).pack(side="left")

        ctk.CTkLabel(
            c2, text="Limites",
            font=("Segoe UI", 12, "bold"), text_color=self.COLORS["danger"]
        ).pack(anchor="w", pady=(12, 4))
        for p in ["Abstraction mathematique", "Necessite un solver", "Moins visuel"]:
            row = ctk.CTkFrame(c2, fg_color="transparent")
            row.pack(fill="x", pady=1)
            ctk.CTkLabel(
                row, text="●",
                font=("Segoe UI", 8), text_color=self.COLORS["danger"], width=16
            ).pack(side="left")
            ctk.CTkLabel(
                row, text=p,
                font=("Segoe UI", 11), text_color=self.COLORS["text_secondaire"]
            ).pack(side="left")

    def _build_validation(self):
        val = ctk.CTkFrame(self.main_container, fg_color="transparent")
        val.pack(fill="x", pady=(35, 0))

        ctk.CTkLabel(
            val,
            text="Validation & Verification",
            font=("Segoe UI", 22, "bold"),
            text_color=self.COLORS["vert_fonce"]
        ).pack(anchor="w", pady=(0, 20))

        vcard = ctk.CTkFrame(
            val, fg_color="white",
            corner_radius=16, border_width=1,
            border_color=self.COLORS["bordure_grise"]
        )
        vcard.pack(fill="x")

        vheader = ctk.CTkFrame(vcard, fg_color=self.COLORS["vert_fonce"], corner_radius=0, height=50)
        vheader.pack(fill="x")
        vheader.pack_propagate(False)
        vheader.configure(corner_radius=16)

        vh = ctk.CTkFrame(vheader, fg_color="transparent")
        vh.pack(fill="x", padx=24, pady=12)

        ctk.CTkLabel(
            vh,
            text="SOLUTION VALIDEE PAR SOLVER",
            font=("Segoe UI", 13, "bold"),
            text_color="white"
        ).pack(side="left")

        ctk.CTkLabel(
            vh,
            text="Verification independante",
            font=("Segoe UI", 11),
            text_color="#a7f3d0"
        ).pack(side="right")

        vcontent = ctk.CTkFrame(vcard, fg_color="transparent")
        vcontent.pack(fill="x", padx=24, pady=24)

        checks = ctk.CTkFrame(vcontent, fg_color="transparent")
        checks.pack(fill="x")

        validations = [
            ("Fonction objectif", "Minimisee", "Valeur optimale atteinte", "#1b5e20"),
            ("Contraintes", "Respectees", "Toutes les contraintes satisfaites", "#2e7d32"),
            ("Volumes min.", "Verifies", "Seuils minimaux respectes", "#4caf50"),
            ("Optimalite", "Confirmee", "Solution prouvee optimale", "#81c784"),
        ]

        for i, (label, status, detail, color) in enumerate(validations):
            col = i % 2
            row = i // 2

            vc = ctk.CTkFrame(
                checks, fg_color=self.COLORS["vert_tres_pale"],
                corner_radius=12
            )
            vc.grid(
                row=row, column=col, sticky="nsew",
                padx=(0 if col == 0 else 8, 8 if col == 0 else 0),
                pady=(0 if row == 0 else 8, 8)
            )

            inner = ctk.CTkFrame(vc, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=16, pady=14)

            top = ctk.CTkFrame(inner, fg_color="transparent")
            top.pack(fill="x")

            ctk.CTkLabel(
                top, text=label,
                font=("Segoe UI", 12, "bold"),
                text_color=self.COLORS["text_principal"]
            ).pack(side="left")

            ctk.CTkLabel(
                top, text=status,
                font=("Segoe UI", 10, "bold"),
                text_color=color
            ).pack(side="right")

            ctk.CTkLabel(
                inner, text=detail,
                font=("Segoe UI", 10),
                text_color=self.COLORS["text_tertiaire"]
            ).pack(anchor="w", pady=(4, 0))

        checks.grid_columnconfigure(0, weight=1)
        checks.grid_columnconfigure(1, weight=1)

    def _build_cta(self):
        cta = ctk.CTkFrame(
            self.main_container, fg_color=self.COLORS["vert_fonce"],
            corner_radius=20
        )
        cta.pack(fill="x", pady=(35, 30))

        cta_content = ctk.CTkFrame(cta, fg_color="transparent")
        cta_content.pack(fill="x", padx=40, pady=32)

        ctk.CTkLabel(
            cta_content,
            text="Pret a optimiser votre irrigation ?",
            font=("Segoe UI", 26, "bold"),
            text_color="white"
        ).pack(anchor="w")

        ctk.CTkLabel(
            cta_content,
            text="Lancez votre premiere optimisation et decouvrez les economies d'eau "
                 "que NeoFarm peut generer pour votre exploitation.",
            font=("Segoe UI", 13),
            text_color="#b7e4c7",
            wraplength=600, justify="left"
        ).pack(anchor="w", pady=(8, 20))

        bf = ctk.CTkFrame(cta_content, fg_color="transparent")
        bf.pack(anchor="w")

        ctk.CTkButton(
            bf,
            text="Retour a l'accueil",
            fg_color="transparent",
            hover_color="#0f5238",
            text_color="white",
            font=("Segoe UI", 12),
            border_width=0.5,
            border_color="#b7e4c7",
            width=180, height=40,
            corner_radius=10,
            command=lambda: self.controller.show_page("home")
        ).pack(side="left", padx=(0, 12))

        ctk.CTkButton(
            bf,
            text="Demarrer l'optimisation",
            fg_color=self.COLORS["vert_clair"],
            hover_color=self.COLORS["vert_hover"],
            text_color="white",
            font=("Segoe UI", 13, "bold"),
            width=220, height=40,
            corner_radius=10,
            command=lambda: self.controller.show_page("parcelles")
        ).pack(side="left")

    def _build_footer(self):
        footer = ctk.CTkFrame(
            self, fg_color="#0a3d2a",
            corner_radius=0, height=40
        )
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        ctk.CTkLabel(
            footer,
            text="NeoFarm © 2026 — Irrigation intelligente",
            font=("Segoe UI", 11),
            text_color="#b7e4c7",
        ).pack(expand=True)