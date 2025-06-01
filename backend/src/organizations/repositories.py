from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, contains_eager

from src.database import get_async_session
from src.organizations.constants import DEGREE_M
from src.organizations.models import Organization, Activity, Building
from src.organizations.schemas import OrganizationFilterSchema
from src.repositories import IBaseRepository


class OrganizationRepository(IBaseRepository):
    async def get_list(self, filters: OrganizationFilterSchema | None = None):
        stmt = (
            select(Organization)
            .options(
                selectinload(Organization.phones),
                selectinload(Organization.activities),
                contains_eager(Organization.building),
            )
            .join(Organization.building)
            .outerjoin(Organization.activities)
        )
        if filters is None:
            result = await self.session.execute(stmt)
            return result.scalars().unique().all()

        if filters.building_id:
            stmt = stmt.where(Organization.building_id == filters.building_id)

        if filters.name:
            stmt = stmt.where(Organization.name.ilike(f"%{filters.name}%"))

        if filters.activity_id:
            ids = await ActivityRepository(self.session).get_descendants(
                filters.activity_id, depth=3
            )
            stmt = stmt.where(Activity.id.in_(ids))

        if filters.lat and filters.lon and filters.radius_m:
            building_ids_stmt = select(Building.id).where(
                func.sqrt(
                    func.pow((Building.latitude - filters.lat) * DEGREE_M, 2)
                    + func.pow(
                        (Building.longitude - filters.lon)
                        * DEGREE_M
                        * func.cos(func.radians(filters.lat)),
                        2,
                    )
                )
                <= filters.radius_m
            )
            stmt = stmt.where(Organization.building_id.in_(building_ids_stmt))

        if filters.lat_min and filters.lat_max and filters.lon_min and filters.lon_max:
            building_ids_stmt = select(Building.id).where(
                Building.latitude.between(filters.lat_min, filters.lat_max),
                Building.longitude.between(filters.lon_min, filters.lon_max),
            )
            stmt = stmt.where(Organization.building_id.in_(building_ids_stmt))

        result = await self.session.execute(stmt)
        return result.scalars().unique().all()


async def get_organization_repository(
    session: AsyncSession = Depends(get_async_session),
) -> OrganizationRepository:
    return OrganizationRepository(session)


class ActivityRepository(IBaseRepository):
    async def get_descendants(self, root_id: int, depth: int = 1) -> list[int]:
        result = []

        async def recurse(root_id: int, depth: int) -> None:
            result.append(root_id)
            if depth == 0:
                return
            depth -= 1
            stmt = select(Activity.id).where(Activity.parent_id == root_id)
            children_ids = (await self.session.execute(stmt)).scalars().all()
            for child_id in children_ids:
                await recurse(child_id, depth)

        await recurse(root_id, depth)
        return result
