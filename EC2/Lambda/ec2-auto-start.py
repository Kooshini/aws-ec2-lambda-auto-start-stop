import boto3
import logging

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#define the connection
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    # filter all instances, ensure the AutoOnOff tag is present, the instance is stopped and the training VPC to prevent accidents
    filters = [{
            'Name': 'tag:AutoOnOff',
            'Values': ['True']
        },
        {
            'Name': 'instance-state-name',
            'Values': ['stopped']
        },
           {
            'Name': 'vpc-id',
            'Values': ['vpc-58a2673c']
        }
    ]

    #filter the instances
    instances = ec2.instances.filter(Filters=filters)

    #locate all running instances
    StoppedInstances = [instance.id for instance in instances]

    #make sure there are actually instances to shut down.
    if len(StoppedInstances) > 0:
        #perform the shutdown
        startingInstances = ec2.instances.filter(InstanceIds=StoppedInstances).start()
        print startingInstances
    else:
        print "No stopped instances that match the filters can be found"

