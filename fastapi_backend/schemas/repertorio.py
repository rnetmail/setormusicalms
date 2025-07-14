class RepertorioItemCreate(RepertorioItemBase):
    pass

class RepertorioItemUpdate(BaseModel):
    type: Optional[str] = None
    title: Optional[str] = None
    arrangement: Optional[str] = None
    year: Optional[int] = None
    audio_url: Optional[str] = None
    video_url: Optional[str] = None
    sheet_music_url: Optional[str] = None
    naipes: Optional[List[str]] = None
    grupos: Optional[List[str]] = None
    active: Optional[bool] = None

class RepertorioItem(RepertorioItemBase):
    id: int

    class Config:
        from_attributes = True
