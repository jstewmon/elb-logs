# elb-logs

elb-logs is a cli that makes downloading, parsing and filtering elb logs a cinch.

## Installation

##### requirements
- python 2.7
- pip >= 6.0

With virtualenv:

```
mkvirtualenv elb-logs && pip install git+git://github.com/jstewmon/elb-logs.git@master
```

## Commands

### base

##### options

```
Usage: elb-logs [OPTIONS] COMMAND [ARGS]...

Options:
  --profile TEXT
  --region TEXT
  --access-key TEXT
  --secret-key TEXT
  --help             Show this message and exit.

Commands:
  download
  filter
  parse
```

Notes:
- `--profile` is expected to be a boto/aws profile
    - It can be used to supply credentials and defaults for any command options.

### download
download elb log files from s3

##### options

```
Usage: elb-logs download [OPTIONS]

Options:
  --bucket TEXT       [required]
  --time-prefix TEXT  [required]
  --elb TEXT          [required]
  --output-dir TEXT
  --help              Show this message and exit.
```

Notes:
- the `--output-dir` default is `$(pwd)/<elb>/<time-prefix>`
- `--region` is required to be given on the base command

Example with `--region`, `--bucket` and `--elb` provided through boto config:

```
elb-logs --profile test download --time-prefix 20150613T100
```

### parse
parse the log lines and output json - one document out per line in.

```
elb-logs parse $(find s3-bucket-name/20150613T100/ -type f)
```

To sort log entries chronologically:

```
cat s3-bucket-name/20150613T100/* | sort | elb-logs parse -
```

Example output (formatted for readability):

```
{
  "_line": "2015-06-13T10:05:43.471617Z ec2-elb-name 10.1.2.1:43989 10.1.1.1:80 0.000055 0.293759 0.000063 200 200 0 2810 \"GET http://example.com:80/someUrl HTTP/1.1\" \"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36\" - -\n",
  "backend_processing_time": 0.293759,
  "received_bytes": 0,
  "elb": "ec2-elb-name",
  "timestamp": 1434189943,
  "request": "GET http://example.com:80/someUrl HTTP/1.1",
  "request_processing_time": 0.000055,
  "sent_bytes": 2810,
  "client": {
    "ip": "10.1.2.1",
    "port": 43989
  },
  "backend_status_code": 200,
  "elb_status_code": 200,
  "response_processing_time": 0.000063,
  "_file": "s3-elb-log-bucket/20150613T100/123456789098_elasticloadbalancing_us-west-1_ec2-elb-name_20150613T1005Z_54.0.0.0_G43XknE4.log",
  "backend": {
    "ip": "10.1.1.1",
    "port": 80
  }
}
```

### filter
Filter parsed output using [jmespath expressions](http://jmespath.org).

Each line of input is buffered into batches of 1000 items, so that list filters can be used to efficiently filter
the output.

The output is always json, but can be any the result of any jmespath projection.

##### options

```
Usage: elb-logs filter [OPTIONS] [INPUT_FILES]...

Options:
  --expression TEXT  [required]
  --help             Show this message and exit.
```

Example of finding all requests with a 5XX status code:

```
cat s3-bucket-name/20150613T100/* \
    | sort \
    | elb-logs parse - \
    | elb-logs filter --expression '[?elb_status_code > `499`]' -
```

## Configuration
Command options may be provided by a boto profile. This can be very convenient for frequently used option combinations,
especially when they coincide with an existing profile.

Example:

```
$ cat ~/.aws/config
[prod]
aws_access_key_id=XXXXXXXX
aws_secret_access_key=XXXXXX
ELB_LOGS_DOWNLOAD_BUCKET=s3-elb-log-bucket
ELB_LOGS_DOWNLOAD_ELB=ec2-elb-name
ELB_LOGS_REGION=us-west-1
```
