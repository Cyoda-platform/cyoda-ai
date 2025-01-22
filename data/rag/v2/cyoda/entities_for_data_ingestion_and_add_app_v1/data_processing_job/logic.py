import asyncio
import logging

from common.auth.auth import authenticate
from common.config.config import ENTITY_VERSION
from app_init.app_init import entity_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def data_processing_job_scheduler(token: str, data: dict) -> dict:
    # Save a job entity with data model $data to cyoda
    job_entity = await entity_service.add_item(
        token, "data_processing_job", ENTITY_VERSION, data
    )
    return job_entity


async def main():
    test_data = {
        "job_id": "job_001",
        "job_name": "Data Processing Job",
        "scheduled_time": "2023-10-01T17:00:00Z",
        "status": "completed",
        "start_time": "2023-10-01T17:00:00Z",
        "end_time": "2023-10-01T17:30:00Z",
        "total_records_processed": 150,
        "successful_records": 145,
        "failed_records": 5,
        "failure_reason": [
            "Timeout",
            "Data format error"
        ],
        "summary": {
            "average_processing_time_ms": 250,
            "max_processing_time_ms": 500,
            "min_processing_time_ms": 100
        },
        "data_source": {
            "source_name": "External API",
            "source_url": "https://api.example.com/data",
            "data_retrieval_method": "GET"
        },
        "request_parameters": {
            "param1": "value1",
            "param2": "value2",
            "param3": "value3",
            "country": "FI"
        },
        "recipients": [
            {
                "name": "Admin User",
                "email": "admin@example.com"
            }
        ]
    }

    try:
        token = await authenticate()
        result = await data_processing_job_scheduler(token, test_data)
        print(f"Job scheduled successfully. Job details: {result}")
    except Exception as e:
        print(f"Error scheduling job: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())