# GHAS for platform engineers

## Overview

- [ ] [Exercise 1 - Enabling GHAS on your repository](#exercise-1---enabling-ghas-on-your-repository-10-minutes)
- [ ] [Exercise 2 - Secret Scanning and Push Protection](#exercise-2---secret-scanning-and-push-protection-10-mins)
- [ ] [Exercise 3 - Secret Scanning - Custom Secret Scanning Pattern + Push protection](#exercise-3---secret-scanning---custom-secret-scanning-pattern--push-protection-15-mins)
- [ ] [Exercise 4 - Code Scanning and CodeQL](#exercise-4---code-scanning-and-codeql-20-mins)

## GHAS Enablement

### Exercise 1 - Enabling GHAS on your repository (10 minutes)

### Enabling Dependabot alerts

Dependabot can be enabled in the settings of an organization or a repository.

- Go to the repository settings and enable Dependabot alerts in the `Code security and analysis` section. You will be prompted to enable the dependency graph if it's not enabled already.

### Reviewing the dependency graph

Dependabot uses the dependency graph to determine which dependencies are used by your project.

- Verify in the dependency graph that it found dependencies for:
    - The frontend service.
    - The authentication service.
    - The gallery service.
    - The storage service.

The dependency graph can be accessed from the `Insights` tab in your repository.

### Viewing and managing results

After a few minutes, the `Security` tab in the repository will indicate that there are new security alerts. You will see a **Create a security update** button; click this button to create a pull request (PR) to update the vulnerable dependency. The next section will show you how to enable security updates for all applicable Dependabot alerts.

**Note**: If this not the case, we can trigger an analysis by updating `authn-service/requirements.txt`

1. Go to the Dependabot alert section to view the detected dependency issues.

For each dependency alert, we have the option to create a security update or to dismiss the alert with a reason.

2. For one of the alerts, create a dependency security update. If Dependabot can update the dependency automatically, it will create a PR.

3. For one of the alerts, dimiss the alert.

### Enabling Dependabot security updates

Dependabot can automatically create PRs to upgrade vulnerable dependencies to non-vulnerable versions. Please note that there may be some Dependabot alerts that don't have patches. In those cases, a security update is not available.

- Go to the repository settings and enable Dependabot security updates in the *Code security & analysis* section.

After a few minutes multiple PRs will be created that will upgrade vulnerable dependencies.

### Enabling GitHub Adanced security

#### Repo Level

Up until now GHAS licenses were not consumed. Let's go to enabling GitHub Advanced Security now. Navigate back to `Code security and analysis` section in the Settings of your repository. 

You will notice the `GitHub Advanced Security` section right under the Dependabot options which you already enabled. Go ahead and click on the `Enable` button. A modal will pop-up asking you to confirm the action. Click on `Enable GitHub Advanced Security` button to confirm the action. In the modal you will also notice information about how many licenses (GitHub Advanced Security seats) will be consumed. The number of seats consumed is equal to the number of active committers in your repository.

After enabling GitHub Advanced Security you will notice that the `Code scanning alerts` section has been expanded with more options. Before proceeding to those we want to explore the other ways how GitHub Advanced Security can be enabled.

#### Organization Level

Similar to the repository level, navigate to the `Code security and analysis` but on your Organization Settings page. You will notice almost the same view as on the repository level. Few noticable differences:

- You have the `Enable All` / `Disable All` button.
- Additional checkbox option `Automatically enable for new private and internal repositories`. This option will automatically enable GitHub Advanced Security for all new private and internal repositories created in your organization. Turning this feature is useful but it should be accompanied with GHAS license consideration.

NOTE: DO NOT click the `Enable All` button if you are organization admin. We will follow the repo level enablement in this workshop

## How does it work?

### Exercise 2 - Secret Scanning and Push Protection (10 mins)

### Enabling secret scanning

Secret scanning can be enabled in the settings of an organization or a repository. If Advanced Security is not enabled yet, then enable that first (same settings screen).

1. Go to the repository settings and enable secret scanning in the `Code security and analysis` section.

NOTE: Do not enable `Push protection`, yet.

### Viewing and managing secret scanning results

After a few minutes, the `Security` tab in the repository will indicate that there are new security alerts.

- Go to the `Secret scanning` section to view the detected secrets.

For each secret, look at the options to close it and determine which one is most suitable.

### Introducing a test secret

When developing test cases, you might find that secrets are introduced that cannot be abused when disclosed. Secret scanning will still detect and alert on these secrets.

1. In the GitHub repository file explorer, create a test file that contains a test secret.
    - For example the file `storage-service/src/main/resources/application.dev.properties` with the secrets
        ```
        STRIPE_NEW="sk_live_devboxbcct1DfwS2ClCIKlzP"
        ```
2. Determine if the secret is detected when the file is stored.
3. How would you like to manage results from test files?

### Excluding files from secret scanning

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

### Enabling Push Protection

To enable `Push Protection` navigate back to `Code security and analysis` and click the `Enable` button under Secret Scanning. 

### Introdocuing a new secret

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

---

### Exercise 3 - Secret Scanning - Custom Secret Scanning Pattern + Push protection (15 mins)

### Custom patterns for secret scanning

Secret scanning supports finding other [secret patterns](https://docs.github.com/en/code-security/secret-security/defining-custom-patterns-for-secret-scanning), which are specified by regex patterns and use the Hyperscan library.

1. Add a custom secret pattern by going to the `Code security and analysis` settings and under the header "Custom patterns" click on `New pattern`.
2. Add a custom pattern name, a secret format and test cases.   For example:
```
Custom pattern name: My secret pattern
Secret format: my_custom_secret_[a-z0-9]{3}
Test string: my_custom_secret_123
```
3. Save your pattern and observe the secret scanning alerts page to see if your custom secret pattern has been detected.

### Another Secret Scanning pattern for internal token

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

---

### Exercise 4 - Code Scanning and CodeQL (20 mins)

### Enabling code scanning

1. On the `Security` tab, in the **Vulnerability alerts** section, click **Code scanning**, and then click the **Configure scanning tool** button.

2. Select `Set Up -> Advanced` and choose `CodeQL` as the analysis tool.

3. Review the created Action workflow file `codeql-analysis.yml` and choose `Start commit` to accept the default proposed workflow.

4. Head over to the `Actions` tab to see the created workflow in action. Click on the workflow to view details and status for each analysis job.

### Reviewing any failed analysis job

CodeQL requires a build of compiled languages. An analysis job can fail if our *autobuilder* is unable to build a program to extract an analysis database.

1. Inside the workflow, you'll see a list of jobs on the left. Click on the Java job to view the logging output and review any errors to determine if there's a build failure.

2. The `autobuild` compilation failure appears to be caused by a JDK version mismatch. Our project targets JDK version 15. How can we check the Java version that the GitHub hosted runner is using? Does the logging output provide any helpful information?
detailsYou could either check what is documented on the [runner-images](https://github.com/actions/runner-images/blob/main/images/linux/Ubuntu2204-Readme.md) repository, or you can debug your self by executing another run.

    <details>
    <summary>Solution</summary>

    - GitHub saves workflow files in the `.github/workflows` directory of your repository. You can add a command to the existing `codeql-analysis.yml` workflow to output the Java version.  Add this anywhere before the step that is failing to help in your debugging:

    ```yaml
    - run: |
        echo "java version"
        java -version
    ```

    In any case you will conclude that the version is bellow 15. So, you will need to setup the correct version of Java in the runner for the build to succeed. 

    </details>

3. The previous debugging has concluded that we have a mismatch.  Resolve the JDK version issue by using the `setup-java` Action in `codeql-analysis.yml` to explicitly specify a version.  This should be added to the workflow before the `autobuild` step to properly configure the runtime environment before the build.

    <details>
    <summary>Solution</summary>
    ```yaml
      - uses: actions/setup-java@v3
        with:
            java-version: 16
            distribution: 'microsoft'
    ```
    </details>

### Using context and expressions to modify build

How would you [modify](https://docs.github.com/en/free-pro-team@latest/actions/reference/context-and-expression-syntax-for-github-actions) the workflow such that the autobuild step only targets compiled languages (`java` in our repository)?

<details>
<summary>Solution</summary>

You can run this step for only `Java` analysis when you use the `if` expression and `matrix` context.

```yaml
- if: matrix.language == 'java'  
  uses: github/codeql-action/autobuild@v2
```
</details>

### Reviewing and managing code scanning results

1. On the `Security` tab, view the `Code scanning alerts`.

2. For a result, determine:
    1. The issue reported.
    2. The corresponding query id.
    3. Its `Common Weakness Enumeration` identifier.
    4. The recommendation to solve the issue.
    5. The path from the `source` to the `sink`. Where would you apply a fix?
    6. Is it a *true positive* or *false positive*?

### Triaging a result in a PR

The default workflow configuration enables code scanning on PRs.
Follow the next steps to see it in action.

1. Add a vulnerable snippet of code and commit it to a patch branch and create a PR.

    Make the following change in `frontend/src/components/AuthorizationCallback.vue:27`

    ```javascript
     - if (this.hasCode && this.hasState) {
     + eval(this.code)    
     + if (this.hasCode && this hasState) {
    ```

2. Is the vulnerability detected in your PR?

3. You can also configure the check failures for code scanning. Go into the `Code security and analysis` settings and modify the Check Failures. Set it to `Only critical/ Only errors` and see how that affects the code scanning status check for subsequent PR checks. In the next steps, you will be enabling additional query suites that have other severity types.
