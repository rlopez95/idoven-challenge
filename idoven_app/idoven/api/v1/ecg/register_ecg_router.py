from fastapi import APIRouter, Depends, HTTPException, Security, status
from idoven_app.idoven.api.v1.auth import get_current_user
from idoven_app.idoven.domain.ecg import ECG, DuplicatedECGException, ECGInvalidException
from idoven_app.idoven.domain.command_handler import CommandHandler
from idoven_app.idoven.domain.user import Role, User
from idoven_app.idoven.use_cases.register_ecg_command import (
    RegisterECGCommand,
    RegisterECGCommandHandler,
)
from idoven_app.idoven.infrastructure.mongo_ecg_repository import MongoECGRepository
from idoven_app.idoven.api.v1.ecg.ecg_request import ECGRequest
from idoven_app.idoven.config import settings

register_ecg_router = APIRouter(prefix=settings.api_v1_prefix)


async def _register_ecg_command_handler() -> CommandHandler:
    repository = MongoECGRepository(mongo_uri=settings.mongo_uri)
    return RegisterECGCommandHandler(repository)


@register_ecg_router.post("/register", response_model=ECG, status_code=status.HTTP_201_CREATED)
async def register_ecg(
    ecg_request: ECGRequest,
    user: User = Security(get_current_user, scopes=[Role.USER]),
    register_ecg_command_handler: CommandHandler = Depends(_register_ecg_command_handler),
):
    try:
        command = RegisterECGCommand(
            ecg_id=ecg_request.ecg_id, user_id=user.user_id, date=ecg_request.date, leads=ecg_request.leads
        )
        await register_ecg_command_handler.process(command)
        return ECG(ecg_id=ecg_request.ecg_id, user_id=str(user.user_id), date=ecg_request.date, leads=ecg_request.leads)
    except ECGInvalidException as invalid_exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The ECG request with id: {ecg_request.ecg_id}, date: {ecg_request.date} and leads {ecg_request.leads} is invalid",
        ) from invalid_exception
    except DuplicatedECGException as duplicated_error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The ECG request with id: {ecg_request.ecg_id} already exists",
        ) from duplicated_error
