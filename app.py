import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(
    page_title="IAM Access Review & GRC Risk Register Dashboard",
    page_icon="🔐",
    layout="wide"
)

# Title
st.title("🔐 IAM Access Review & GRC Risk Register Dashboard")

st.write(
    """
    This dashboard simulates an Identity and Access Management (IAM) access review.
    It identifies risky access patterns such as terminated users with active access,
    admin access without MFA, inactive accounts, and access review gaps.
    """
)

st.subheader("🎯 Control Objective")

st.info(
    """
    The objective of this access review is to evaluate whether user access follows
    least privilege, MFA enforcement, account lifecycle management, and periodic
    access review requirements. Findings are categorized by risk level and include
    remediation recommendations to support IAM governance and GRC control review.
    """
)

st.subheader("🧾 Risk Criteria")

st.markdown(
    """
    - **High Risk:** Terminated users with access, admin access without MFA, or interns with admin privileges.
    - **Medium Risk:** Access not reviewed in over 90 days, inactive accounts, or access outside department.
    - **Low Risk:** Access appears appropriate based on role, MFA status, and review timeline.
    """
)

# Load dataset
df = pd.read_csv("iam_access_dataset.csv")

# Show dataset
# Sidebar filters
st.sidebar.header("🔎 Filters")

risk_filter_note = st.sidebar.info(
    "Use these filters to review user access by department, access level, MFA status, and employment status."
)

department_filter = st.sidebar.multiselect(
    "Select Department",
    options=sorted(df["Department"].unique()),
    default=sorted(df["Department"].unique())
)

access_filter = st.sidebar.multiselect(
    "Select Access Level",
    options=sorted(df["AccessLevel"].unique()),
    default=sorted(df["AccessLevel"].unique())
)

mfa_filter = st.sidebar.multiselect(
    "Select MFA Status",
    options=sorted(df["MFAEnabled"].unique()),
    default=sorted(df["MFAEnabled"].unique())
)

status_filter = st.sidebar.multiselect(
    "Select Employment Status",
    options=sorted(df["EmploymentStatus"].unique()),
    default=sorted(df["EmploymentStatus"].unique())
)

filtered_df = df[
    (df["Department"].isin(department_filter)) &
    (df["AccessLevel"].isin(access_filter)) &
    (df["MFAEnabled"].isin(mfa_filter)) &
    (df["EmploymentStatus"].isin(status_filter))
]

# Show dataset
st.subheader("📋 User Access Dataset")
st.dataframe(filtered_df, use_container_width=True)

# Basic metrics
total_users = len(filtered_df)
admin_users = len(filtered_df[filtered_df["AccessLevel"] == "Admin"])
users_without_mfa = len(filtered_df[filtered_df["MFAEnabled"] == "No"])
terminated_users = len(filtered_df[filtered_df["EmploymentStatus"] == "Terminated"])

st.subheader("📊 Access Review Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Users Reviewed", total_users)
col2.metric("Admin Users", admin_users)
col3.metric("Users Without MFA", users_without_mfa)
col4.metric("Terminated Users", terminated_users)

# Risk detection logic
findings = []

for _, row in filtered_df.iterrows():
    user = row["Name"]
    department = row["Department"]
    job_role = row["JobRole"]
    status = row["EmploymentStatus"]
    system = row["SystemAccess"]
    access = row["AccessLevel"]
    mfa = row["MFAEnabled"]
    last_login = row["LastLoginDays"]
    last_review = row["LastAccessReviewDays"]

    # Rule 1: Terminated users still have access
    if status == "Terminated":
        findings.append({
            "UserID": row["UserID"],
            "Name": user,
            "Finding": "Terminated user still has system access",
            "RiskLevel": "High",
            "ControlArea": "Joiner-Mover-Leaver / Offboarding",
            "Recommendation": "Disable account immediately and remove all system access."
        })

    # Rule 2: Admin access without MFA
    if access == "Admin" and mfa == "No":
        findings.append({
            "UserID": row["UserID"],
            "Name": user,
            "Finding": "Admin access without MFA",
            "RiskLevel": "High",
            "ControlArea": "Privileged Access Management",
            "Recommendation": "Enable MFA immediately or remove admin access until MFA is enforced."
        })

    # Rule 3: Intern has admin access
    if "Intern" in job_role and access == "Admin":
        findings.append({
            "UserID": row["UserID"],
            "Name": user,
            "Finding": "Intern has privileged/admin access",
            "RiskLevel": "High",
            "ControlArea": "Least Privilege Access",
            "Recommendation": "Review business justification and reduce access to least privilege."
        })

    # Rule 4: Access not reviewed in over 90 days
    if last_review > 90:
        findings.append({
            "UserID": row["UserID"],
            "Name": user,
            "Finding": "Access has not been reviewed in over 90 days",
            "RiskLevel": "Medium",
            "ControlArea": "Periodic Access Review",
            "Recommendation": "Perform access review and document approval or removal decision."
        })

    # Rule 5: Inactive account
    if last_login > 90:
        findings.append({
            "UserID": row["UserID"],
            "Name": user,
            "Finding": "Inactive account has not logged in for over 90 days",
            "RiskLevel": "Medium",
            "ControlArea": "Account Lifecycle Management",
            "Recommendation": "Review account activity and disable if no longer required."
        })

    # Rule 6: Department mismatch access
    if department == "HR" and "Finance" in system:
        findings.append({
            "UserID": row["UserID"],
            "Name": user,
            "Finding": "User has access outside their department",
            "RiskLevel": "Medium",
            "ControlArea": "Role-Based Access Control",
            "Recommendation": "Validate business need and remove access if not justified."
        })

# Convert findings to dataframe
findings_df = pd.DataFrame(findings)

st.subheader("🚩 IAM / GRC Audit Findings")

if findings_df.empty:
    st.success("No access risks found.")
else:
    st.dataframe(findings_df, use_container_width=True)

    high_risks = len(findings_df[findings_df["RiskLevel"] == "High"])
    medium_risks = len(findings_df[findings_df["RiskLevel"] == "Medium"])

    st.subheader("📌 Risk Findings Summary")

    risk_col1, risk_col2, risk_col3 = st.columns(3)

    risk_col1.metric("Total Findings", len(findings_df))
    risk_col2.metric("High Risk Findings", high_risks)
    risk_col3.metric("Medium Risk Findings", medium_risks)

    st.subheader("📝 Executive Summary")

    st.write(
        f"""
        This access review identified **{len(findings_df)} total IAM/GRC findings**
        across the selected user population. Of these findings, **{high_risks} are high risk**
        and **{medium_risks} are medium risk**.

        High-risk findings should be prioritized for immediate remediation, especially
        issues involving privileged access, missing MFA, terminated users, and excessive access.
        Medium-risk findings should be reviewed by system owners and documented as part of
        the periodic access review process.
        """
    )

    st.subheader("📒 GRC Risk Register")

    risk_register_df = findings_df.copy()

    risk_register_df["RiskOwner"] = risk_register_df["ControlArea"].map({
        "Joiner-Mover-Leaver / Offboarding": "IAM Operations Team",
        "Privileged Access Management": "Security Operations Team",
        "Least Privilege Access": "Access Governance Team",
        "Periodic Access Review": "System Owner",
        "Account Lifecycle Management": "IAM Operations Team",
        "Role-Based Access Control": "Business Application Owner"
    })

    risk_register_df["RiskTreatment"] = risk_register_df["RiskLevel"].map({
        "High": "Mitigate Immediately",
        "Medium": "Review and Remediate",
        "Low": "Monitor"
    })

    risk_register_df["Status"] = "Open"

    st.dataframe(
        risk_register_df[
            [
                "UserID",
                "Name",
                "Finding",
                "RiskLevel",
                "ControlArea",
                "RiskOwner",
                "RiskTreatment",
                "Status",
                "Recommendation"
            ]
        ],
        use_container_width=True
    )

        # Risk level chart
    st.subheader("📈 Risk Level Distribution")

    risk_counts = findings_df["RiskLevel"].value_counts()

    fig, ax = plt.subplots()
    ax.bar(risk_counts.index, risk_counts.values)
    ax.set_xlabel("Risk Level")
    ax.set_ylabel("Number of Findings")
    ax.set_title("IAM / GRC Risk Findings by Risk Level")

    st.pyplot(fig)

    # Downloadable audit report
    st.subheader("⬇️ Download Audit Report")

    csv_report = risk_register_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download IAM/GRC Audit Report as CSV",
        data=csv_report,
         file_name="iam_grc_risk_register_report.csv",
        mime="text/csv"
    )