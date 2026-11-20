from sqlalchemy import BigInteger, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class ItemSketchDB(Base):
    name: Mapped[str]
    tag: Mapped[str] = mapped_column(unique=True)
    hash: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None] = mapped_column(default=None)
    emodzi: Mapped[str | None] = mapped_column(default=None)
    custom_emodzi_id: Mapped[str | None] = mapped_column(default=None)
    data: Mapped[dict] = mapped_column(JSON, default={})
    items: Mapped[list['ItemDB']] = relationship(
        'ItemDB',
        uselist=True,
        lazy='select',
        back_populates='sketch',
        cascade='all, delete-orphan',
    )

    @property
    def all_counts_all_time(self) -> int:
        return max(self.data.get('all_counts_all_time', 0), 0)

    @all_counts_all_time.setter
    def all_counts_all_time(self, value: str) -> int:
        self.data = self.data | {'all_counts_all_time':value}
        return value


class ItemDB(Base):
    sketch_id: Mapped[int] = mapped_column(ForeignKey('ItemSketchDB.id'))
    sketch: Mapped[ItemSketchDB] = relationship('ItemSketchDB', uselist=False, lazy='joined', back_populates='items')
    inventory_id: Mapped[int] = mapped_column(ForeignKey('InventoryDB.id'))
    inventory: Mapped['InventoryDB'] = relationship(
        'InventoryDB',
        uselist=False,
        lazy='joined',
        back_populates='items',
    )
    quantity: Mapped[int] = mapped_column(default=1)
    data: Mapped[dict] = mapped_column(JSON, default=dict)


class InventoryDB(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('UserDB.id'))
    user: Mapped[Base] = relationship('UserDB', uselist=False, lazy='select', back_populates='inventory')
    items: Mapped[list[ItemDB]] = relationship(
        'ItemDB',
        uselist=True,
        lazy='select',
        back_populates='inventory',
        cascade='all, delete-orphan',
    )

    @property
    def items_by_sketch_id(self):
        return {i.sketch_id:i for i in self.items}
    
    @property
    def items_by_sketch_tag(self):
        return {i.sketch.tag:i for i in self.items}