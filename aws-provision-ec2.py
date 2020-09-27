import boto3
import os
import time

# my 'boto3-ec2-user' IAM user with Programmatic access
settings = {
    'aws_access_key_id': 'XXXXXXXXXXXXXXXXXXXX',
    'aws_secret_access_key': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'myregion': 'us-east-2'
}

# create session and get ec2 resource
session = boto3.Session(
    aws_access_key_id = settings['aws_access_key_id'],
    aws_secret_access_key = settings['aws_secret_access_key'],
    region_name=settings['myregion']
)
ec2 = session.resource('ec2')
ec2client = session.client('ec2') # also create session for the low-level Clients API, I needed it for describe_instances()


#check if privkey was already saved to the disk
if os.path.isfile('boto3-ec2-keypair.pem'):
    with open('boto3-ec2-keypair.pem', 'r') as f:
        keypair_str = f.read()
else:
    # create a keypair that will allow us to access instance/vm after it is provisioned
    keypair = ec2.create_key_pair(KeyName='boto3-ec2-keypair')
    outfile = open('boto3-ec2-keypair.pem', 'w')

    # capture the key and store it in a file
    keypair_str = str(keypair.key_material)
    print('generated keypair:\n{0}'.format(keypair_str))
    outfile.write(keypair_str) # save privkey so it can be used with 'ssh -i'
    outfile.close()

yaml_datadisk_dict = {
    'yaml_datadisk_device': "/dev/xvdb",
    'yaml_datadisk_size': "+5G",
    'yaml_datadisk_fs': "xfs",
    'yaml_datadisk_mountpoint': "/data",
}

# prepare EC2 User Data post install script that will parition the /dev/xvdb disk, create fs, and mount it
myuserdata = '''
sudo su
echo -e "o\\nY\\nn\\n1\\n\\n\\n\\nw\\nY\\n" | gdisk {yaml_datadisk_device}
mkfs.{yaml_datadisk_fs} {yaml_datadisk_device}1
mkdir -p {yaml_datadisk_mountpoint}
echo "{yaml_datadisk_device}1 {yaml_datadisk_mountpoint} {yaml_datadisk_fs} defaults 0 0" >> /etc/fstab
mount -a
'''.format(**yaml_datadisk_dict)


# create a new micro EC2 instance/vm with Amazon Linux 2 AMI image
instance = ec2.create_instances(
    BlockDeviceMappings = [
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {'VolumeSize': 9},
        },
        {
            'DeviceName': '/dev/xvdb',
            'Ebs': {'VolumeSize': 9},
        },
    ],
    ImageId = 'ami-0603cbe34fd08cb81',
    MinCount = 1,
    MaxCount = 1,
    InstanceType = 't2.micro',
    KeyName = 'boto3-ec2-keypair',
    UserData = myuserdata,
    TagSpecifications = [
        {
            'ResourceType' : 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'myBotoEC2micro'
                },
            ]
        }
    ],
)
# wait until instance's state changes to 'running'
ec2client.wait_until_running()

# wait until OS boots up, not ideal, could use Waiters but they are in the other 'Clients' API
while instance[0].state == 'pending':
    time.sleep(3)
    instance[0].update()
print("instance id: {0}".format(instance[0].id))

# aws ec2 describe-instances --filters Name=tag:Name,Values=myBotoEC2micro --query 'Reservations[*].Instances[*].InstanceId' --output text
res = ec2client.describe_instances(
    Filters=[
        {
        'Name': 'tag:Name',
        'Values': ['myBotoEC2micro']
        }
    ]
) 
instanceID = res['Reservations'][0]['Instances'][0]['InstanceId']
print("again instance id is: {0}".format(instanceID))

# boto3 API can only check if the volume is attached to an instance, but not if it is mounted
# our volume that will hold /data was already attached in ec2.create_instances() step
# we will use EC2 User Data to format the /dev/xvdb volume with xfs filesystem & mount it at /data

# the catch is that EC2 User Data can be only used once during creation/launch of new instance/vm,
# so you need to feed it to ec2.create_instances()

# get domain name of newly launched instance
publicDNS = res['Reservations'][0]['Instances'][0]['PublicDnsName']
print("Login to new instance using:\n" \
    "ssh -i {0} e2c-user@{1}".format('boto3-ec2-keypair.pem', publicDNS))


#for i in ec2.instances.all():
#    print(i.id)
