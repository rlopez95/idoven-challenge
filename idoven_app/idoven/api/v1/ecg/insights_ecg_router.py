from fastapi import APIRouter, Depends, HTTPException, Security, status
from idoven_app.idoven.api.v1.auth import get_current_user
from idoven_app.idoven.domain.command_handler import CommandHandler
from idoven_app.idoven.domain.ecg import ECGNotFoundException
from idoven_app.idoven.domain.user import Role, User
from idoven_app.idoven.infrastructure.mongo_ecg_repository import MongoECGRepository
from idoven_app.idoven.use_cases.insights_ecg_command import (
    InsightsCommandResponse,
    InsightsECGCommand,
    InsightsECGCommandHandler,
)
from idoven_app.idoven.config import settings


insights_ecg_router = APIRouter(prefix=settings.api_v1_prefix)


async def _insigths_ecg_command_handler() -> CommandHandler:
    repository = MongoECGRepository(mongo_uri=settings.mongo_uri)
    return InsightsECGCommandHandler(repository)


@insights_ecg_router.get("/insights/{ecg_id}", status_code=status.HTTP_200_OK)
async def insights_ecg(
    ecg_id: str,
    user: User = Security(get_current_user, scopes=[Role.USER]),
    insights_ecg_command_handler: CommandHandler = Depends(_insigths_ecg_command_handler),
):
    try:
        command = InsightsECGCommand(ecg_id=ecg_id, user_id=user.user_id)
        insight_response: InsightsCommandResponse = await insights_ecg_command_handler.process(command)
    except ECGNotFoundException as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ECG {ecg_id} not found for current user {user.username}"
        ) from exception
    return insight_response.insights
