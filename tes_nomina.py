
import unittest
from my import (
    EmpleadoAsalariado,
    EmpleadoPorHoras,
    EmpleadoPorComision,
    EmpleadoTemporal
)


class TestNomina(unittest.TestCase):

    def test_bono_asalariado_mas_de_cinco_anos(self):
        empleado = EmpleadoAsalariado(
            "1", "Carlos", 3_000_000, 6
        )
        self.assertEqual(empleado.calcular_salario_bruto(), 3_300_000)

    def test_asalariado_con_cinco_anos_no_recibe_bono(self):
        empleado = EmpleadoAsalariado(
            "2", "Laura", 3_000_000, 5
        )
        self.assertEqual(empleado.calcular_salario_bruto(), 3_000_000)

    def test_horas_extras(self):
        empleado = EmpleadoPorHoras(
            "3", "Pedro", 20_000, 45, 0
        )
        # 40 horas normales y 5 horas extras a 1.5.
        self.assertEqual(empleado.calcular_salario_bruto(), 950_000)

    def test_bono_por_ventas_superiores_a_veinte_millones(self):
        empleado = EmpleadoPorComision(
            "4", "Ana", 2_000_000, 25_000_000, 0.05
        )
        # Base + 5% de comision + 3% de bono.
        self.assertEqual(empleado.calcular_salario_bruto(), 4_000_000)

    def test_empleado_temporal_sin_bonos(self):
        empleado = EmpleadoTemporal(
            "5", "Luis", 1_800_000, 6
        )
        self.assertEqual(empleado.calcular_salario_bruto(), 1_800_000)
        self.assertEqual(empleado.calcular_beneficios(), 0)

    def test_no_permite_horas_negativas(self):
        with self.assertRaises(ValueError):
            EmpleadoPorHoras("6", "Sofia", 20_000, -5, 2)

    def test_no_permite_ventas_negativas(self):
        with self.assertRaises(ValueError):
            EmpleadoPorComision(
                "7", "Juan", 2_000_000, -100, 0.05
            )

    def test_no_permite_salario_neto_negativo(self):
        empleado = EmpleadoTemporal(
            "8", "Mario", 1_000_000, 3, arl_rate=30
        )
        with self.assertRaises(ValueError):
            empleado.calcular_nomina()


if __name__ == "__main__":
    unittest.main()
