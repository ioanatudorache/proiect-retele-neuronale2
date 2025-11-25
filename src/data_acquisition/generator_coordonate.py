import numpy as np
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Stea:
    name: str
    ra: float
    dec: float
    magnitude: float

class Calculator:
    Andromeda = [
        Stea('alfa andromeda', 0.1397, 29.0902, 2.03),
        Stea('beta andromeda', 1.1867, 35.7611, 2.17),
        Stea('gamma andromeda', 0.092, 42.4567, 2.23),
        Stea('delta andromeda', 0.6789, 31.0061, 3.42),
        Stea('nu andromeda', 0.8547, 41.2237, 4.47),
        Stea('mu andromeda', 0.9703, 38.6433, 3.86)
    ]
    Ursa_Major = [
        Stea('alfa umajor', 11.062, 61.7508, 1.79),
        Stea('beta umajor', 11.0306, 56.3825, 2.37),
        Stea('upsilon umajor', 11.8970, 53.6947, 2.44),
        Stea('delta umajor', 12.2569, 57.0325, 3.31),
        Stea('epsilon umajor', 12.9006, 55.9597, 1.76),
        Stea('zeta umajor', 13.3989, 54.9253, 2.23),
        Stea('mu umajor', 13.7922, 49.3133, 1.85)
    ]
    Pegasus = [
        Stea('alfa pegasus', 23.0794, 15.2053, 2.49),
        Stea('beta pegasus', 23.0629, 28.0825, 2.42),
        Stea('upsilon pegasus', 0.2207, 15.1833, 2.83),
        Stea('epsilon pegasus', 21.7364, 9.8750, 2.38),
        Stea('zeta pegasus', 22.6917, 10.8311, 3.40),
        Stea('theta pegasus', 22.1683, 6.6169, 3.50),
        Stea('nu pegasus', 22.7744, 30.2217, 2.95)
    ]
    Ursa_Minor = [
        Stea('(Polaris) alfa uminor', 2.5303, 89.2641, 1.98),
        Stea('beta uminor', 14.8451, 74.1556, 2.08),
        Stea('upsilon uminor', 15.3450, 71.8340, 3.05),
        Stea('delta uminor', 17.5369, 86.5864, 4.35),
        Stea('epsilon uminor', 16.7664, 82.0372, 4.22),
        Stea('zeta uminor', 15.7344, 77.7947, 4.32),
        Stea('eta uminor', 16.2919, 75.7553, 4.95)
    ]

    def __init__(self, name: str, ra: float, dec: float, magnitude: float):
        self.name = name
        self.ra = ra
        self.dec = dec
        self.magnitude = magnitude

    def calculeaza_coord(self, stele: List[Stea], show_steps=True) -> List[Tuple[float, float]]:
        if show_steps:
            print("\n" + "=" * 70)
            print(f"Calculam coordonate pentru: {stele[0].name}")
            print("=" * 70)

        ra = np.array([s.ra for s in stele])
        dec = np.array([s.dec for s in stele])

        ra_min, ra_max = ra.min(), ra.max()
        dec_min, dec_max = dec.min(), dec.max()

        ra_norm = (ra - ra_min) / (ra_max - ra_min)
        dec_norm = (dec - dec_min) / (dec_max - dec_min)

        return [(round(r, 4), round(d, 4)) for r, d in zip(ra_norm, dec_norm)]

    def genereaza_coordonate(self):
        constelatii = {
            'Andromeda': self.Andromeda,
            'Ursa_Major': self.Ursa_Major,
            'Pegasus': self.Pegasus,
            'Ursa_Minor': self.Ursa_Minor
        }

        rezultat = {}
        for name, stele in constelatii.items():
            print(f"\n{'#' * 70}")
            print(f"# {name.upper()}")
            print(f"{'#' * 70}")

            coordonate = self.calculeaza_coord(stele, show_steps=True)
            rezultat[name] = coordonate

            print(f"'{name.replace(' ', '_')}': [")
            for coord in coordonate:
                print(f"    ({coord[0]:.4f}, {coord[1]:.4f}),")
            print("]")

        return rezultat
calc = Calculator("test", 0, 0, 0)
rezultat = calc.genereaza_coordonate()

print("\n=== Rezultatul final ===")
print(rezultat)
