"""Modèles de données pour les parcelles et le modèle global d'irrigation."""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class Parcel:
    """Représente une parcelle avec ses paramètres agronomiques."""
    id: int
    taux_perte: float
    coeff_croissance: float
    coeff_production: float
    vol_min: float
    nom: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Parcel":
        """Crée une Parcel à partir d'un dictionnaire."""
        return cls(
            id=int(data.get("id", 0)),
            taux_perte=float(data.get("taux_perte", 0.0)),
            coeff_croissance=float(data.get("coeff_croissance", 0.0)),
            coeff_production=float(data.get("coeff_production", 0.0)),
            vol_min=float(data.get("vol_min", 0.0)),
            nom=str(data.get("nom", f"Parcelle {int(data.get('id', 0)) + 1}")),
        )

    def get(self, key: str, default: Any = None) -> Any:
        """Permet d'utiliser .get() comme sur un dict."""
        return getattr(self, key, default)

    def to_dict(self) -> Dict[str, Any]:
        """Convertit la Parcel en dictionnaire."""
        return asdict(self)



@dataclass
class GlobalModel:
    """Représente les paramètres globaux du modèle d'irrigation."""
    besoin_total_croissance: float
    besoin_total_production: float

    def get(self, key: str, default: Any = None) -> Any:
        """Permet d'utiliser .get() comme sur un dict."""
        return getattr(self, key, default)


    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GlobalModel":
        """Crée un GlobalModel à partir d'un dictionnaire."""
        return cls(
            besoin_total_croissance=float(data.get("besoin_total_croissance", 0.0)),
            besoin_total_production=float(data.get("besoin_total_production", 0.0)),
        )

    def to_dict(self) -> Dict[str, float]:
        """Convertit le GlobalModel en dictionnaire."""
        return asdict(self)

