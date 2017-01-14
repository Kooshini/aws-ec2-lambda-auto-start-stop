import boto3
import logging

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#define the connection
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    # filter all instances, ensure the AutoOnOff tag is present, the instance is running and the training VPC to prevent accidents
    filters = [{
            'Name': 'tag:AutoOnOff',
            'Values': ['True']
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        },
           {
            'Name': 'vpc-id',
            'Values': ['vpc-58a2673c']
        }
    ]

    #filter the instances
    instances = ec2.instances.filter(Filters=filters)

    #locate all running instances
    RunningInstances = [instance.id for instance in instances]

    #make sure there are actually instances to shut down.
    if len(RunningInstances) > 0:
        #perform the shutdown
        shuttingDown = ec2.instances.filter(InstanceIds=RunningInstances).stop()
        print shuttingDown
    else:
        print "No running instances that match the filters can be found"

