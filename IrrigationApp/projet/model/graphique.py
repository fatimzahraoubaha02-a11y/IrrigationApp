
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Any
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
from matplotlib.widgets import Button


def afficher_graphique(parcels: List[Dict[str, Any]], global_data: Dict[str, float], controller=None) -> Optional[Dict]:
    """
    Affiche la méthode graphique pour résoudre le problème d'irrigation.
    
    Args:
        parcels: Liste des parcelles avec leurs paramètres
        global_data: Données globales (besoins en eau, etc.)
        controller: Contrôleur pour la navigation (optionnel)
    
    Returns:
        Dict avec 'solution', 'cout', 'details' ou None si infaisable
    """
    n = len(parcels)

    if n == 0:
        print("Aucune parcelle définie")
        return None

    result = _resoudre_linprog(parcels, global_data)

    if n == 2:
        return _afficher_graphique_2d(parcels, global_data, result, controller)
    else:
        return _afficher_graphique_nd(parcels, global_data, result, controller)


def _on_valider_clicked(controller, result=None):
    """
    Gère le clic sur le bouton Valider - sauvegarde les résultats et navigue vers la page de validation.
    
    Args:
        controller: Contrôleur pour la navigation
        result: Résultat de la résolution à sauvegarder
    """
    print("=== VALIDER BUTTON CLICKED ===")
    plt.close('all')
    
    if controller is None:
        print("No controller available")
        return
        
    if result is None:
        print("No result available - cannot validate")
        return
    
    solution = result.get('solution', [])
    if solution:
        print(f"Sauvegarde des résultats de résolution graphique: {solution}")
        controller.set_resolution_results(solution, method="graphique")
        
        controller.show_page("validation_solveur")
    else:
        print("No solution found in result")
def _on_retour_clicked(controller):
    """
    Gère le clic sur le bouton Retour - ferme le graphique et retourne à la page précédente.
    
    Args:
        controller: Contrôleur pour la navigation
    """
    print("=== RETOUR BUTTON CLICKED ===")
    plt.close('all')
    
    if controller:
        controller.show_page("solution")
    else:
        print("No controller available - just closing graph")


def _resoudre_linprog(parcels: List[Dict], global_data: Dict) -> Optional[Dict]:
    """
    Résout le problème d'irrigation avec scipy.optimize.linprog.
    
    Args:
        parcels: Liste des parcelles
        global_data: Données globales
    
    Returns:
        Dict avec 'solution', 'cout', 'success' ou None
    """
    try:
        n = len(parcels)

        c = np.array([p.get('taux_perte', 0) / 100 for p in parcels])

        A_ub = []
        b_ub = []

        besoin_croissance = global_data.get('besoin_total_croissance', 0)
        if besoin_croissance > 0:
            row = [-p.get('coeff_croissance', 1) for p in parcels]
            A_ub.append(row)
            b_ub.append(-besoin_croissance)

        besoin_production = global_data.get('besoin_total_production', 0)
        if besoin_production > 0:
            row = [-p.get('coeff_production', 1) for p in parcels]
            A_ub.append(row)
            b_ub.append(-besoin_production)

        if A_ub:
            A_ub = np.array(A_ub)
            b_ub = np.array(b_ub)
        else:
            A_ub = None
            b_ub = None

        bounds = [(p.get('vol_min', 0) if p.get('vol_min', 0) > 0 else 0, None) for p in parcels]

        from scipy.optimize import linprog
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

        if result.success:
            return {
                'solution': result.x.tolist(),
                'cout': result.fun,
                'success': True,
                'method': 'scipy_highs'
            }
        else:
            return {
                'solution': None,
                'cout': None,
                'success': False,
                'message': 'Problème infaisable'
            }

    except ImportError:
        return _resoudre_manual(parcels, global_data)
    except Exception as e:
        return {
            'solution': None,
            'cout': None,
            'success': False,
            'message': str(e)
        }


def _resoudre_manual(parcels: List[Dict], global_data: Dict) -> Optional[Dict]:
    n = len(parcels)
    if n == 0:
        return None

    besoin_croissance = global_data.get('besoin_total_croissance', 0)
    besoin_production = global_data.get('besoin_total_production', 0)

    total_coeff_croissance = sum(p.get('coeff_croissance', 1) for p in parcels)
    total_coeff_production = sum(p.get('coeff_production', 1) for p in parcels)

    solution = []
    total_cout = 0

    for i, parcel in enumerate(parcels):
        vol_c = (besoin_croissance * parcel.get('coeff_croissance', 1) / total_coeff_croissance) if total_coeff_croissance > 0 else 0
        vol_p = (besoin_production * parcel.get('coeff_production', 1) / total_coeff_production) if total_coeff_production > 0 else 0

        vol = max(parcel.get('vol_min', 0), vol_c + vol_p)
        solution.append(vol)

        taux_perte = parcel.get('taux_perte', 0)
        total_cout += vol * (taux_perte / 100)

    return {
        'solution': solution,
        'cout': total_cout,
        'success': True,
        'method': 'manual'
    }


def _afficher_graphique_2d(parcels: List[Dict], global_data: Dict, result: Dict, controller=None) -> Dict:
    COLORS = {
        "primary": "#0a3d2a",
        "primary_light": "#1a5c40",
        "hover": "#2e7d32",
        "bg": "#F5F7F6",
        "accent": "#f39c12",
    }

    besoin_croissance = global_data.get('besoin_total_croissance', 0)
    besoin_production = global_data.get('besoin_total_production', 0)

    coeff_croissance = [p.get('coeff_croissance', 1) for p in parcels]
    coeff_production = [p.get('coeff_production', 1) for p in parcels]
    vol_min = [p.get('vol_min', 0) for p in parcels]

    fig = plt.figure(figsize=(14, 10))

    ax = fig.add_subplot(111)
    ax.set_position([0.08, 0.18, 0.84, 0.72])

    ax_btn_bg = fig.add_axes([0.0, 0.0, 1.0, 0.12])
    ax_btn_bg.set_facecolor(COLORS["bg"])
    ax_btn_bg.set_xlim(0, 1)
    ax_btn_bg.set_ylim(0, 1)
    ax_btn_bg.axis('off')

    ax_retour = fig.add_axes([0.08, 0.035, 0.10, 0.05])
    btn_retour = Button(
        ax_retour, 
        'Retour',
        color=COLORS["bg"],
        hovercolor='#E8F5E9'
    )
    btn_retour.label.set_fontsize(11)
    btn_retour.label.set_fontweight('bold')
    btn_retour.label.set_color(COLORS["primary"])
    for spine in ax_retour.spines.values():
        spine.set_color(COLORS["primary"])
        spine.set_linewidth(1)
    ax_retour.set_facecolor('white')
    btn_retour.on_clicked(lambda x: _on_retour_clicked(controller))

    ax_valider = fig.add_axes([0.82, 0.035, 0.10, 0.05])
    btn_valider = Button(
        ax_valider, 
        ' Valider',
        color=COLORS["primary_light"],
        hovercolor=COLORS["hover"]
    )
    btn_valider.label.set_fontsize(11)
    btn_valider.label.set_fontweight('bold')
    btn_valider.label.set_color('white')
    ax_valider.set_facecolor(COLORS["primary_light"])
    for spine in ax_valider.spines.values():
        spine.set_color(COLORS["primary_light"])
        spine.set_linewidth(1)
    btn_valider.on_clicked(lambda x: _on_valider_clicked(controller, result))

    max_x = 0
    max_y = 0

    contraintes = []

    if besoin_croissance > 0 and coeff_croissance[0] > 0 and coeff_croissance[1] > 0:
        x_max = besoin_croissance / coeff_croissance[0]
        y_max = besoin_croissance / coeff_croissance[1]
        contraintes.append({
            'x intercept': x_max,
            'y intercept': y_max,
            'label': 'C1: Croissance',
            'color': '#e74c3c'
        })
        max_x = max(max_x, x_max * 1.2)
        max_y = max(max_y, y_max * 1.2)

    if besoin_production > 0 and coeff_production[0] > 0 and coeff_production[1] > 0:
        x_max = besoin_production / coeff_production[0]
        y_max = besoin_production / coeff_production[1]
        contraintes.append({
            'x intercept': x_max,
            'y intercept': y_max,
            'label': 'C2: Production',
            'color': '#3498db'
        })
        max_x = max(max_x, x_max * 1.2)
        max_y = max(max_y, y_max * 1.2)

    if vol_min[0] > 0:
        contraintes.append({
            'x intercept': vol_min[0],
            'y intercept': None,
            'label': 'C3: x1 ≥ min',
            'color': '#2ecc71'
        })
        max_x = max(max_x, vol_min[0] * 2)

    if vol_min[1] > 0:
        contraintes.append({
            'x intercept': None,
            'y intercept': vol_min[1],
            'label': 'C4: x2 ≥ min',
            'color': '#9b59b6'
        })
        max_y = max(max_y, vol_min[1] * 2)

    if max_x == 0:
        max_x = 500
    if max_y == 0:
        max_y = 500

    x = np.linspace(0, max_x, 500)

    feasible_points = []

    for x_val in x:
        y_requirements = []

        for contrainte in contraintes:
            if contrainte['y intercept'] is not None and contrainte['x intercept'] is not None:
                y_min = contrainte['y intercept'] - (contrainte['y intercept'] / contrainte['x intercept']) * x_val
                if y_min > 0:
                    y_requirements.append(y_min)
            elif contrainte['x intercept'] is not None and contrainte['y intercept'] is None:
                if x_val < contrainte['x intercept']:
                    y_requirements.append(float('inf'))
            elif contrainte['y intercept'] is not None and contrainte['x intercept'] is None:
                y_requirements.append(contrainte['y intercept'])

        if y_requirements:
            y_feasible = max(y_requirements)
            if y_feasible < float('inf') and y_feasible >= 0 and y_feasible <= max_y:
                feasible_points.append((x_val, y_feasible))

    
    for contrainte in contraintes:
        if contrainte['y intercept'] is not None and contrainte['x intercept'] is not None:
            if contrainte['x intercept'] > 0:
                y_vals = np.maximum(0, contrainte['y intercept'] - (contrainte['y intercept'] / contrainte['x intercept']) * x)
                y_vals = np.clip(y_vals, 0, None)
                ax.plot(x, y_vals, label=contrainte['label'], color=contrainte['color'], linewidth=2)

        elif contrainte['x intercept'] is not None and contrainte['y intercept'] is None:
            ax.axvline(x=contrainte['x intercept'], label=contrainte['label'], 
                      color=contrainte['color'], linewidth=2, linestyle='--')

        elif contrainte['y intercept'] is not None and contrainte['x intercept'] is None:
            ax.axhline(y=contrainte['y intercept'], label=contrainte['label'],
                      color=contrainte['color'], linewidth=2, linestyle='--')

    if result and result.get('success') and result.get('solution'):
        opt_x1 = result['solution'][0]
        opt_x2 = result['solution'][1]
        ax.scatter(opt_x1, opt_x2, color=COLORS["accent"], s=200, zorder=5, marker='*', 
                   edgecolors='black', linewidths=1.5)
        ax.annotate(f'Optimal\n({int(opt_x1)}, {int(opt_x2)})', 
                   xy=(opt_x1, opt_x2), xytext=(opt_x1 + max_x*0.1, opt_x2 + max_y*0.1),
                   fontsize=11, fontweight='bold', color=COLORS["accent"],
                   arrowprops=dict(arrowstyle='->', color=COLORS["accent"]))

    ax.set_xlim(0, max_x)
    ax.set_ylim(0, max_y)
    ax.set_xlabel('x1: Volume Parcelle 1 (m³)')
    ax.set_ylabel('x2: Volume Parcelle 2 (m³)')
    ax.set_title("Méthode Graphique - Problème d'Irrigation")

    ax.legend(loc='upper right')

    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#f8f9fa')

    if result and result.get('success'):
        texte = f"Solution Optimale:\n"
        for i, val in enumerate(result['solution']):
            texte += f"x{i+1} = {int(val)} m³\n"
        texte += f"\nw = {int(result['cout'])}"
        ax.text(0.02, 0.98, texte, transform=ax.transAxes, fontsize=10,
               verticalalignment='top', fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    plt.show()

    return result


def _afficher_graphique_nd(parcels: List[Dict], global_data: Dict, result: Dict, controller=None) -> Dict:
    n = len(parcels)

    COLORS = {
        "primary": "#0a3d2a",
        "primary_light": "#1a5c40",
        "hover": "#2e7d32",
        "bg": "#F5F7F6",
    }

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(5, 9, 'Méthode Graphique - Résolution', fontsize=16, fontweight='bold',
            ha='center', va='top', color=COLORS["primary"])

    info_text = f"""
    Problème avec {n} variables (parcelles)

    La méthode graphique 2D ne peut pas afficher 
    {n} dimensions directement.

    Utilisation de scipy.optimize.linprog 
    (Méthode du Simplexe/Highers)
    """

    ax.text(5, 7, info_text, fontsize=12, ha='center', va='top', color='#333333')

    if result and result.get('success'):
        sol_text = "Solution Optimale:\n"
        for i, val in enumerate(result['solution']):
            sol_text += f"x{i+1} = {int(val)} m³\n"
        sol_text += f"\nw = {int(result['cout'])}\n"
        sol_text += f"Méthode: {result.get('method', 'N/A')}"

        ax.text(5, 4, sol_text, fontsize=12, ha='center', va='top', fontweight='bold',
               color='#2e7d32',
               bbox=dict(boxstyle='round', facecolor='#e8f5e9', alpha=0.9))
    else:
        ax.text(5, 4, "Problème infaisable ou erreur de calcul", 
               fontsize=12, ha='center', va='top', color='#c0392b')

    ax_retour = fig.add_axes([0.08, 0.035, 0.10, 0.05])
    btn_retour = Button(
        ax_retour, 
        'Retour',
        color=COLORS["bg"],
        hovercolor='#E8F5E9'
    )
    btn_retour.label.set_fontsize(11)
    btn_retour.label.set_fontweight('bold')
    btn_retour.label.set_color(COLORS["primary"])
    for spine in ax_retour.spines.values():
        spine.set_color(COLORS["primary"])
        spine.set_linewidth(1)
    ax_retour.set_facecolor('white')
    btn_retour.on_clicked(lambda x: _on_retour_clicked(controller))

    ax_valider = fig.add_axes([0.82, 0.035, 0.10, 0.05])
    btn_valider = Button(
        ax_valider, 
        ' Valider',
        color=COLORS["primary_light"],
        hovercolor=COLORS["hover"]
    )
    btn_valider.label.set_fontsize(11)
    btn_valider.label.set_fontweight('bold')
    btn_valider.label.set_color('white')
    ax_valider.set_facecolor(COLORS["primary_light"])
    for spine in ax_valider.spines.values():
        spine.set_color(COLORS["primary_light"])
        spine.set_linewidth(1)
    print("Creating Valider button for ND case...")
    btn_valider.on_clicked(lambda x: _on_valider_clicked(controller, result))
    print("Valider button callback set for ND case")

    plt.tight_layout()
    plt.show()

    return result


if __name__ == "__main__":
    parcels_test = [
        {"id": 0, "taux_perte": 5.0, "coeff_croissance": 1.2, "coeff_production": 1.5, "vol_min": 100,
         "solve_btn": solve_graphique},
        {"id": 1, "taux_perte": 5.5, "coeff_croissance": 1.2, "coeff_production": 1.5, "vol_min": 120},
    ]

    global_data_test = {
        "besoin_total_croissance": 500,
        "besoin_total_production": 300,
    }

    print("Test avec 2 parcelles:")
    result = afficher_graphique(parcels_test, global_data_test)
    if result:
        print(f"Solution: {result.get('solution')}")
        print(f"Coût: {result.get('cout')}")