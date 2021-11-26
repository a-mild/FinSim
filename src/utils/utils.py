import pandas as pd
from datetime import datetime


def get_BOM_datetime(today: datetime = datetime.today()) -> datetime:
    return (today + pd.offsets.MonthBegin(-1)).normalize().to_pydatetime()
