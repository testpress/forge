from model_utils.models import TimeStampedModel
from safedelete.config import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel
from simple_history.models import HistoricalRecords


class BaseModel(TimeStampedModel, SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
