import customtkinter as ctk
from controller.controller import MainController
from .parcelle import ParcellePage
from .parcel_details import ParcelDetailsPage
from .recap_page import RecapPage
from .dashboard import DashboardPage
from .savoirplus import SavoirPlusPage
from .solution_page import SolutionPage
from model.dual_simplexe import DualSimplexePage
from model.validationSolveur import ValidationSolveurPage

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


class HomePage(ctk.CTkFrame):
    """
    Page d'accueil principale de l'application NeoFarm.
    Présente l'interface de démarrage avec message d'accueil.
    """
    def __init__(self, parent, controller):
        """
        Initialise la page d'accueil.
        
        Args:
            parent: Widget parent
            controller: Contrôleur de l'application
        """
        super().__init__(parent, fg_color="#F5FBF8")
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        """
        Construit l'interface utilisateur de la page d'accueil.
        """

        self.top_bar = ctk.CTkFrame(
            self,
            fg_color="#0a3d2a",
            corner_radius=0,
            height=40
        )
        self.top_bar.pack(fill="x", side="top")
        self.top_bar.pack_propagate(False)

        self.announcement_label = ctk.CTkLabel(
            self.top_bar,
            text="Optimisation intelligente de l'irrigation pour une agriculture durable",
            font=("Segoe UI", 14, "italic"),
            text_color="white"
        )
        self.announcement_label.pack(expand=True)

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=60, pady=40)

        content = ctk.CTkFrame(self.main_container, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")

        badge = ctk.CTkFrame(content, fg_color="#E8F5E9", corner_radius=20)
        badge.pack(pady=(0, 20))
        badge.bind("<Enter>", lambda e: badge.configure(fg_color="#C8E6C9"))
        badge.bind("<Leave>", lambda e: badge.configure(fg_color="#E8F5E9"))

        ctk.CTkLabel(
            badge,
            text="Bienvenue sur NeoFarm",
            font=("Segoe UI", 17, "bold"),
            text_color="#2e7d32",
        ).pack(padx=16, pady=5)

        title_label = ctk.CTkLabel(
            content,
            text="Irrigation de Précision et Gestion Intelligente de l'Eau",
            font=("Segoe UI", 28, "bold"),
            text_color="#0a3d2a",
            justify="center",
            wraplength=700,
        )
        title_label.pack(pady=(0, 15))

        sep = ctk.CTkFrame(content, fg_color="#C8E6C9", height=2, width=120)
        sep.pack(pady=(0, 15))

        ctk.CTkLabel(
            content,
            text="Optimisez vos cultures grâce à des solutions intelligentes d'irrigation,\n"
                 "conçues pour améliorer vos rendements tout en économisant l'eau.",
            font=("Segoe UI", 15),
            text_color="#555555",
            justify="center",
        ).pack(pady=(0, 25))

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=(5, 0))

        btn_secondary = ctk.CTkButton(
            btn_frame,
            text="En savoir plus",
            fg_color="transparent",
            hover_color="#E8F5E9",
            height=40,
            width=150,
            corner_radius=12,
            font=("Segoe UI", 12),
            text_color="#0a3d2a",
            border_width=2,
            border_color="#0a3d2a",
            command=lambda: self.controller.show_page("savoir_plus"),
        )
        btn_secondary.pack(side="left", padx=(0, 12))
        btn_secondary.bind("<Enter>", lambda e: btn_secondary.configure(text_color="#1b5e20", border_color="#1b5e20"))
        btn_secondary.bind("<Leave>", lambda e: btn_secondary.configure(text_color="#0a3d2a", border_color="#0a3d2a"))

        btn_primary = ctk.CTkButton(
            btn_frame,
            text="DÉMARRER",
            fg_color="#2e7d32",
            hover_color="#1b5e20",
            height=40,
            width=160,
            corner_radius=12,
            font=("Segoe UI", 12, "bold"),
            command=lambda: self.controller.show_page("parcelles"),
        )
        btn_primary.pack(side="left")

        footer = ctk.CTkFrame(self, fg_color="#0a3d2a", corner_radius=0, height=40)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        ctk.CTkLabel(
            footer,
            text="NeoFarm © 2026 — Irrigation intelligente",
            font=("Segoe UI", 11),
            text_color="#b7e4c7",
        ).pack(expand=True)


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NeoFarm - Solutions d'Irrigation Intelligente")
        self.geometry("1200x720")
        self.configure(fg_color="#FFFFFF")
        self.update_idletasks()
        width = 1200
        height = 720
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

        self.controller = MainController(self)

        self.home_page = HomePage(self, self.controller)
        self.controller.add_page("home", self.home_page)

        self.parcelle_page = ParcellePage(self, self.controller)
        self.controller.add_page("parcelles", self.parcelle_page)

        self.parcel_details_page = ParcelDetailsPage(self, self.controller)
        self.controller.add_page("parcel_details", self.parcel_details_page)

        self.recap_page = RecapPage(self, self.controller)
        self.controller.add_page("recap", self.recap_page)

        self.dashboard_page = DashboardPage(self, self.controller)
        self.controller.add_page("dashboard", self.dashboard_page)

        self.savoir_plus_page = SavoirPlusPage(self, self.controller)
        self.controller.add_page("savoir_plus", self.savoir_plus_page)

        self.solution_page = SolutionPage(self, self.controller)
        self.controller.add_page("solution", self.solution_page)

        self.dual_simplexe_page = DualSimplexePage(self, self.controller)
        self.controller.add_page("dual_simplexe", self.dual_simplexe_page)

        self.validation_solveur_page = ValidationSolveurPage(self, self.controller)
        self.controller.add_page("validation_solveur", self.validation_solveur_page)

        self.controller.show_page("home")
