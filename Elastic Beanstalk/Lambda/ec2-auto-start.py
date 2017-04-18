########################
# Created by Chris Cooke
# Last Updated: 18/04/2017
#
# Required Env Vars:
# VPC_ID
# AUTOSCALING_GROUP_NAME
# ELASTICBEANSTALK_ENVIRONMENT_ID
########################

import os
import boto3
import logging

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#define the connections
ec2 = boto3.resource('ec2')
autoscale = boto3.client('autoscaling')

def lambda_handler(event, context):
    # filter all instances by environment-id, status and vpc-id
    filters = [{
            'Name': 'tag:elasticbeanstalk:environment-id',
            'Values': [os.environ['ELASTICBEANSTALK_ENVIRONMENT_ID']]
        },
        {
            'Name': 'instance-state-name',
            'Values': ['stopped']
        },
           {
            'Name': 'vpc-id',
            'Values': [os.environ['VPC_ID']]
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

    #enable the auto scale and capacity
    autoscale.resume_processes(AutoScalingGroupName=os.environ['AUTOSCALING_GROUP_NAME'],ScalingProcesses=[],)
    autoscale.set_desired_capacity(AutoScalingGroupName=os.environ['AUTOSCALING_GROUP_NAME'],DesiredCapacity=1,HonorCooldown=True,)
