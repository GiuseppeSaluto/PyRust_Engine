# Builder stage
FROM rust:latest AS builder
WORKDIR /usr/src/app
COPY . .
RUN cargo install --path .

# Runtime stage
FROM debian:bullseye-slim
COPY --from=builder /usr/local/cargo/bin/pricing_engine_rs /usr/local/bin/pricing_engine_rs
CMD ["pricing_engine_rs"]
