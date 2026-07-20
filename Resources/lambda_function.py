import os
import boto3

tagging_client = boto3.client('resourcegroupstaggingapi')
sns_client = boto3.client('sns')

SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def get_resource_name(tags):
    """Helper to extract the 'Name' tag if it exists."""
    for tag in tags:
        if tag['Key'].lower() == 'name':
            return tag['Value']
    return "N/A"

def lambda_handler(event, context):
    try:
        # 1. Fetch all tagged resources
        response = tagging_client.get_resources()
        resources = response.get('ResourceTagMappingList', [])
        
        while 'PaginationToken' in response and response['PaginationToken']:
            response = tagging_client.get_resources(PaginationToken=response['PaginationToken'])
            resources.extend(response.get('ResourceTagMappingList', []))
            
        total_count = len(resources)
        
        # 2. Group resources by service type with details
        service_groups = {}
        for res in resources:
            arn = res['ResourceARN']
            tags = res.get('Tags', [])
            resource_name = get_resource_name(tags)
            
            # Extract Service and Resource Type from ARN
            # ARN Format: arn:aws:service:region:account-id:resource-type/resource-id
            arn_parts = arn.split(':')
            service = arn_parts[2].upper() if len(arn_parts) > 2 else "UNKNOWN"
            resource_id_part = arn_parts[-1]
            
            if service not in service_groups:
                service_groups[service] = []
                
            service_groups[service].append({
                'name': resource_name,
                'arn': arn,
                'resource_id': resource_id_part
            })

        # 3. Build Detailed Email Message
        message_lines = [
            "==================================================",
            "          AWS RESOURCE DETAIL REPORT              ",
            "==================================================",
            f"Total Resources Found: {total_count}\n",
        ]
        
        for service, items in service_groups.items():
            message_lines.append(f"▶ {service} ({len(items)} resource/s):")
            message_lines.append("-" * 50)
            
            for item in items:
                message_lines.append(f"  • Name: {item['name']}")
                message_lines.append(f"    ID / Path: {item['resource_id']}")
                message_lines.append(f"    ARN: {item['arn']}")
                message_lines.append("")  # Empty line for spacing
            
            message_lines.append("")

        full_message = "\n".join(message_lines)

        # 4. Publish to SNS
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"AWS Resource Details Report - ({total_count} Resources)",
            Message=full_message
        )
        
        return {
            'statusCode': 200,
            'body': f"Report successfully sent for {total_count} resources."
        }
        
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        raise e