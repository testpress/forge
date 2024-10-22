from model_utils.models import TimeStampedModel
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel
from simple_history.models import HistoricalRecords


class BaseModel(TimeStampedModel, SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
