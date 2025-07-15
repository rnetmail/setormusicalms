# setormusicalms/backend/app/main_production.py

# Endpoint para buscar todos os itens do repertório com filtros opcionais
@router.get("/repertorio/all", response_model=List[RepertorioItemSchema])
def get_all_repertorio(
    type_filter: Optional[str] = None,
    year_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(RepertorioItem).filter(RepertorioItem.active)
    if type_filter:
        query = query.filter(RepertorioItem.type == type_filter)
    if year:
        query = query.filter(func.strftime("%Y", RepertorioItem.date) == year)
    return query.order_by(RepertorioItem.year.desc(), RepertorioItem.title).all()


# Endpoint para buscar todos os itens da agenda com filtros opcionais
@router.get("/agenda/all", response_model=List[AgendaItemSchema])
def get_all_agenda(
    group_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if group_filter:
        query = query.filter(AgendaItem.group == group_filter)
    return query.order_by(AgendaItem.date.desc()).all()


# Endpoint para buscar todos os itens da agenda de um grupo específico
@router.get("/agenda/{group_type}", response_model=List[AgendaItemSchema])
def get_agenda_by_group(group_type: str, db: Session = Depends(get_db)):
    return db.query(AgendaItem).filter(
        AgendaItem.group == group_type,
        AgendaItem.active


@router.get("/recados/all", response_model=List[RecadoItemSchema])
def get_all_recados(
    group_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(RecadoItem).filter(RecadoItem.active)
    if group_filter:
        query = query.filter(RecadoItem.group == group_filter)
    return query.order_by(RecadoItem.date.desc()).all()

@router.get("/recados/{group_type}", response_model=List[RecadoItemSchema])
def get_recados_by_group(group_type: str, db: Session = Depends(get_db)):
    return db.query(RecadoItem).filter(
        RecadoItem.group == group_type,
        RecadoItem.active
    ).order_by(RecadoItem.date.desc()).all()
