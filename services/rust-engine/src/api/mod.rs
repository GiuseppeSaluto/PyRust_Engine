use axum::Router;

mod asteroid;

pub use asteroid::process_asteroid;

pub fn router() -> Router {
    Router::new()
        .route("/process/asteroid", axum::routing::post(process_asteroid))
}
