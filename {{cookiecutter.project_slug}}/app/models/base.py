from model_utils.models import TimeStampedModel
from safedelete.models import SOFT_DELETE
from simple_history.models import HistoricalRecords


class BaseModel(TimeStampedModel):
    _safedelete_policy = SOFT_DELETE
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
