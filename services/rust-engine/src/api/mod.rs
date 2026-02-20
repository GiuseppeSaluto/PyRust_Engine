use axum::routing::{get, post};
use axum::Router;
mod asteroid;

pub use asteroid::process_asteroid;

async fn health() -> &'static str {
    "ok"
}

pub fn router() -> Router {
    Router::new()
        .route("/health", get(health))
        .route("/process/asteroid", post(process_asteroid))
}
