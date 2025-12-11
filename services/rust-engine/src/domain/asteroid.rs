use crate::dto::asteroid_dto::AsteroidDTO;

#[derive(Debug, Clone)]
pub struct Asteroid {
    pub id: String,
    pub name: String,
    pub absolute_magnitude: f64,
    pub diameter_km: f64,
    pub velocity_kps: f64,
    pub distance_km: f64,
    pub hazardous: bool,
    pub date: String,
    pub orbiting_body: String,
}

impl TryFrom<AsteroidDTO> for Asteroid {
    type Error = String;

    fn try_from(dto: AsteroidDTO) -> Result<Self, Self::Error> {
        if dto.id.trim().is_empty() {
            return Err("AsteroidDTO id is empty".into());
        }

        if dto.diameter_avg_km <= 0.0 {
            return Err(format!("Invalid diameter: {} km", dto.diameter_avg_km));
        }

        if dto.relative_velocity_kps < 0.0 {
            return Err(format!(
                "Velocity cannot be negative: {}",
                dto.relative_velocity_kps
            ));
        }

        if dto.miss_distance_km < 0.0 {
            return Err(format!(
                "Distance cannot be negative: {}",
                dto.miss_distance_km
            ));
        }

        Ok(Asteroid {
            id: dto.id,
            name: dto.name,
            absolute_magnitude: dto.absolute_magnitude_h,
            diameter_km: dto.diameter_avg_km,
            velocity_kps: dto.relative_velocity_kps,
            distance_km: dto.miss_distance_km,
            hazardous: dto.is_potentially_hazardous,
            date: dto.close_approach_date,
            orbiting_body: dto.orbiting_body,
        })
    }
}
