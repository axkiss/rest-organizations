from fastapi import APIRouter, Depends

from src.auth.utils import verify_header_api_key
from src.organizations.repositories import get_organization_repository, OrganizationRepository
from src.organizations.schemas import OrganizationFilterSchema, OrganizationOutSchema

router = APIRouter()


@router.get(
    "/organizations",
    response_model=list[OrganizationOutSchema],
    dependencies=[Depends(verify_header_api_key)],
)
async def filter_organizations(
    filters: OrganizationFilterSchema = Depends(),
    repo: OrganizationRepository =Depends(get_organization_repository),
):
    return await repo.get_list(filters)
