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
            'Values': ['running']
        },
           {
            'Name': 'vpc-id',
            'Values': [os.environ['VPC_ID']]
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

    #disable the auto scale
    autoscale.suspend_processes(AutoScalingGroupName=os.environ['AUTOSCALING_GROUP_NAME'],ScalingProcesses=[],)
