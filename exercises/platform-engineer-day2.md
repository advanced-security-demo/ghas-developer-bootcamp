# GHAS for platform engineerrs

## Overview

- [ ] [Excercise 5 - Run tool Checkov in PR and integrate in Code Scanning](#exercise-5---run-tool-checkov-in-pr-and-integrate-in-code-scanning-15-mins)
  - [ ] [Extra: Integrate Secret Scanning alerts in PR](#extra-integrate-secret-scanning-alerts-in-pr)
- [ ] [Excercise 6 - Catch and alert on Push Protection bypasses](#exercise-6---catch-and-alert-on-push-protection-bypasses-15-mins)
- [ ] [Excercise 7 - Report on Code Scanning alerts that got dismissed](#exercise-7---report-on-code-scanning-alerts-that-got-dismissed-15-mins)
- [ ] [Excercise 8 - Investigate deactivation activity of GHAS in audit log](#exercise-8---investigate-deactivation-activity-of-ghas-in-audit-log-15-mins)
- [ ] [Excercise 9 - Generate CodeQL debug and identify a problem](#exercise-9---generate-codeql-debug-and-identify-a-problem-15-mins)

## Integrations - GHAS API and Webhooks

### Exercise 5 - Run tool Checkov in PR and integrate in Code Scanning (15 mins)

In this excercise we will integrate another security testing tool results into Code Scanning. The choice of a tool is Checkov. 

### Create a new workflow

You need to create a new workflow file that will do the analysis. To do this you can navigate to the `Actions` tab of your repository and select `New workflow`. You will be presented with a list of templates.
We will not be using already existing workflow on the marketplace in this excercises, so you will need to select `Skip this and set up a workflow yourself`. 

Navigate to [bridgecrewio/checkov-action](https://github.com/bridgecrewio/checkov-action) and copy the example config. Rename the workflow file to `checkov.yml` and paste the content into the editor and commit the file to your repository.

<details>
<summary>Solution</summary>

```yaml
name: checkov

# Controls when the workflow will run
on:
  # Triggers the workflow on push or pull request events but only for the "main" branch
  push:
    branches: [ "main", "master" ]
  pull_request:
    branches: [ "main", "master" ]

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "scan"
  scan:
    permissions:
      contents: read # for actions/checkout to fetch code
      security-events: write # for github/codeql-action/upload-sarif to upload SARIF results
      actions: read # only required for a private repository by github/codeql-action/upload-sarif to get the Action run status
      
    # The type of runner that the job will run on
    runs-on: ubuntu-latest

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so follow-up steps can access it
      - uses: actions/checkout@v3

      - name: Checkov GitHub Action
        uses: bridgecrewio/checkov-action@v12
        with:
          # This will add both a CLI output to the console and create a results.sarif file
          output_format: cli,sarif
          output_file_path: console,results.sarif
        
      - name: Upload SARIF file
        uses: github/codeql-action/upload-sarif@v2
        
        # Results are generated only on a success or failure
        # this is required since GitHub by default won't run the next step
        # when the previous one has failed. Security checks that do not pass will 'fail'.
        # An alternative is to add `continue-on-error: true` to the previous step
        # Or 'soft_fail: true' to checkov.
        if: success() || failure()
        with:
          sarif_file: results.sarif
```
</details>

After committing the file you should see a new workflow running in the `Actions` tab. 

### Trigger a new checkov run

To trigger a new checkov run you can create a new branch and edit the `terraform/aws/lambda.tf` file and add the following snippet:

```terraform
resource "aws_iam_role" "iam_for_lambda" {
  name = "${local.resource_prefix.value}-analysis-lambda"


  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
  tags = {
    git_commit           = "e6d83b21346fe85d4fe28b16c0b2f1e0662eb1d7"
    git_file             = "terraform/aws/lambda.tf"
    git_last_modified_at = "2023-04-27 12:47:51"
    git_last_modified_by = "nadler@paloaltonetworks.com"
    git_modifiers        = "nadler/nimrodkor"
    git_org              = "bridgecrewio"
    git_repo             = "terragoat"
    yor_trace            = "93cfa6f9-a257-40c3-b7dc-3c3686929734"
  }
}

resource "aws_lambda_function" "analysis_lambda" {
  # lambda have plain text secrets in environment variables
  filename      = "resources/lambda_function_payload.zip"
  function_name = "${local.resource_prefix.value}-analysis"
  role          = "${aws_iam_role.iam_for_lambda.arn}"
  handler       = "exports.test"

  source_code_hash = "${filebase64sha256("resources/lambda_function_payload.zip")}"

  runtime = "nodejs13.x"

  environment {
    variables = {
      access_key = "AKIAIOSFODNN7EXAMPLE"
      secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    }
  }
  tags = {
    git_commit           = "5c6b5d60a8aa63a5d37e60f15185d13a967f0542"
    git_file             = "terraform/aws/lambda.tf"
    git_last_modified_at = "2021-05-02 10:06:10"
    git_last_modified_by = "nimrodkor@users.noreply.github.com"
    git_modifiers        = "nimrodkor"
    git_org              = "bridgecrewio"
    git_repo             = "terragoat"
    yor_trace            = "f7d8bc47-e5d9-4b09-9d8f-e7b9724d826e"
  }
}
```

Next, go ahead and raise a PR against the default branch and check if that will trigger an analysis.

---

### Extra: Integrate Secret Scanning alerts in PR

### Create a new workflow

Following the same steps create a new workflow file that will run the [advanced-security/secret-scanning-review-action](https://github.com/advanced-security/secret-scanning-review-action) action.

As also pointed out in the `README` of the `advanced-security/secret-scanning-review-action` you will have to create a new GitHub token with the `repo` scope and add it as a secret to your repository with a name `SECRET_SCAN_REVIEW_GITHUB_TOKEN`.

<details>
<summary>Solution</summary>

```yaml
name: 'Secret Scanning Review'
on: [pull_request]

jobs:
  secret-scanning-review:
    runs-on: ubuntu-latest
    steps:
      - name: 'Secret Scanning Review Action'
        uses: advanced-security/secret-scanning-review-action@v0
        with:
          token: ${{ secrets.SECRET_SCAN_REVIEW_GITHUB_TOKEN }}
          fail-on-alert: true
          fail-on-alert-exclude-closed: true
```
</details>

### Trigger an action run in PR

To trigger a new checkov run you can create a new branch and edit the `authn-service/.env` file and add the following secret `STRIPE_DEV="sk_live_devboxbcct1DfwS2ClCIKlbT"`
Since you have Push Protection enabled go ahead and by pass it with `I'll fix it later` reason.

Raise a PR and check if that will trigger an analysis and observe the results.

### Exercise 6 - Catch and alert on Push Protection bypasses (15 mins)

### Setting up the local envrionment

If you haven't done it so far, go ahead and pull your training repository to your local machine.

- Setup python virtual environment and install the requirements

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Install [ngrok](https://ngrok.com/download) and setup a tunnel

### Create a new webhook

- Visit the organization or repository on GitHub that you wish to set the webhook up for, and follow the [Setting up a webhook](https://docs.github.com/en/developers/webhooks-and-events/webhooks/creating-webhooks#setting-up-a-webhook) instructions.
- Choose the `application/json` content type
- Configure the events by choosing "Let me select individual events", and deselect the "Push" event and instead select the "Code Scanning alerts" event
- Run `python3 generic_wh.py`, and trigger an event from your repository (For example: close a code scanning alert)

Using the information from the [secret_scanning_alert docs](https://docs.github.com/en/enterprise-cloud@latest/webhooks/webhook-events-and-payloads#secret_scanning_alert) adapt the python code to catch the `secret_scanning_alert` and print an alert message to the console.

#### Exercise 7 - Report on Code Scanning alerts that got dismissed (15 mins)

Following the similar steps as in the previous exercise, create a new webhook that will catch the `code_scanning_alert` event and change the `alerts_closed.py` to trigger when a critical code scanning alert is dismissed and print an alert message to the console.

<details> 
<summary>Solution</summary>

```python
def foo():
    data = json.loads(request.data)
    print(json.dumps(data, indent=4, sort_keys=True))
    if data["action"] == "closed_by_user" and data['alert']['rule']['security_severity_level'] == "critical":
        print(f"WARNING: A developer dismissed a critical alert for reason: { data['alert']['dismissed_reason'] }.")
    return "OK"
```
</details>

---

### Troubleshooting GHAS

### Exercise 8 - Investigate deactivation activity of GHAS in audit log (15 mins)

In the past two days you have made some changes to your repository - enabled GHAS, added a custom secret scanning pattern, enabled push protection, closed alerts, etc. With this excercise we want to get familiar with how the audit log can help us troubleshoot issues or understand what happened in the past in regards to GHAS.

We will use the audit log to answer questions about the actions that have been performed in our organization. Access the audit log by going to the `Settings` of your organization and selecting `Logs -> Audit log` from the left menu.

You can use the UI to search through the events. Using the information from the [official documentation](https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization) can you find the answers to the following questions:

1. How many times was GHAS enabled in your repository?
2. How many times was GHAS disabled in your repository?
3. How many times have you bypassed push protection?
4. Who has disabled `repository_secret_scanning_push_protection` in your repository?

<details>
<summary>Solution</summary>

1. How many times was GHAS enabled in your repository?

    - Search for `action:repo.advanced_security_enabled repo:org/your-repo-name`

2. How many times was GHAS disabled in your repository?

    - Search for `action:repo.advanced_security_disabled repo:org/your-repo-name`

3. How many times have you bypassed push protection?

    - Search for `action:secret_scanning_push_protection.bypass actor:your-github-username`

4. Who has disabled `repository_secret_scanning_push_protection` in your repository?

    - Search for `action:repository_secret_scanning_push_protection.enable`

</details>

---

### Exercise 9 - Generate CodeQL debug and identify a problem (15 mins)

In this exercise we will generate look at options for you to debug a Code Scanning - CodeQL debug analysis run. We will generate a CodeQL Code Scanning debug run file and understand the structure of a debug artifact, then we will also look at few debug artifacts to identify the problems and last how we can use the `Tool Status` to understand the status of the CodeQL analysis.

### Enabling CodeQL Debug mode

First navigate to the Actions tab on your repository and select the `CodeQL` workflow.

You can re-run a CodeQL analysis in debug mode by selecting a CodeQL analysis workflo run, then clicking `Re-run all jobs` in the top right of the page and selecting `Enable debug logging` before hitting the  `Re-run jobs` button. This will trigger a new CodeQL analysis run after which and the debug data will be uploaded as Actions artifact. After the run has completed you should see a list of artifacts  `debug-artifacts-*`. Go ahead and download the `debug-artifacts-java`.

The other option to enabled CodeQL debug mode in the Action is by providing `debug: true` configuration option. This is useful when you want to enabled debug mode for a workflow where you expect it to fail and you don't want to wait for it to finish before re-runnning it in debug mode.
The end result is the same.

### Understanding the debug artifact

The debug artifact is a zip file that contains a number of files and directories. The most important ones are:

- `java/log/`
  - `ext/*` - directory containing the CodeQL extractor configuration, envrionment variables, etc
  - `log/databbase-*` - files containing logs from the CodeQL database related operations - creation, initialization, etc
  - `log/javac-*` - files containing logs from the compilation and extrator process
- `log` - logs from the build tracker and database initializaiton
- `java.sarif` - the results of the analysis in SARIF format
- `db-java.zip` - the CodeQL database that was created and used for the analysis. This is the most important file as it contains all the information about the analysis. Beaware when sharing this archive as it also contains the source code of your repository.

### Investigating the CodeQL debug artifact

In this exercise we will look at few debug artifacts and try to identify the problem.

Go ahead and download the debug artifacts from the following link: [code-debug-artifactsjava](https://gh.io/ghas-training-debug-artifacts)

Using the artifact provided can you answer the following questions:

- Which CodeQL CLI version was used for the analysis?
- What type of codebase was the analysis ran on?
- Was the analysis completed successfully? If not, what was the reason?
- Can you identified which CodeQL queries were configured for this analysis?

Hint: look into the `db-cpp-partial.zip` file
<details>
<summary>Solution</summary>
- Which CodeQL CLI version was used for the analysis?
    - `CodeQL CLI version: 2.15.1`
- What type of codebase was the analysis ran on?
    - `C or Cpp` as can be guess from the filename but also the extractor used, or the `codeql-database.yml` file
- Was the analysis completed successfully? If not, what was the reason?
    - No, the analysis failed because `No supported build system detected` as it can be seen in the extractor diagnostic message.
    - Digging further in, we can also see that there were indeed empty source directory without code or build systems.
- The files `config-queries.qls` give us the list of queries that were configured for this analysis.
</details>

### Using Tool Status

In the `Security` tab of your repository, under Code Scanning, you have a section called `Tool status`. This is a good place to check if there are any issues with the CodeQL analysis as well as find information about the CodeQL version used for the analysis, CodeQL queries used, etc.

Navigate to the `Tool status` section and answer the following questions:

- Which CodeQL CLI version was used for the analysis?
- Which Query Suite was used for the analysis for the last analysis of the Java codebase?
- How many rules were ran in the last analysis of the Python codebase?
- Where all the files from the Go component `gallery-service` scanned?
