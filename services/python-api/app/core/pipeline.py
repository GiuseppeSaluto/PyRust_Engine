from flask import current_app
from requests.exceptions import RequestException

from app.core.dto_mapper import map_mongo_document_to_asteroid
from app.core.mongodb import MongoDBClient
from app.core.rust_client import process_asteroid_with_rust
from app.utils.logger import logger


class AnalysisPipeline:
      
    @staticmethod
    def analyze_unprocessed_asteroids(limit: int = 100) -> dict:
        mongo: MongoDBClient | None = current_app.extensions.get("mongo")
        if not mongo:
            raise RuntimeError("MongoDB extension not initialized")
        
        logger.info(f"Starting analysis pipeline for up to {limit} asteroids")
        
        stats = {
            "total_fetched": 0,
            "processed": 0,
            "failed": 0,
            "skipped": 0,
        }
        
        try:
            raw_asteroids = mongo.get_unprocessed_asteroids(limit=limit)
            stats["total_fetched"] = len(raw_asteroids)
            
            logger.info(f"Fetched {len(raw_asteroids)} unprocessed asteroids")
            
            for raw_doc in raw_asteroids:
                asteroid_id = raw_doc.get("asteroid", {}).get("id", "unknown")
                
                try:
                    asteroid = map_mongo_document_to_asteroid(raw_doc)
                    
                    if asteroid is None:
                        logger.warning(f"Skipping asteroid {asteroid_id}: mapping failed")
                        stats["skipped"] += 1
                        continue
                    
                    asteroid_dto = asteroid.to_dto_dict()
                    
                    risk_result = process_asteroid_with_rust(asteroid_dto)
                    
                    mongo.save_analysis_result(asteroid.id, risk_result)
                    
                    stats["processed"] += 1
                    logger.info(
                        f"Successfully analyzed asteroid {asteroid.id} "
                        f"(risk: {risk_result.get('risk_level', 'unknown')})"
                    )
                    
                except RequestException as e:
                    logger.error(f"Rust engine error for asteroid {asteroid_id}: {e}")
                    stats["failed"] += 1
                    
                except Exception as e:
                    logger.error(f"Unexpected error processing asteroid {asteroid_id}: {e}")
                    stats["failed"] += 1
            
            logger.info(
                f"Pipeline completed: {stats['processed']} processed, "
                f"{stats['failed']} failed, {stats['skipped']} skipped"
            )
            
            return stats
            
        except Exception as e:
            logger.critical(f"Pipeline failed: {e}")
            raise


    @staticmethod
    def analyze_single_asteroid(asteroid_id: str) -> dict:
        
        mongo: MongoDBClient | None = current_app.extensions.get("mongo")
        if not mongo:
            raise RuntimeError("MongoDB extension not initialized")
        
        logger.info(f"Analyzing single asteroid: {asteroid_id}")
        
        raw_doc = mongo.get_raw_asteroid_by_id(asteroid_id)
        
        if not raw_doc:
            raise ValueError(f"Asteroid {asteroid_id} not found in database")
        
        asteroid = map_mongo_document_to_asteroid(raw_doc)
        if asteroid is None:
            raise ValueError(f"Asteroid {asteroid_id} mapping failed")
        
        asteroid_dto = asteroid.to_dto_dict()
        
        risk_result = process_asteroid_with_rust(asteroid_dto)
        
        mongo.save_analysis_result(asteroid.id, risk_result)
        
        logger.info(f"Single asteroid analysis complete: {asteroid_id}")
        
        return risk_result
