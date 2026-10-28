
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ResultadoNomina:
    salario_bruto: float
    deducciones: float
    salario_neto: float
    beneficios_empresa: float
    ahorro_empleado: float = 0.0


class Empleado(ABC):
    def __init__(self, identificacion, nombre, arl_rate=0.0):
        if arl_rate < 0:
            raise ValueError("La tasa de ARL no puede ser negativa.")

        self.identificacion = identificacion
        self.nombre = nombre
        self.arl_rate = arl_rate

    @abstractmethod
    def calcular_salario_bruto(self):
        pass

    @abstractmethod
    def calcular_beneficios(self):
        pass

    def calcular_ahorro(self):
        return 0.0

    def calcular_nomina(self):
        bruto = self.calcular_salario_bruto()
        beneficios = self.calcular_beneficios()
        ahorro = self.calcular_ahorro()

        # El 4% corresponde conjuntamente a seguro social y pension.
        seguro_y_pension = bruto * 0.04

        # La actividad no define la tasa de ARL.
        arl = bruto * self.arl_rate

        deducciones = seguro_y_pension + arl + ahorro
        neto = bruto - deducciones

        if neto < 0:
            raise ValueError("El salario neto no puede ser negativo.")

        return ResultadoNomina(
            salario_bruto=bruto,
            deducciones=deducciones,
            salario_neto=neto,
            beneficios_empresa=beneficios,
            ahorro_empleado=ahorro
        )


class EmpleadoAsalariado(Empleado):
    def __init__(self, identificacion, nombre, salario, antiguedad,
                 arl_rate=0.0):
        super().__init__(identificacion, nombre, arl_rate)

        if salario < 0 or antiguedad < 0:
            raise ValueError("Salario y antiguedad no pueden ser negativos.")

        self.salario = salario
        self.antiguedad = antiguedad

    def calcular_salario_bruto(self):
        bono = self.salario * 0.10 if self.antiguedad > 5 else 0
        return self.salario + bono

    def calcular_beneficios(self):
        return 1_000_000


class EmpleadoPorHoras(Empleado):
    def __init__(self, identificacion, nombre, tarifa, horas,
                 antiguedad, acepta_ahorro=False, arl_rate=0.0):
        super().__init__(identificacion, nombre, arl_rate)

        if tarifa < 0 or horas < 0 or antiguedad < 0:
            raise ValueError("Tarifa, horas y antiguedad deben ser válidas.")

        self.tarifa = tarifa
        self.horas = horas
        self.antiguedad = antiguedad
        self.acepta_ahorro = acepta_ahorro

    def calcular_salario_bruto(self):
        horas_normales = min(self.horas, 40)
        horas_extras = max(self.horas - 40, 0)

        pago_normal = horas_normales * self.tarifa
        pago_extra = horas_extras * self.tarifa * 1.5

        return pago_normal + pago_extra

    def calcular_beneficios(self):
        return 0.0

    def calcular_ahorro(self):
        if self.antiguedad > 1 and self.acepta_ahorro:
            return self.calcular_salario_bruto() * 0.02
        return 0.0


class EmpleadoPorComision(Empleado):
    def __init__(self, identificacion, nombre, salario_base,
                 ventas, porcentaje_comision, arl_rate=0.0):
        super().__init__(identificacion, nombre, arl_rate)

        if salario_base < 0 or ventas < 0:
            raise ValueError("Salario base y ventas no pueden ser negativos.")

        if not 0 <= porcentaje_comision <= 1:
            raise ValueError("La comisión debe estar entre 0 y 1.")

        self.salario_base = salario_base
        self.ventas = ventas
        self.porcentaje_comision = porcentaje_comision

    def calcular_salario_bruto(self):
        comision = self.ventas * self.porcentaje_comision
        bono = self.ventas * 0.03 if self.ventas > 20_000_000 else 0
        return self.salario_base + comision + bono

    def calcular_beneficios(self):
        return 1_000_000


class EmpleadoTemporal(Empleado):
    def __init__(self, identificacion, nombre, salario,
                 duracion_contrato, arl_rate=0.0):
        super().__init__(identificacion, nombre, arl_rate)

        if salario < 0 or duracion_contrato <= 0:
            raise ValueError("Salario o duración del contrato inválidos.")

        self.salario = salario
        self.duracion_contrato = duracion_contrato

    def calcular_salario_bruto(self):
        return self.salario

    def calcular_beneficios(self):
        return 0.0


def mostrar_nomina(empleado):
    resultado = empleado.calcular_nomina()

    print(f"\nEmpleado: {empleado.nombre}")
    print(f"Identificación: {empleado.identificacion}")
    print(f"Salario bruto: ${resultado.salario_bruto:,.0f}")
    print(f"Deducciones: ${resultado.deducciones:,.0f}")
    print(f"Salario neto: ${resultado.salario_neto:,.0f}")
    print(f"Beneficios cubiertos por la empresa: "
          f"${resultado.beneficios_empresa:,.0f}")
    print(f"Ahorro del empleado: ${resultado.ahorro_empleado:,.0f}")


if __name__ == "__main__":
    empleados = [
        EmpleadoAsalariado("101", "Carlos", 3_000_000, 6),
        EmpleadoPorHoras("102", "Laura", 20_000, 45, 2, True),
        EmpleadoPorComision(
            "103", "Andrés", 2_000_000, 25_000_000, 0.05
        ),
        EmpleadoTemporal("104", "María", 1_800_000, 6)
    ]

    for empleado in empleados:
        mostrar_nomina(empleado)
