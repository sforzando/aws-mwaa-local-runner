# aws-mwaa-local-runner

[![Sync](https://github.com/sforzando/aws-mwaa-local-runner/actions/workflows/sync.yml/badge.svg)](https://github.com/sforzando/aws-mwaa-local-runner/actions/workflows/sync.yml)
[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

- [Prerequisites](#prerequisites)
- [How to](#how-to)
  - [Setup](#setup)
  - [Start](#start)
  - [Airflow UI](#airflow-ui)
  - [Requirements.txt](#requirementstxt)
  - [Plugins](#plugins)
  - [Startup Scripts](#startup-scripts)
- [What's NEXT?](#whats-next)
- [FAQs](#faqs)
  - [Can I test execution role permissions using this repository?](#can-i-test-execution-role-permissions-using-this-repository)
  - [How do I add libraries to requirements.txt and test install?](#how-do-i-add-libraries-to-requirementstxt-and-test-install)
  - [What if a library is not available on PyPi.org?](#what-if-a-library-is-not-available-on-pypiorg)
  - [My environment is not starting](#my-environment-is-not-starting)
  - [Fernet Key InvalidToken](#fernet-key-invalidtoken)
- [Security](#security)
- [License](#license)

## Prerequisites

- Docker
  - Python (Version 3.10 or higher)
- [pre-commit](https://pre-commit.com)
- [Ruff](https://beta.ruff.rs/docs/)
- [hadolint](https://github.com/hadolint/hadolint)

## How to

```shell
default              常用
setup                初期
hide                 秘匿
reveal               暴露
open                 閲覧
build                構築
start                開始
check                検証
test                 試験
doc                  文書
clean                掃除
prune                破滅
help                 助言
```

### Setup

```shell
make setup
```

### Start

```shell
make start
```

To stop the local environment, Ctrl+C on the terminal and wait till the local runner and the postgres containers are stopped.

### Airflow UI

Open the Apache Airflow UI: [http://0.0.0.0:8080](http://0.0.0.0:8080)

By default, the `bootstrap.sh` script creates a username and password for your local Airflow environment.

- Username: `admin`
- Password: `test`

### Requirements.txt

1. Add Python dependencies to `requirements/requirements.txt`.
2. To test a requirements.txt without running Apache Airflow, use the following script:

```shell
./mwaa-local-env test-requirements
```

Let's say you add `aws-batch==0.6` to your `requirements/requirements.txt` file. You should see an output similar to:

```shell
Installing requirements.txt
Collecting aws-batch (from -r /usr/local/airflow/dags/requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/5d/11/3aedc6e150d2df6f3d422d7107ac9eba5b50261cf57ab813bb00d8299a34/aws_batch-0.6.tar.gz
Collecting awscli (from aws-batch->-r /usr/local/airflow/dags/requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/07/4a/d054884c2ef4eb3c237e1f4007d3ece5c46e286e4258288f0116724af009/awscli-1.19.21-py2.py3-none-any.whl (3.6MB)
    100% |████████████████████████████████| 3.6MB 365kB/s
...
...
...
Installing collected packages: botocore, docutils, pyasn1, rsa, awscli, aws-batch
  Running setup.py install for aws-batch ... done
Successfully installed aws-batch-0.6 awscli-1.19.21 botocore-1.20.21 docutils-0.15.2 pyasn1-0.4.8 rsa-4.7.2
```

3. To package the necessary WHL files for your requirements.txt without running Apache Airflow, use the following script:

```shell
./mwaa-local-env package-requirements
```

For example usage see [Installing Python dependencies using PyPi.org Requirements File Format Option two: Python wheels (.whl)](https://docs.aws.amazon.com/mwaa/latest/userguide/best-practices-dependencies.html#best-practices-dependencies-python-wheels).

### Plugins

- There is a directory at the root of this repository called plugins.
- In this directory, create a file for your new custom plugin.
- Add any Python dependencies to `requirements/requirements.txt`.

**Note**: this step assumes you have a DAG that corresponds to the custom plugin. For example usage [MWAA Code Examples](https://docs.aws.amazon.com/mwaa/latest/userguide/sample-code.html).

### Startup Scripts

- There is a sample shell script `startup.sh` located in a directory at the root of this repository called `startup_script`.
- If there is a need to run additional setup (e.g. install system libraries, setting up environment variables), please modify the `startup.sh` script.
- To test a `startup.sh` without running Apache Airflow, use the following script:

```shell
./mwaa-local-env test-startup-script
```

## What's NEXT?

- Learn how to upload the requirements.txt file to your Amazon S3 bucket in [Installing Python dependencies](https://docs.aws.amazon.com/mwaa/latest/userguide/working-dags-dependencies.html).
- Learn how to upload the DAG code to the dags folder in your Amazon S3 bucket in [Adding or updating DAGs](https://docs.aws.amazon.com/mwaa/latest/userguide/configuring-dag-folder.html).
- Learn more about how to upload the plugins.zip file to your Amazon S3 bucket in [Installing custom plugins](https://docs.aws.amazon.com/mwaa/latest/userguide/configuring-dag-import-plugins.html).

## FAQs

The following section contains common questions and answers you may encounter when using your Docker container image.

### Can I test execution role permissions using this repository?

- You can setup the local Airflow's boto with the intended execution role to test your DAGs with AWS operators before uploading to your Amazon S3 bucket. To setup aws connection for Airflow locally see [Airflow | AWS Connection](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html)
To learn more, see [Amazon MWAA Execution Role](https://docs.aws.amazon.com/mwaa/latest/userguide/mwaa-create-role.html).
- You can set AWS credentials via environment variables set in the `docker/config/.env.localrunner` env file. To learn more about AWS environment variables, see [Environment variables to configure the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html) and [Using temporary security credentials with the AWS CLI](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html#using-temp-creds-sdk-cli). Simply set the relevant environment variables in `.env.localrunner` and `./mwaa-local-env start`.

### How do I add libraries to requirements.txt and test install?

- A `requirements.txt` file is included in the `/requirements` folder of your local Docker container image. We recommend adding libraries to this file, and running locally.

### What if a library is not available on PyPi.org?

- If a library is not available in the Python Package Index (PyPi.org), add the `--index-url` flag to the package in your `requirements/requirements.txt` file. To learn more, see [Managing Python dependencies in requirements.txt](https://docs.aws.amazon.com/mwaa/latest/userguide/best-practices-dependencies.html).

### My environment is not starting

- If you encountered [the following error](https://issues.apache.org/jira/browse/AIRFLOW-3678): `process fails with "dag_stats_table already exists"`, you'll need to reset your database using the following command:

```bash
./mwaa-local-env reset-db
```

- If you are moving from an older version of local-runner you may need to run the above reset-db command, or delete your `./db-data` folder. Note, too, that newer Airflow versions have newer provider packages, which may require updating your DAG code.

### Fernet Key InvalidToken

A Fernet Key is generated during image build (`./mwaa-local-env build-image`) and is durable throughout all
containers started from that image. This key is used to [encrypt connection passwords in the Airflow DB](https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/fernet.html).
If changes are made to the image and it is rebuilt, you may get a new key that will not match the key used when
the Airflow DB was initialized, in this case you will need to reset the DB (`./mwaa-local-env reset-db`).

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License.
