"""Pydantic request and response schemas."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Severity = Literal["critical", "warning", "info"]


class AlertCreate(BaseModel):
    title: str = Field(min_length=1)
    severity: Severity
    source: str = Field(min_length=1)
    metric_name: str = Field(min_length=1)
    metric_value: float
    threshold: float


class AlertOut(AlertCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class ExplainResponse(BaseModel):
    alert_id: int
    explanation: str
    generated_at: datetime