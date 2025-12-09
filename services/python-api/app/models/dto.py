class AsteroidDTO:
    id: str
    name: str
    absolute_magnitude_h: float
    diameter_min_km: float
    diameter_max_km: float
    diameter_avg_km: float
    close_approach_date: str
    relative_velocity_kps: float
    miss_distance_km: float
    is_potentially_hazardous: bool
    orbiting_body: str

    def __init__(self, raw_doc: dict) -> None:
        if not raw_doc:
            raise ValueError("Raw document for AsteroidDTO cannot be None or empty.")

        raw = raw_doc.get("asteroid", {})
        if not raw:
            raise ValueError("Document missing 'asteroid' data.")

        # Prefer the official NASA identifier
        self.id = raw.get("neo_reference_id", raw.get("id", ""))
        self.name = raw.get("name", "")
        self.absolute_magnitude_h = float(raw.get("absolute_magnitude_h", 0.0))

        diam_km = raw.get("estimated_diameter", {}).get("kilometers", {})
        self.diameter_min_km = float(diam_km.get("estimated_diameter_min", 0.0))
        self.diameter_max_km = float(diam_km.get("estimated_diameter_max", 0.0))
        self.diameter_avg_km = (
            self.diameter_min_km + self.diameter_max_km
        ) / 2 if (self.diameter_min_km and self.diameter_max_km) else 0.0

        ca_list = raw.get("close_approach_data", [])
        if ca_list:
            ca = ca_list[0]
            self.close_approach_date = ca.get("close_approach_date", "")

            rel_vel = ca.get("relative_velocity", {})
            self.relative_velocity_kps = self._safe_float(
                rel_vel.get("kilometers_per_second", 0.0)
            )

            miss_dist = ca.get("miss_distance", {})
            self.miss_distance_km = self._safe_float(
                miss_dist.get("kilometers", 0.0)
            )

            self.orbiting_body = ca.get("orbiting_body", "")
        else:
            self.close_approach_date = ""
            self.relative_velocity_kps = 0.0
            self.miss_distance_km = 0.0
            self.orbiting_body = ""

        self.is_potentially_hazardous = raw.get(
            "is_potentially_hazardous_asteroid", False
        )

    @staticmethod
    def _safe_float(value) -> float:
        try:
            return float(value)
        except Exception:
            return 0.0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "absolute_magnitude_h": self.absolute_magnitude_h,
            "diameter_min_km": self.diameter_min_km,
            "diameter_max_km": self.diameter_max_km,
            "diameter_avg_km": self.diameter_avg_km,
            "close_approach_date": self.close_approach_date,
            "relative_velocity_kps": self.relative_velocity_kps,
            "miss_distance_km": self.miss_distance_km,
            "is_potentially_hazardous": self.is_potentially_hazardous,
            "orbiting_body": self.orbiting_body,
        }