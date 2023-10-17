# GHAS for platform engineerrs

## Overview

## Day 1

### GHAS Enablement

#### Exercise 1 - Enabling GHAS on your repository (10 minutes)

#### Enabling Dependabot alerts

Dependabot can be enabled in the settings of an organization or a repository.

- Go to the repository settings and enable Dependabot alerts in the `Code security and analysis` section. You will be prompted to enable the dependency graph if it's not enabled already.

#### Reviewing the dependency graph

Dependabot uses the dependency graph to determine which dependencies are used by your project.

- Verify in the dependency graph that it found dependencies for:
    - The frontend service.
    - The authentication service.
    - The gallery service.
    - The storage service.

The dependency graph can be accessed from the `Insights` tab in your repository.

#### Viewing and managing results

After a few minutes, the `Security` tab in the repository will indicate that there are new security alerts. You will see a **Create a security update** button; click this button to create a pull request (PR) to update the vulnerable dependency. The next section will show you how to enable security updates for all applicable Dependabot alerts.

**Note**: If this not the case, we can trigger an analysis by updating `authn-service/requirements.txt`

1. Go to the Dependabot alert section to view the detected dependency issues.

For each dependency alert, we have the option to create a security update or to dismiss the alert with a reason.

2. For one of the alerts, create a dependency security update. If Dependabot can update the dependency automatically, it will create a PR.

3. For one of the alerts, dimiss the alert.

#### Enabling Dependabot security updates

Dependabot can automatically create PRs to upgrade vulnerable dependencies to non-vulnerable versions. Please note that there may be some Dependabot alerts that don't have patches. In those cases, a security update is not available.

- Go to the repository settings and enable Dependabot security updates in the *Code security & analysis* section.

After a few minutes multiple PRs will be created that will upgrade vulnerable dependencies.

#### Enabling GitHub Adanced security

##### Repo Level

Up until now GHAS licenses were not consumed. Let's go to enabling GitHub Advanced Security now. Navigate back to `Code security and analysis` section in the Settings of your repository. 

You will notice the `GitHub Advanced Security` section right under the Dependabot options which you already enabled. Go ahead and click on the `Enable` button. A modal will pop-up asking you to confirm the action. Click on `Enable GitHub Advanced Security` button to confirm the action. In the modal you will also notice information about how many licenses (GitHub Advanced Security seats) will be consumed. The number of seats consumed is equal to the number of active committers in your repository.

After enabling GitHub Advanced Security you will notice that the `Code scanning alerts` section has been expanded with more options. Before proceeding to those we want to explore the other ways how GitHub Advanced Security can be enabled.

For now we will disable GHAS by clicking the `Disable` button. (?)

##### Organization Level

Similar to the repository level, navigate to the `Code security and analysis` but on your Organization Settings page. You will notice almost the same view as on the repository level. Few noticable differences:

- You have the `Enable All` / `Disable All` button.
- Additional checkbox option `Automatically enable for new private and internal repositories`. This option will automatically enable GitHub Advanced Security for all new private and internal repositories created in your organization. Turning this feature is useful but it should be accompanied with GHAS license consideration.

NOTE: DO NOT click the `Enable All` button if you are organization admin. We will follow the repo level enablement in this workshop

##### IssueOps way (?)

In your organization the current way development teams to enable GitHub Advanced Security to their repositories is via the DevX portal. Let's go ahead and enable GitHub Advanced Security for our repository via the DevX portal.

You should see `Enable GHAS on GitHub Repositories` service on the DevX portal. Select it and follow the steps by selecting your training repository. Observe the progress and the final result.

After completion, navigate back to your training repository and check the `Code security and analysis` section. You will notice that GitHub Advanced Security is enabled.

### How does it work?

#### Exercise 2 - Secret Scanning and Push Protection (10 mins)

##### Enabling secret scanning

Secret scanning can be enabled in the settings of an organization or a repository. If Advanced Security is not enabled yet, then enable that first (same settings screen).

1. Go to the repository settings and enable secret scanning in the `Code security and analysis` section.

NOTE: Do not enable `Push protection`, yet.

##### Viewing and managing results

After a few minutes, the `Security` tab in the repository will indicate that there are new security alerts.

- Go to the `Secret scanning` section to view the detected secrets.

For each secret, look at the options to close it and determine which one is most suitable.

##### Introducing a test secret

When developing test cases, you might find that secrets are introduced that cannot be abused when disclosed. Secret scanning will still detect and alert on these secrets.

1. In the GitHub repository file explorer, create a test file that contains a test secret.
    - For example the file `storage-service/src/main/resources/application.dev.properties` with the secrets
        ```
        STRIPE_NEW="sk_live_devboxbcct1DfwS2ClCIKlzX"
        ```
2. Determine if the secret is detected when the file is stored.
3. How would you like to manage results from test files?

##### Excluding files from secret scanning
While we can close a detected secret as being used in a test, we can also configure secret scanning to exclude files from being scanned.

1. Create the file `.github/secret_scanning.yml` if it doesn't already exist.
2. Add a list of paths to exclude from secret scanning. You can use [filter patterns](https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet) to specify paths.
    ```yaml
    paths-ignore:
        - '**/test/**'
        - 'exercises/**'
    ```
    **Note**: The characters `*`, `[`, and `!` are special characters in YAML. If you start a pattern with `*`, `[`, or `!`, you must enclose the pattern in quotes.

    Use a pattern to exclude the file `storage-service/src/main/resources/application.dev.properties`

    Merge your changes to `.github/secret_scanning.yml` to your default branch before going to the next step.

    <details>
    <summary>Solution</summary>
    A possible solution is:

    ```yaml
    paths-ignore:
        - '**/test/**'
        - '**/application.dev.properties'
    ```
    </details>

3. Test the pattern by adding another secret or to the file `storage-service/src/main/resources/application.dev.properties`

    For example change the `secretKey` to
    ```
    STRIPE_NEW="sk_live_devboxbcct1DfwS2ClCIKlbN"
    ```

#### Enabling Push Protection

To enable `Push Protection` navigate back to `Code security and analysis` and click the `Enable` button under Secret Scanning. 

#### Introdocuing a new secret

Follow the similar steps as before try to push a new commit that contains a secret:

- Create a new branch in your repository
- In the UI, Edit the `authn-service/authn-service.py` and try to add a new secret
        ```
        STRIPE_NEW="sk_live_devboxbcct1DfwS2ClCIKlmY"
        ```
- If you want to still push you would need to follow the steps to bypass the push protection in the modal.

Question: What would happen if you try to push the secret from your local machine using your git client (or your favourite IDE)? 

As an extra exercises go ahead and try pushing the following secret to the repository.
```
STRIPE_NEW="sk_live_devboxbcct1DfwS2ClCIKllL"
```

#### Exercise 3 - Secret Scanning - Custom Secret Scanning Pattern + Push protection (15 mins)

#### Custom patterns for secret scanning
Secret scanning supports finding other [secret patterns](https://docs.github.com/en/code-security/secret-security/defining-custom-patterns-for-secret-scanning), which are specified by regex patterns and use the Hyperscan library.

1. Add a custom secret pattern by going to the `Code security and analysis` settings and under the header "Custom patterns" click on `New pattern`.
2. Add a custom pattern name, a secret format and test cases.

For example:
    ```
    Custom pattern name: My secret pattern
    Secret format: my_custom_secret_[a-z0-9]{3}
    Test string: my_custom_secret_123
    ```
 3. Save your pattern and observe the secret scanning alerts page to see if your custom secret pattern has been detected.

#### Another Secret Scanning pattern for interal token

Let's work on detecting the following secret:

```text
NBS_1: # Secret Scanning Custom Pattern  
    NBS_tkn_19vciafvzay#wa29ss15vt//tkn
    NBS_tkn_19vciuwwqaw#MM2SaXz15v//tkn
    NBS_tkn_19vrruijoaq#45qqsw115v//tkn
    NBS_tkn_19vcttijoax#4xr3zb15mx//tkn
    NBS_tkn_19vtivfzjqx#4xr3zb15mx//tkn
    NBS_tkn_19yciuijoax#4xr3zb15mx//tkn
    

Dummy value:
NBS_1: # Secret Scanning Custom Pattern  
    NBS_tkn_19vciafvzay#wa29ss15vt//tkn
    NBS_tkn_19vciuwwqaw#MM2SaXz15v//tkn
    NBS_tkn_19vrruijoaq#45qqsw115v//tkn
    NBS_tkn_19vcttijoax#4xr3zb15mx//tkn
    NBS_tkn_19vtivfzjqx#4xr3zb15mx//tkn
    NBS_tkn_19yciuijoax#4xr3zb15mx//tkn
```

<details>
<summary>Solution</summary>

```yaml
</details>
NBS_tkn_19[a-z]{9}#[a-zA-Z0-9]{10}//tkn
```
</details>

After creating and publishing the custom pattern go ahead and select the `Push protection` checkbox to add the pattern to the Push Protection scans. After enabling it 

#### Exercise 4 - Code Scanning and CodeQL (20 mins)

##### Enabling code scanning

1. On the `Security` tab, in the **Vulnerability alerts** section, click **Code scanning**, and then click the **Configure scanning tool** button. 

2. Review the created Action workflow file `codeql-analysis.yml` and choose `Start commit` to accept the default proposed workflow.

3. Head over to the `Actions` tab to see the created workflow in action. Click on the workflow to view details and status for each analysis job.

##### Reviewing any failed analysis job

CodeQL requires a build of compiled languages. An analysis job can fail if our *autobuilder* is unable to build a program to extract an analysis database.

1. Inside the workflow you'll see a list of jobs on the left. Click on the Java job to view the logging output and review any errors to determine if there's a build failure.

2. The `autobuild` compilation failure appears to be caused by a JDK version mismatch. Our project targets JDK version 15. How can we check the Java version that the GitHub hosted runner is using? Does the logging output provide any helpful information?

    <details>
    <summary>Solution</summary>

    - GitHub saves workflow files in the `.github/workflows` directory of your repository. You can add a command to the existing `codeql-analysis.yml` workflow to output the Java version.  Add this anywhere before the step that is failing to help in your debugging:

    ```yaml
    - run: |
        echo "java version"
        java -version
    ```

    </details>

3. The previous debugging has concluded that we have a mismatch.  Resolve the JDK version issue by using the `setup-java` Action in `codeql-analysis.yml` to explicitly specify a version.  This should be added to the workflow before the `autobuild` step to properly configure the runtime environment before the build.

    <details>
    <summary>Solution</summary>

        uses: actions/setup-java@v3
        with:
            java-version: 16
            distribution: 'microsoft'

    </details>

##### Using context and expressions to modify build

How would you [modify](https://docs.github.com/en/free-pro-team@latest/actions/reference/context-and-expression-syntax-for-github-actions) the workflow such that the autobuild step only targets compiled languages (`java` in our repository)?

  <details>
  <summary>Solution</summary>

  You can run this step for only `Java` analysis when you use the `if` expression and `matrix` context.

  ```yaml
  - if: matrix.language == 'java'  
    uses: github/codeql-action/autobuild@v2
  ```
  </details>

##### Reviewing and managing results

1. On the `Security` tab, view the `Code scanning alerts`.

2. For a result, determine:
    1. The issue reported.
    1. The corresponding query id.
    1. Its `Common Weakness Enumeration` identifier.
    1. The recommendation to solve the issue.
    1. The path from the `source` to the `sink`. Where would you apply a fix?
    1. Is it a *true positive* or *false positive*?

##### Triaging a result in a PR

The default workflow configuration enables code scanning on PRs.
Follow the next steps to see it in action.

1. Add a vulnerable snippet of code and commit it to a patch branch and create a PR.

    Make the following change in `frontend/src/components/AuthorizationCallback.vue:27`

    ```javascript
     - if (this.hasCode && this.hasState) {
     + eval(this.code)    
     + if (this.hasCode && this.hasState) {
    ```

2. Is the vulnerability detected in your PR?

3. You can also configure the check failures for code scanning. Go into the `Code security and analysis` settings and modify the Check Failures. Set it to `Only critical/ Only errors` and see how that affects the code scanning status check for subsequent PR checks. In the next steps, you will be enabling additional query suites that have other severity types.

---

## Day 2

### Integrations - GHAS API and Webhooks

#### Exercise 5 - Run tool Checkov in PR and integrate in Code Scanning (15 mins)

In this excercise we will integrate another security testing tool results into Code Scanning. The choice of a tool is Checkov. 

##### Create a new workflow

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

##### Trigger a new checkov run

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

#### Extra: Integrate Secret Scanning alerts in PR

##### Create a new workflow

Following the same steps create a new workflow file that will run the [advanced-security/secret-scanning-review-action](https://github.com/advanced-security/secret-scanning-review-action) action.

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

##### Trigger an action run in PR

To trigger a new checkov run you can create a new branch and edit the `authn-service/.env` file and add the following secret `STRIPE_DEV="sk_live_devboxbcct1DfwS2ClCIKlbT"`
Since you have Push Protection enabled go ahead and by pass it with `I'll fix it later` reason.

Raise a PR and check if that will trigger an analysis and observe the results.

#### Exercise 6 - Catch and alert on Push Protection bypasses (15 mins)

##### Setting up the local envrionment

If you haven't done it so far, go ahead and pull your training repository to your local machine.

- Setup python virtual environment and install the requirements

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Install [ngrok](https://ngrok.com/download) and setup a tunnel

##### Create a new webhook

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

### Troubleshooting GHAS

#### Exercise 8 - Investigate deactivation activity of GHAS in audit log ? (15 mins)

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

#### Exercise 9 - Generate CodeQL debug and identify a problem (15 mins)

TODO
