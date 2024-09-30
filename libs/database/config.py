from typing import Final
from sqlalchemy.orm import registry
from sqlalchemy import MetaData


registro_dos_orms: Final = registry()
metadata = MetaData()
