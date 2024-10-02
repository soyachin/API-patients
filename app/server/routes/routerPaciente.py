from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    add_paciente,
    delete_paciente,
    update_paciente,
    get_pacientes,
    get_pacientes_id,
)

from app.server.models.patientModel import (
    error_response_model,
    response_model,
    Paciente,
    PacienteUpdate
)

router = APIRouter()
