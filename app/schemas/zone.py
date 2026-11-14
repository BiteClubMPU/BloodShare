from pydantic import BaseModel, ConfigDict


class ZoneBase(BaseModel):
    name: str
    code: str


class ZoneCreate(ZoneBase):
    pass


class ZoneResponse(ZoneBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
