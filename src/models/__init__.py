"""Models for SGHSS application."""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Usuario:
    """User model."""

    id: Optional[int] = None
    nome: str = ""
    email: str = ""
    senha: str = ""
    tipo: str = ""  # admin, medico, paciente, etc
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None

    def to_dict(self, include_password: bool = False) -> dict:
        """
        Convert model to dictionary.

        Args:
            include_password: Include password in output.

        Returns:
            Dictionary representation of the model.
        """
        data = {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "tipo": self.tipo,
            "criado_em": self.criado_em,
            "atualizado_em": self.atualizado_em,
        }
        if include_password:
            data["senha"] = self.senha
        return data


@dataclass
class Paciente:
    """Patient model."""

    id: Optional[int] = None
    nome: str = ""
    email: str = ""
    telefone: str = ""
    cpf: str = ""
    data_nascimento: Optional[str] = None
    endereco: str = ""
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None

    def to_dict(self) -> dict:
        """
        Convert model to dictionary.

        Returns:
            Dictionary representation of the model.
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento,
            "endereco": self.endereco,
            "criado_em": self.criado_em,
            "atualizado_em": self.atualizado_em,
        }


@dataclass
class Profissional:
    """Professional/Doctor model."""

    id: Optional[int] = None
    nome: str = ""
    email: str = ""
    telefone: str = ""
    especialidade: str = ""
    registro: str = ""  # Medical registration number
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None

    def to_dict(self) -> dict:
        """
        Convert model to dictionary.

        Returns:
            Dictionary representation of the model.
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "especialidade": self.especialidade,
            "registro": self.registro,
            "criado_em": self.criado_em,
            "atualizado_em": self.atualizado_em,
        }


@dataclass
class Consulta:
    """Consultation model."""

    id: Optional[int] = None
    paciente_id: int = 0
    profissional_id: Optional[int] = None
    data: str = ""
    motivo: str = ""
    observacoes: str = ""
    tipo_consulta: str = "presencial"  # presencial ou telemedicina
    link_video: Optional[str] = None
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None

    def to_dict(self) -> dict:
        """
        Convert model to dictionary.

        Returns:
            Dictionary representation of the model.
        """
        return {
            "id": self.id,
            "paciente_id": self.paciente_id,
            "profissional_id": self.profissional_id,
            "data": self.data,
            "motivo": self.motivo,
            "observacoes": self.observacoes,
            "tipo_consulta": self.tipo_consulta,
            "link_video": self.link_video,
            "criado_em": self.criado_em,
            "atualizado_em": self.atualizado_em,
        }


@dataclass
class Medicamento:
    """Medication model."""

    id: Optional[int] = None
    nome: str = ""
    descricao: str = ""
    dosagem: str = ""
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None

    def to_dict(self) -> dict:
        """
        Convert model to dictionary.

        Returns:
            Dictionary representation of the model.
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "dosagem": self.dosagem,
            "criado_em": self.criado_em,
            "atualizado_em": self.atualizado_em,
        }


@dataclass
class Prescricao:
    """Prescription model."""

    id: Optional[int] = None
    consulta_id: int = 0
    medicamento_id: int = 0
    duracao: str = ""
    instrucoes: str = ""
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None

    def to_dict(self) -> dict:
        """
        Convert model to dictionary.

        Returns:
            Dictionary representation of the model.
        """
        return {
            "id": self.id,
            "consulta_id": self.consulta_id,
            "medicamento_id": self.medicamento_id,
            "duracao": self.duracao,
            "instrucoes": self.instrucoes,
            "criado_em": self.criado_em,
            "atualizado_em": self.atualizado_em,
        }
