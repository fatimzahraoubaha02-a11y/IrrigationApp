import customtkinter as ctk
from typing import Dict, List
import tkinter as tk
from tkinter import messagebox


class MainController:
    """
    Contrôleur principal de l'application NeoFarm.
    Gère la navigation entre les pages et le partage des données.
    """
    def __init__(self, parent):
        """
        Initialise le contrôleur principal.
        
        Args:
            parent: Widget parent de l'application
        """
        self.parent = parent
        self._parcels: List[dict] = []
        self._parcel_count = 0
        self.pages: Dict[str, ctk.CTkFrame] = {}
        self._completed_steps = set()
        self._current_step = None
        self._last_resolution_results = {}
        self._last_solver_results = {}
        self._global_model = {}

    def add_page(self, name: str, page: ctk.CTkFrame):
        """
        Ajoute une page au contrôleur.
        
        Args:
            name: Nom unique de la page
            page: Widget de la page
        """
        self.pages[name] = page
        page.pack(fill="both", expand=True)

    def show_page(self, name: str):
        """
        Affiche une page spécifique et cache les autres.
        Vérifie les droits d'accès avant l'affichage.
        
        Args:
            name: Nom de la page à afficher
            
        Returns:
            True si la page a été affichée, False sinon
        """
        if name == "solution" and not self._can_access_solution():
            self._show_access_denied_message("solution")
            return False
        elif name == "graphique" and not self._can_access_graphique():
            self._show_access_denied_message("graphique")
            return False
        elif name == "dual_simplexe" and not self._can_access_dual_simplexe():
            self._show_access_denied_message("dual_simplexe")
            return False
        elif name == "validation_solveur" and not self._can_access_validation_solveur():
            self._show_access_denied_message("validation_solveur")
            return False
        
        for page_name, page in self.pages.items():
            if page_name == name:
                page.pack(fill="both", expand=True)
                self._current_step = name
                
                if page_name == "parcelles" and hasattr(page, 'refresh_data'):
                    page.refresh_data()
                    self._completed_steps.add("parcelle")
                elif page_name == "parcel_details" and hasattr(page, 'refresh_data'):
                    page.refresh_data()
                    self._completed_steps.add("parcel_details")
                elif page_name == "recap" and hasattr(page, 'refresh_data'):
                    page.refresh_data()
                    self._completed_steps.add("recap")
                elif page_name == "solution" and hasattr(page, 'refresh_data'):
                    page.refresh_data()
                    self._completed_steps.add("solution")
                elif page_name == "graphique":
                    if hasattr(page, 'solve_and_display'):
                        page.solve_and_display()
                    self._completed_steps.add("graphique")
                elif page_name == "dual_simplexe":
                    if hasattr(page, 'refresh_data'):
                        page.refresh_data()
                    self._completed_steps.add("dual_simplexe")
                elif page_name == "validation_solveur":
                    if hasattr(page, 'refresh_data'):
                        page.refresh_data()
                    self._completed_steps.add("validation_solveur")
                elif page_name == "dashboard":
                    if hasattr(page, 'refresh_data'):
                        page.refresh_data()
                    self._completed_steps.add("dashboard")
            else:
                page.pack_forget()
        return True

    def get_parcel_count(self) -> int:
        return self._parcel_count

    def set_parcel_count(self, count: int):
        self._parcel_count = count

    def get_parcels(self) -> List[dict]:
        return self._parcels

    def get_parcels_model(self) -> List[dict]:
        """Alias pour get_parcels pour compatibilité avec les pages UI."""
        return self.get_parcels()

    def set_parcels(self, parcels: List[dict]):
        self._parcels = parcels

    def set_global_model(self, data: dict):
        self._global_model = data

    def get_global_model(self) -> dict:
        return getattr(self, '_global_model', {})

    def load_demo_parcels(self, n_parcels: int):
        self._parcel_count = n_parcels
        demo_data = []
        for i in range(n_parcels):
            demo_data.append({
                "id": i,
                "taux_perte": 5.0 + i * 0.5,
                "coeff_croissance": 1.2,
                "coeff_production": 1.5,
                "vol_min": 100 + i * 20
            })
        self._parcels = demo_data

    def show_lp_modal(self, parent=None):
        return self.show_page("solution")
    
    def _can_access_solution(self) -> bool:
        
        if not self._parcels or len(self._parcels) == 0:
            return False
        
        if not hasattr(self, '_global_model') or not self._global_model:
            return False
        
        return True
    
    def _can_access_graphique(self) -> bool:
        required_steps = ["parcelle", "parcel_details", "recap", "solution"]
        
        for step in required_steps:
            if step not in self._completed_steps:
                return False
        
        return True
    
    def _can_access_dual_simplexe(self) -> bool:
        required_steps = ["parcelle", "parcel_details", "recap", "solution"]
        
        for step in required_steps:
            if step not in self._completed_steps:
                return False
        
        return True
    
    def _can_access_validation_solveur(self) -> bool:
        required_steps = ["parcelle", "parcel_details", "recap"]
        
        for step in required_steps:
            if step not in self._completed_steps:
                return False
        
        return True
    
    def get_completed_steps(self) -> set:
        return self._completed_steps.copy()
    
    def reset_progress(self):
        self._completed_steps.clear()
        self._current_step = None
    
    def is_step_completed(self, step: str) -> bool:
        return step in self._completed_steps
    
    def get_required_steps_for_page(self, page: str) -> List[str]:
        requirements = {
            "solution": ["parcelle", "parcel_details", "recap"],
            "graphique": ["parcelle", "parcel_details", "recap", "solution"],
            "dual_simplexe": ["parcelle", "parcel_details", "recap", "solution"],
            "validation_solveur": ["parcelle", "parcel_details", "recap"]
        }
        return requirements.get(page, [])
    
    def get_missing_steps_for_page(self, page: str) -> List[str]:
        required = self.get_required_steps_for_page(page)
        return [step for step in required if step not in self._completed_steps]
    
    def set_resolution_results(self, results: List[float], method: str = None):
        """Stocke les résultats de résolution."""
        self._last_resolution_results = {i: val for i, val in enumerate(results)}
        
        if method == "graphique":
            self._completed_steps.add("graphique")
        elif method == "dual_simplexe":
            self._completed_steps.add("dual_simplexe")
        elif method == "solveur_excel":
            self._completed_steps.add("solveur_excel")
    
    def set_solver_results(self, results: List[float]):
        """Stocke les résultats du solveur."""
        self._last_solver_results = {i: val for i, val in enumerate(results)}
    
    def get_resolution_results(self) -> Dict[int, float]:
        """Retourne les derniers résultats de résolution."""
        return self._last_resolution_results
    
    def get_solver_results(self) -> Dict[int, float]:
        """Retourne les derniers résultats du solveur."""
        return self._last_solver_results
    
    def log_message(self, message: str):
        """Enregistre un message de log."""
        print(f"LOG: {message}")
    
    def get_global_model(self):
        """Retourne les données du modèle global."""
        user_global_model = getattr(self, '_global_model', {})
        if user_global_model:
            return user_global_model
        
        parcels = self.get_parcels()
        if not parcels:
            return {}
        
        besoin_total_croissance = sum(p.get('vol_min', 0) * p.get('coeff_croissance', 1) for p in parcels)
        besoin_total_production = sum(p.get('vol_min', 0) * p.get('coeff_production', 1) for p in parcels)
        
        return {
            'besoin_total_croissance': besoin_total_croissance,
            'besoin_total_production': besoin_total_production
        }
    
    def _show_access_denied_message(self, page: str):
        missing_steps = self.get_missing_steps_for_page(page)
        
        step_names = {
            "parcelle": "Nombre de parcelles",
            "parcel_details": "Détails des parcelles",
            "recap": "Récapitulatif",
            "solution": "Solution",
            "graphique": "Graphique",
            "dual_simplexe": "Dual Simplexe",
            "validation_solveur": "Validation Solveur"
        }
        
        page_names = {
            "solution": "Solution",
            "graphique": "Graphique",
            "dual_simplexe": "Dual Simplexe",
            "validation_solveur": "Validation Solveur"
        }
        
        missing_names = [step_names.get(step, step) for step in missing_steps]
        
        message = f"Veuillez compléter les étapes suivantes avant d'accéder à {page_names.get(page, page)}:\n\n"
        message += "\n".join(f"• {name}" for name in missing_names)
        message += "\n\nFlux complet requis:\n"
        message += "parcelle.py → parcel_details.py → recap_page.py → solution_page.py"
        message += "\n→ graphique.py ou dual_simplexe.py → validationSolveur.py"
        
        messagebox.showwarning("Accès refusé", message)
