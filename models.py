"""Data models for Patient Health Analyzer application.

Defines dataclasses and enums for type-safe data handling.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class HealthStatus(str, Enum):
    """Enumeration of patient health status categories.

    Attributes:
        HEALTHY: Patient health status is normal/healthy
        AT_RISK: Patient has one or more at-risk health indicators
        CRITICAL: Patient has one or more critical health indicators
    """

    HEALTHY = "Healthy"
    AT_RISK = "AtRisk"
    CRITICAL = "Critical"


@dataclass
class Patient:
    """Data model representing a patient with health metrics.

    Attributes:
        patient_id (str): Unique identifier for the patient
        name (str): Patient's full name
        bmi (float): Body Mass Index value
        blood_pressure (str): Blood pressure in format 'systolic/diastolic'
        glucose_level (float): Fasting glucose level in mg/dL
        health_status (HealthStatus): Categorized health status
    """

    patient_id: str
    name: str
    bmi: float
    blood_pressure: str
    glucose_level: float
    health_status: HealthStatus = field(default=HealthStatus.HEALTHY)

    def __post_init__(self) -> None:
        """Validate patient data after initialization.

        Raises:
            ValueError: If any required field is invalid
        """
        if not self.patient_id or not isinstance(self.patient_id, str):
            raise ValueError("patient_id must be a non-empty string")

        if not self.name or not isinstance(self.name, str):
            raise ValueError("name must be a non-empty string")

        if not isinstance(self.bmi, (int, float)) or self.bmi < 0:
            raise ValueError("bmi must be a non-negative number")

        if not isinstance(self.glucose_level, (int, float)) or self.glucose_level < 0:
            raise ValueError("glucose_level must be a non-negative number")

        if "/" not in self.blood_pressure:
            raise ValueError("blood_pressure must be in format 'systolic/diastolic'")

        if not isinstance(self.health_status, HealthStatus):
            raise ValueError("health_status must be a HealthStatus enum value")
