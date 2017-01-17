# aws-tools

Some helpful scripts when interacting with the AWS cloud.

## aws-inventory.py

Generate config files from your AWS inventory with Jinja2 templates. 
There is an example template for creating an icinga2 hosts file provided. Take a look at `hosts.j2.dist`.

### Dependencies

* Python 2.7
* Boto 2
* Jinja 2

### Usage
```
./aws-inventory.py --help
usage: aws-inventory.py [-h] [--template TEMPLATE] [--aws-region AWS_REGION]
                        OUTPUT_FILE

Generate a hosts file from AWS.

positional arguments:
  OUTPUT_FILE           The path to the generated hosts file

optional arguments:
  -h, --help            show this help message and exit
  --template TEMPLATE   The path to the jinja2 template
  --aws-region AWS_REGION
                        The AWS Region. Defaults to eu-central-1
```

## License

All scripts are released under the terms of the GPL 3.0.