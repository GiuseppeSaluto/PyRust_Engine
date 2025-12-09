use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub struct AsteroidDTO {
    pub id: String,
    pub name: String,
    pub absolute_magnitude_h: f64,
    pub diameter_min_km: f64,
    pub diameter_max_km: f64,
    pub diameter_avg_km: f64,
    pub close_approach_date: String,
    pub relative_velocity_kps: f64,
    pub miss_distance_km: f64,
    pub orbiting_body: String,
    pub is_potentially_hazardous: bool,
}
