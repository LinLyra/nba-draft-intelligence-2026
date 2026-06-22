from pydantic import BaseModel, Field


class Prospect(BaseModel):
    player_id: str
    player_name: str
    position: str
    age: float | None = None
    height_in: float | None = None
    weight_lb: float | None = None
    wingspan_in: float | None = None
    standing_reach_in: float | None = None
    school_or_league: str | None = None
    country: str | None = None


class DraftPick(BaseModel):
    year: int
    pick_number: int = Field(ge=1, le=60)
    original_team: str
    current_owner: str
    via_trade: bool = False
    protection: str | None = None


class TeamNeed(BaseModel):
    team: str
    rebuild_stage: str
    need_creation: float = Field(ge=0, le=1)
    need_shooting: float = Field(ge=0, le=1)
    need_defense: float = Field(ge=0, le=1)
    need_size: float = Field(ge=0, le=1)
    need_rim_protection: float = Field(ge=0, le=1)
    need_ready_now: float = Field(ge=0, le=1)
    need_upside: float = Field(ge=0, le=1)
