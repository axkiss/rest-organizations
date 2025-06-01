from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Model(DeclarativeBase):
    pass


org_activity = Table(
    "org_activity",
    Model.metadata,
    Column("organization_id", ForeignKey("organization.id"), primary_key=True),
    Column("activity_id", ForeignKey("activity.id"), primary_key=True),
)


class Building(Model):
    __tablename__ = "building"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]

    organizations: Mapped[list["Organization"]] = relationship(
        back_populates="building"
    )


class Activity(Model):
    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activity.id"), nullable=True
    )

    children: Mapped[list["Activity"]] = relationship(
        backref="parent", remote_side=[id]
    )


class Organization(Model):
    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    building_id: Mapped[int] = mapped_column(ForeignKey("building.id"))

    building: Mapped["Building"] = relationship(back_populates="organizations")
    phones: Mapped[list["Phone"]] = relationship(
        back_populates="organization", cascade="all, delete-orphan"
    )
    activities: Mapped[list["Activity"]] = relationship(
        secondary=org_activity, backref="organizations"
    )


class Phone(Model):
    __tablename__ = "phone"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str]
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))

    organization: Mapped["Organization"] = relationship(back_populates="phones")
