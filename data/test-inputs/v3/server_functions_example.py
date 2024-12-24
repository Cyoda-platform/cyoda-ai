import json
from common.repository.crud_repository import CrudRepository
from common.repository.cyoda.cyoda_repository import CyodaRepository

repository: CrudRepository = CyodaRepository()

def lock_for_review(meta, data):

    try:
        data['status'] = "under_review"
        repository.update_all(meta, [data])

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Application approved successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Function to approve an application
def reject_application(meta, data):
    try:
        data['status'] = "rejected"
        repository.update_all(meta, [data])

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Application approved successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Function to approve an application
def approve_application(meta, data):
    try:
        data['status'] = "under_review"
        repository.update_all(meta, [data])

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Application approved successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Function to approve an application
def withdraw_application(meta, data):
    try:
        data['status'] = "withdrawn"
        repository.update_all(meta, [data])

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Application approved successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }