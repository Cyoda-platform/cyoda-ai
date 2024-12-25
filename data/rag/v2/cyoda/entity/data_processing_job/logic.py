import logging

from common.auth.auth import authenticate
from common.config.config import ENTITY_VERSION
from common.app_init import entity_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def data_processing_job_scheduler(token: str, data: dict) -> dict:
    # Save a job entity with data model $data to cyoda
    job_entity = entity_service.add_item(
        token, "data_processing_job", ENTITY_VERSION, data
    )
    return job_entity

def main():
    # Test data for the job scheduler
    test_token = "test_token_123"
    test_data = {
        "job_id": "job_001",
        "job_name": "Data Processing Job",
        "data_source": {
            "source_name": "External API",
            "source_url": "https://api.example.com/data",
            "data_retrieval_method": "GET",
        },
        "request_parameters": {
            "code": "7080005051286",
            "country": "FI",
            "name": "",
        },
        "recipients": [
            {"name": "Admin User", "email": "admin@example.com"},
            {"name": "Data Analyst", "email": "analyst@example.com"},
        ],
        "report": {
            "report_id": "report_001",
            "generated_at": "2023-10-01T17:35:00Z",
            "report_title": "Monthly Data Processing Report",
            "distribution_info": {
                "sent_at": "2023-10-01T17:40:00Z",
                "communication_method": "Email",
            },
        },
    }

    try:
        token = authenticate()
        result = data_processing_job_scheduler(token, test_data)
        print(f"Job scheduled successfully. Job details: {result}")
    except Exception as e:
        print(f"Error scheduling job: {str(e)}")

if __name__ == "__main__":
    main()
