import os
import boto3

# Initialize AWS SDK clients
tagging_client = boto3.client('resourcegroupstaggingapi')
sns_client = boto3.client('sns')

SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    try:
        # Get all resources in the current region
        response = tagging_client.get_resources()
        resources = response.get('ResourceTagMappingList', [])
        
        # Paginate if there are more than 100 resources
        while 'PaginationToken' in response and response['PaginationToken']:
            response = tagging_client.get_resources(PaginationToken=response['PaginationToken'])
            resources.extend(response.get('ResourceTagMappingList', []))
            
        total_count = len(resources)
        
        # Categorize resources by service type (e.g., ec2, s3, lambda)
        service_counts = {}
        for res in resources:
            arn = res['ResourceARN']
            service = arn.split(':')[2]  # Extract service name from ARN
            service_counts[service] = service_counts.get(service, 0) + 1

        # Format message body
        breakdown_str = "\n".join([f"  - {svc.upper()}: {count}" for svc, count in service_counts.items()])
        message = (
            f"AWS Resource Count Report\n"
            f"===========================\n\n"
            f"Total Active Resources Discovered: {total_count}\n\n"
            f"Breakdown by Service:\n{breakdown_str}\n"
        )
        
        # Send Email via SNS
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="AWS Account Resource Count Report",
            Message=message
        )
        
        return {
            'statusCode': 200,
            'body': f"Successfully sent email report for {total_count} resources."
        }
        
    except Exception as e:
        print(f"Error executing report: {str(e)}")
        raise e