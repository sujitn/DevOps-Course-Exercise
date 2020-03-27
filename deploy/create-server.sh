#!/bin/sh

# Create an EC2 instance using the standard Amazon Linux machine image and micro instance type (free tier eligible)
aws ec2 run-instances --image-id ami-0e49551fc78560451 --instance-type t2.micro --key-name MyKeyPair --security-groups EC2SecurityGroup

# Check the state of the new EC2 instance and wait until it is running
ec2_state=`aws ec2 describe-instances | jq --raw-output '.Reservations | .[-1] | .Instances | .[] | .State.Name'`
while [ $ec2_state != 'running' ]
do
	echo "Waiting for instance to start..."
    sleep 30
    ec2_state=`aws ec2 describe-instances | jq --raw-output '.Reservations | .[-1] | .Instances | .[] | .State.Name'`
done
echo "Instance is now running"

# Display the public DNS name for the new instance
ec2_hostname=`aws ec2 describe-instances | jq --raw-output '.Reservations | .[-1] | .Instances | .[] | .PublicDnsName'`
echo "Instance public DNS name: $ec2_hostname"
