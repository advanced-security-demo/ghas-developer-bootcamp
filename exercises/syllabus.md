
# GitHub Advanced Security for platform engineers workshop

## Syllabus

### Day 1

#### 1. What is GitHub Advanced Security? 
What is GitHub's approach to the current software security challenges the industry is facing. Overview of what our GitHub Advanced Security consists of and how does it fit in the overall GitHub as platform.

- Intros - 5 mins
- Presentation - 10 mins

**Time: 15 minutes**

#### 2. GitHub Advanced Security Licensing
Understand the GHAS licensing model and learn ways where to control and monitor GHAS seats. In this section we discuss possible license consumption situation with allocations and releasing of licenses.
We will go over the means and tools available for you on GitHub.com to find information about current license consumption, active comitters, etc. Lastly, we will showcase NBS internal dashboards around GHAS licenses.

- Presentation - 10 mins
- Demo 1 - Show current license usage/ what is the active committer count/ what is the license allocation. (5 minutes)
- Demo 2 - ELK dashboard from NBS (5 minutes)

**Time: 20 minutes**

#### 3. GHAS Enablement
Learn how do you manage GHAS policy on an enterprise level. Learn how GHAS enablement on organization and repository level means. Go over the available out of the box options for enablement and tracking coverage.
Conclude with the approach that NBS is taking to making GHAS available and activated to development teams/repos and demonstrate the short-/mid-term IssueOps solutions that will be serving Development teams to onboard and get started with GHAS (5 mins)

- Presentation - 10 mins
- Demo 3 - Control GHAS Enterprise Level policy (5 mins)
- Demo 4 - Onboarding process at NBS issueOps (5 mins)
- Exercise 1 - Enabling GHAS on your repository (10 minutes)

**Time: 30 minutes**

#### 4. How does it work?
Go over each of the GHAS products and explain how does it work:

**Dependancy Graph, Dependabot, Dependancy Review.** We will get familiar with the available features and products but we will not go too much into the depths of them.

**Secret Scanning and Secret Scanning Custom Patterns.** We will learn how secret scanning works under the hood and what you as Ops Engineer can and cannot influence or control. We will practically also get familiar with writing custom patterns and learn how to debug them.

**Code Scanning, CodeQL CLI, CodeQL in CI.** We will dig into what the NBS implementation in CBJ and GitHub Actions of CodeQL scans will be. We will practically setup GitHub Actions to analyze a multi-language project and understand what complexities and challenges such situations might bring.

- Presentation - 20 minutes
- Demo 5 - Dependancy Graph, Dependabot, Dependancy Review (5 mins)
- Exercise 2 - Secret Scanning and Push Protection (10 mins)
- Exercise 3 - Secret Scanning - Custom Secret Scanning Pattern + Push protection (15 mins)
- Exercise 4 - Code Scanning and CodeQL (20 mins)

**Time: 70 minutes**

#### 5. Access, Notifications and alerts

Look into what access requirements to the security features and GHAs alerts including how do you manage this. Understand how this the requirements map to the the standard GitHub pre-defined roles: Read, Triage, Write, Maintain and Admin, but also, the special Security Manager user role. We will exercise the possibilities for creating custom roles for Security Champions as per predefined requirements. 

Further, we will investigate what notifications are sent out by the GHAS products and to whom and understand what comes by default vs what could people further configure.
Lastly, we will discuss some considerations around notifications and how to avoid situations where people get flooded and essentially notifications hove the counter effect to users and how they can manage that.

- Presentation - 10 mins
- Demo 3 - GHAS notifications and personal configurations (5 mins)
- Demo 4 - Default user roles in Security Features context; Defining a custom role; Security manager role (10 mins)

**Time: 25 minutes**

---

### Day 2

#### 6. Integrations - GHAS API and Webhooks

Learn about ways to interact with GHAS outside of what is coming of the box through the available audit log, GHAS APIs and webhooks. 

We will look into what GHAS related information is available in the audit log and scenarios that you could potentially monitor, alert and react on from the system where the audit log is streamed to.
Besides this we will look in detail what the GHAS APIs and Webhook provide around GHAS and we will practically exercise on how you can automate activities on important events.

We will also cover a common use case to integrate other security tools under GHAS and Code Scanning with a goal to make Code Scanning one central spot where developers can find all there (static) security analysis results.

Lastly, we will show how a complete GHAS integration using the APIs and the Webhooks with a SIEM solution looks like.

- Presentation - 20 minutes
- Exercise 5 - Integrate Checkov scan in Code Scanning (15 mins)
- Demo/Exercise  6 - Catch and alert on Push Protection bypasses (15 mins)
- Demo/Exercise 7 - Report on Code Scanning alerts that got dismissed (15 mins)
- Demo 5 - SIEM integration (Splunk/Sentinel) (10 mins)

**Time: 75 minutes**

#### 7. Code Scanning - Capacity planning

Understand what resource planning means in the context of enabling GHAS to your development teams. Look at what are the requirements to running all GHAS products as well as what you would need to operationally monitor and plan on.

We will go over the design that NBS short-/mid-term solution for support CodeQL scans are and discuss the considerations you should have as well as scenarios that you might expect and prepare for.

We will look at what tools and metrics does GitHub Actions provide to support you and what is coming up in this area.

- Presentation - 15 mins
- Demo - Look at CodeQL analysis resource consumption and discuss considerations (10)
- Demo - Show Billing and Actions metrics (10 mins)
- Demo - Potential load test on the available runs (15 mins)

**Time: 40 minutes**

#### 8. Troubleshooting GHAS

In this last part of the workshop we will look at most common issues with GHAS adoption. We will start with general service health-checks you could do but focus on Code Scanning and CodeQL. Go over what are common problems that you might expect around CodeQL runs and configurations and how you go about troubleshooting them. We will look at what a CodeQL debug package contains and how you can use that to triage the problem and either work directly to resolution or pass it on to the responsible party internally for optimal resolution time. Given that not all issues will be resolvable on NBS side, we will see how to efficiently raise a ticket towards GitHub Support.

- Presentation - 15 mins
- Exercise 5 - Investigate deactivation activity of GHAS in audit log (15 mins)
- Exercise 9 - Generate CodeQL debug and identify a problem (15 mins)
- Demo 6 - How to submit a GitHub Support ticket and what do you send with? (5 mins)

**Time: 50 minutes**
