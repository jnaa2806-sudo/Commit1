from abc import ABC, abstractmethod

class Recurso(ABC):
    def __init__(self, codigo: str):
        self.codigo = codigo
        self.retraso = 0

    @abstractmethod
    def calcular_multa(self) -> float:
        pass

class PrestamoLibro(Recurso):
    def calcular_multa(self) -> float:
        return self.retraso * 2.30

class UsoSalaEstudio(Recurso):
    def __init__(self, codigo: str, alumnos_espera: int):
        super().__init__(codigo)
        self.alumnos_espera = alumnos_espera
        
    def calcular_multa(self) -> float:
        factor = 1.5 if self.alumnos_espera > 5 else 1.0
        return self.retraso * factor

class Bibliotecario:
    def __init__(self, nombre_empleado: str, codigo_usuario: str):
        self.nombre = nombre_empleado
        self.codigo_usuario = codigo_usuario

class RegistroAtencion:
    def __init__(self, codigo_reg: str, carnet_alumno: str, nombre_bib: str, cod_bib: str):
        self.codigo_reg = codigo_reg
        self.carnet_alumno = carnet_alumno
        self.bibliotecario = Bibliotecario(nombre_bib, cod_bib)
        self._recursos = []
        self.estado = "ACTIVO"

    @property
    def recursos(self):
        return tuple(self._recursos)

    def agregar_recurso(self, recurso: Recurso):
        if len(self._recursos) >= 4:
            raise ValueError("Limite de recursos por atencion alcanzado")
        self._recursos.append(recurso)

    def ejecutar_auditoria(self):
        if self.estado == "CUENTA_SUSPENDIDA":
            raise RuntimeError("Operacion denegada: La cuenta esta suspendida")
            
        if not self._recursos:
            return 0.0

        total_multas = sum(r.calcular_multa() for r in self._recursos)
        promedio = total_multas / len(self._recursos)
        
        es_auxiliar = self.bibliotecario.codigo_usuario.startswith('AUX')
        tiene_sala_critica = any(isinstance(r, UsoSalaEstudio) and r.alumnos_espera > 10 for r in self._recursos)
        
        if promedio > 15.0 or (es_auxiliar and tiene_sala_critica):
            self.estado = "CUENTA_SUSPENDIDA"
            raise RuntimeError("Protocolo de restriccion activado: Cuenta Suspendida")
            
        return promedio
    
















   