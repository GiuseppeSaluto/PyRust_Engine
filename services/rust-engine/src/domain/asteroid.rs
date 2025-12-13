use crate::{domain::error::DomainError, dto::asteroid_dto::AsteroidDTO};

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
    type Error = DomainError;

    fn try_from(dto: AsteroidDTO) -> Result<Self, Self::Error> {
        if dto.id.trim().is_empty() {
            return Err(DomainError::InvalidId);
        }

        if dto.diameter_avg_km <= 0.0 {
            return Err(DomainError::InvalidDiameter(dto.diameter_avg_km));
        }

        if dto.relative_velocity_kps < 0.0 {
            return Err(DomainError::InvalidVelocity(dto.relative_velocity_kps));
        }

        if dto.miss_distance_km < 0.0 {
            return Err(DomainError::InvalidField("miss_distance_km"));
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

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::error::DomainError;
    use crate::dto::asteroid_dto::AsteroidDTO;

    #[test]
    fn asteroid_with_negative_diameter_is_rejected() {
        let dto = AsteroidDTO {
            id: "12345".to_string(),
            name: "Test Asteroid".to_string(),
            absolute_magnitude_h: 20.0,
            diameter_min_km: -1.0,
            diameter_max_km: 0.5,
            diameter_avg_km: -0.25,
            close_approach_date: "2025-01-01".to_string(),
            relative_velocity_kps: 10.0,
            miss_distance_km: 100_000.0,
            orbiting_body: "Earth".to_string(),
            is_potentially_hazardous: false,
        };

        let result = Asteroid::try_from(dto);

        assert!(result.is_err());

        match result.unwrap_err() {
            DomainError::InvalidDiameter(value) => {
                assert!(value < 0.0);
            }
            other => panic!("Unexpected error returned: {:?}", other),
        }
    }
}
