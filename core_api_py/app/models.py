from datetime import datetime, timezone
from typing import Dict, Any

class PricingLog:
    def __init__(self, input_data: Dict[str, Any], result_data: Dict[str, Any]) -> None:
        self.document = {
            "timestamp": datetime.now(timezone.utc),
            "input": input_data,
            "result": result_data,
            "engine": "rust"
        }

    def to_dict(self) -> Dict[str, Any]:
        return self.document

class PriceRequest:
    base_price: float
    factor: float


class PriceResponse:
    final_price: float
    processed_by: str
