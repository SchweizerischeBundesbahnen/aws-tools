#!/usr/bin/env python2

# Author:       Simon Erhardt <simon.erhardt@sbb.ch>
# Purpose:      auto-generate hosts inventory via jinja2
# Dependencies: boto (2.43+), jinja2

from __future__ import print_function
import boto.ec2
import boto.ec2.cloudwatch
import jinja2
import os
import argparse


def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)

parser = argparse.ArgumentParser(description='Generates a file with jinja2 from your AWS inventory.')

parser.add_argument('OUTPUT_FILE', type=str,
                    help="The path to the generated file")

parser.add_argument('--template', type=str, default="host.j2",
                    help="The path to the jinja2 template")

parser.add_argument('--aws-region', type=str, default="eu-central-1",
                    help="The AWS Region. Defaults to eu-central-1")

args = parser.parse_args()

connEC2 = boto.ec2.connect_to_region(args.aws_region)
instances = connEC2.get_all_instances()


connCW = boto.ec2.cloudwatch.connect_to_region(args.aws_region)

inventory = []
for i in instances:
    instance = {
        'id': i.instances[0].id,
        'local_ip': i.instances[0].private_ip_address,
        'tags': i.instances[0].tags,
        'state': i.instances[0].state,
        'metrics': []
    }

    if 'Name' not in i.instances[0].tags:
        print("WARNING! " + instance['id'] + " has no name.")
        continue

    instance['name'] = i.instances[0].tags['Name']

    metrics = connCW.list_metrics(dimensions={
        "InstanceId": instance['id']
    })

    for metric in metrics:
        instance['metrics'].append(metric)

    inventory.append(instance)

f = open(args.OUTPUT_FILE, 'w')

context = {
    "hosts": inventory
}
ret = render(args.template, context)
ret = filter(lambda x: not re.match(r'^\s*$', x), ret)

f.write(ret + "\n")
f.close()

exit(0)
