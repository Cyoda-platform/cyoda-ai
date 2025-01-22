import json
import logging
import os
import unittest
from unittest.mock import patch
import asyncio

from app_init.app_init import ai_service, entity_service
from common.config.config import ENTITY_VERSION, TRINO_AI_API
from common.service.trino_service import get_trino_schema_id_by_entity_name
from common.util.utils import read_json_file, parse_json
from entity.raw_data_entity.connections.connections import ingest_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Updated async functions

async def ingest_data_process(meta, data):
    logger.info("Starting process to ingest raw data.")
    try:
        response_data = await ingest_data(code=data.get('request_parameters', {}).get('code', None), country=data.get('request_parameters', {}).get('country', None), name=None)
        # Save the raw data entity
        raw_data_entity_data = response_data  # Assume it returns the correct data structure
        raw_data_entity_id = await entity_service.add_item(
            meta["token"], "raw_data_entity", ENTITY_VERSION, raw_data_entity_data
        )
        data.setdefault("raw_data_entity", {})["technical_id"] = raw_data_entity_id
        logger.info("Raw data entity saved successfully.")
    except Exception as e:
        logger.error(f"Error in ingest_raw_data: {e}")
        raise


async def aggregate_raw_data(meta, data):
    logger.info("Starting process to aggregate raw data.")
    try:
        # This is an example of how to aggregate data with Trino
        # Get the path to the aggregated data entity schema file
        base_dir = os.path.abspath(os.path.join(__file__, "../../../"))
        aggregated_data_entity_path = os.path.join(base_dir, 'aggregated_data_entity', 'aggregated_data_entity.json')

        # Read the schema file that defines the structure for aggregated data (non-blocking)
        aggregated_data_entity_schema = await read_json_file(aggregated_data_entity_path)

        # Make API call to AI service to generate aggregated data report based on schema
        aggregated_data = await ai_service.ai_chat(
            token=meta["token"],
            chat_id= await get_trino_schema_id_by_entity_name("raw_data_entity"),
            ai_endpoint=TRINO_AI_API,
            ai_question=f"Could you please return json report based on this schema: {json.dumps(aggregated_data_entity_schema)}. Return only json"
        )

        # Parse and validate the returned JSON data (offload parsing if needed)
        aggregated_data_entity_data = json.loads(parse_json(aggregated_data))

        # Store the aggregated data entity and get its ID (non-blocking)
        aggregated_data_entity_id = await entity_service.add_item(
            meta["token"],
            "aggregated_data_entity",
            ENTITY_VERSION,
            aggregated_data_entity_data,
        )

        # Save the entity ID in the job dictionary
        data.setdefault("aggregated_data_entity", {})["technical_id"] = aggregated_data_entity_id

        logger.info("Aggregated data entity saved successfully.")
    except Exception as e:
        # Log any errors that occur during the aggregation process
        logger.error(f"Error in aggregate_raw_data: {e}")
        raise

async def generate_report_process(meta, data):
    logger.info("Starting process to generate and send report email.")
    try:

        aggregated_data_entity = await entity_service.get_item(
            meta["token"],
            "aggregated_data_entity",
            ENTITY_VERSION,
            data.get("aggregated_data_entity").get("technical_id"),
        )
        report_entity_data = {
            "report_id": "report_001",
            "generated_at": "2023-10-01T10:00:00Z",
            "report_title": "Monthly Data Analysis",
            "summary": aggregated_data_entity,
            "distribution_info": {},
        }
        # Save the report entity
        report_entity_id = await entity_service.add_item(
            meta["token"], "report_entity", ENTITY_VERSION, report_entity_data
        )
        logger.info(f"Report entity saved successfully: {report_entity_id}")
        logger.info(f"Sending email with report {report_entity_id}")
    except Exception as e:
        logger.error(f"Error in generate_and_send_report_email: {e}")
        raise


# Updated Test Classes with Mocks
class TestDataProcessingJob(unittest.TestCase):

    @patch("workflow.ingest_data")
    @patch("app_init.app_init.entity_service.add_item")  # Inner decorator
    def test_ingest_data_process(self, mock_entity_service, mock_ingest_raw_data):
        # Arrange
        mock_ingest_raw_data.return_value = [
            {
                "brpCode": "7080005051286",
                "brpName": "Example Name",
                "country": "FI",
                "businessId": "123456789",
                "codingScheme": "GS1",
                "validityStart": "2023-01-01",
                "validityEnd": "2025-01-01"
            }
        ]
        mock_entity_service.return_value = "raw_data_entity_id"

        meta = {"token": "test_token"}
        data = {
            "request_parameters": {
                "code": "7080005051286",
                "country": "FI",
                "name": ""
            }
        }

        # Act and await the async function
        asyncio.run(ingest_data_process(meta, data))

        # Assert
        mock_entity_service.assert_called_once_with(
            meta["token"],
            "raw_data_entity",
            ENTITY_VERSION,
            [
                {
                    "brpCode": "7080005051286",
                    "brpName": "Example Name",
                    "country": "FI",
                    "businessId": "123456789",
                    "codingScheme": "GS1",
                    "validityStart": "2023-01-01",
                    "validityEnd": "2025-01-01"
                }
            ]
        )


    @patch("app_init.app_init.entity_service.add_item")
    @patch("app_init.app_init.ai_service.ai_chat")
    @patch("common.service.trino_service.get_trino_schema_id_by_entity_name")
    def test_aggregate_raw_data(self, mock_get_trino_schema, mock_ai_chat, mock_entity_service):
        # Arrange
        mock_ai_chat.return_value = '{"aggregated_data": "dummy_aggregated_data"}'
        mock_entity_service.return_value = "aggregated_data_entity_id"
        mock_get_trino_schema.return_value = "response_data_entity_id"
        aggregated_data_entity_schema = {"schema": "dummy_schema"}

        # Mock read_json_file to return the dummy schema
        def mock_read_json_file(path):
            return aggregated_data_entity_schema

        # Mock parse_json to return the dummy JSON data
        def mock_parse_json(data):
            return data

        meta = {"token": "test_token"}
        data = {}

        # Act and await the async function
        asyncio.run(aggregate_raw_data(meta, data))


    @patch("app_init.app_init.entity_service.add_item")
    @patch("app_init.app_init.entity_service.get_item")
    def test_generate_report_process(self, mock_get_item, mock_entity_service):
        # Arrange
        mock_get_item.return_value = {"aggregated_data": "dummy_data"}
        mock_entity_service.return_value = "report_entity_id"
        meta = {"token": "test_token"}
        data = {"aggregated_data_entity": {"technical_id": "aggregated_data_entity_id"}}

        # Act and await the async function
        asyncio.run(generate_report_process(meta, data))

        # Assert
        mock_get_item.assert_called_once_with(
            meta["token"],
            "aggregated_data_entity",
            ENTITY_VERSION,
            "aggregated_data_entity_id"
        )
        mock_entity_service.assert_called_once_with(
            meta["token"],
            "report_entity",
            ENTITY_VERSION,
            {
                "report_id": "report_001",
                "generated_at": "2023-10-01T10:00:00Z",
                "report_title": "Monthly Data Analysis",
                "summary": {"aggregated_data": "dummy_data"},
                "distribution_info": {},
            }
        )


if __name__ == "__main__":
    unittest.main()
