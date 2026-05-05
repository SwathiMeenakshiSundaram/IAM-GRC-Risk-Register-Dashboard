# IAM Access Review & GRC Risk Register Dashboard

## Project Overview

This project simulates an Identity and Access Management (IAM) access review process using a fake company user access dataset.

The goal of this project is to identify risky access patterns, least-privilege violations, missing MFA, inactive accounts, terminated-user access, and access review gaps. The dashboard also generates audit-style findings and a GRC risk register with remediation recommendations.

This project is designed for IAM, GRC, IT Risk, Access Governance, Security Compliance, and IT Audit learning.

---

## Why This Project Matters

Organizations must regularly review user access to ensure that employees only have the permissions required for their job responsibilities.

Weak access governance can create serious security, compliance, and audit risks. Examples include:

- Former employees still having system access
- Admin users without MFA enabled
- Interns or junior users having excessive privileges
- Users having access outside their department
- Inactive accounts remaining active
- Access not being reviewed on time

This project demonstrates how an IAM/GRC analyst can review access data, identify control gaps, assign risk levels, and recommend remediation actions.

---

## Key Concepts Demonstrated

- Identity and Access Management
- Access Reviews
- Least Privilege
- Role-Based Access Control
- Privileged Access Management
- Multi-Factor Authentication Review
- Joiner-Mover-Leaver / Offboarding Controls
- Account Lifecycle Management
- GRC Risk Register
- Control Testing
- Audit Findings
- Risk Treatment
- Remediation Recommendations

---

## Tools and Technologies Used

- Python
- Pandas
- Streamlit
- Matplotlib
- CSV dataset
- GitHub

---

## Dataset Description

The project uses a fake IAM user access dataset containing sample users and access details.

The dataset includes:

| Column | Description |
|---|---|
| UserID | Unique user identifier |
| Name | User name |
| Department | User department |
| JobRole | User job role |
| EmploymentStatus | Active or terminated employee status |
| SystemAccess | Application or system the user can access |
| AccessLevel | Read, Write, or Admin access |
| MFAEnabled | Whether MFA is enabled |
| LastLoginDays | Number of days since last login |
| LastAccessReviewDays | Number of days since access was last reviewed |

All data in this project is fictional and created for learning purposes.

---

## Risk Rules Used

The dashboard applies simple IAM/GRC risk rules to identify access issues.

| Risk Rule | Risk Level | Control Area |
|---|---|---|
| Terminated user still has system access | High | Joiner-Mover-Leaver / Offboarding |
| Admin access without MFA | High | Privileged Access Management |
| Intern has admin access | High | Least Privilege Access |
| Access not reviewed in over 90 days | Medium | Periodic Access Review |
| Inactive account has not logged in for over 90 days | Medium | Account Lifecycle Management |
| User has access outside their department | Medium | Role-Based Access Control |

---

## Dashboard Features

The Streamlit dashboard includes:

- User access dataset viewer
- Sidebar filters by department, access level, MFA status, and employment status
- Access review summary metrics
- IAM/GRC audit findings table
- Risk level summary
- Executive summary
- GRC risk register
- Risk owner mapping
- Risk treatment status
- Risk level distribution chart
- Downloadable CSV risk register report

---

## Control Objective

The objective of this access review is to evaluate whether user access follows least privilege, MFA enforcement, account lifecycle management, and periodic access review requirements.

Findings are categorized by risk level and include remediation recommendations to support IAM governance and GRC control review.

---

## Example Findings

The dashboard can identify findings such as:

- Admin access without MFA
- Terminated employee still having access
- Intern with privileged access
- Access not reviewed in over 90 days
- Inactive user account
- User access outside department

Each finding includes:

- User ID
- User name
- Finding description
- Risk level
- Control area
- Risk owner
- Risk treatment
- Status
- Remediation recommendation

---

## Example Remediation Recommendations

| Finding | Recommendation |
|---|---|
| Terminated user still has access | Disable account immediately and remove all system access |
| Admin access without MFA | Enable MFA immediately or remove admin access until MFA is enforced |
| Intern has admin access | Review business justification and reduce access to least privilege |
| Access not reviewed in over 90 days | Perform access review and document approval or removal decision |
| Inactive account | Review account activity and disable if no longer required |
| Access outside department | Validate business need and remove access if not justified |

---

## How to Run the Project

### 1. Clone the repository

git clone https://github.com/SwathiMeenakshiSundaram/IAM-GRC-Risk-Register-Dashboard.git

cd IAM-GRC-Risk-Register-Dashboard
pip install -r requirements.txt
streamlit run app.py

## License

This project is licensed under the MIT License.