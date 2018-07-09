# ======================================================
# SYSTEM STATUS COMMANDS    ============================
# ======================================================

# GENERAL - all Instances ---
# see all instances registered to your account that are currently reporting an online status
# Substitute the ValueSet="Online" with "ConnectionLost" or "Inactive" to view those statuses:
aws ssm describe-instance-information --instance-information-filter-list key=PingStatus,valueSet=Online --output json

# INSTANCE-SPECIFIC ---------
# Use the following command to get status details about one or more instance
aws ssm describe-instance-information --instance-information-filter-list key=InstanceIds,valueSet="i-06eea61bed4d5882a","i-008209845c755399b" --output json

# Use the following command to see which instances are running the latest version of SSM Agent
# Substitute ValueSet="LATEST" 
aws ssm describe-instance-information --instance-information-filter-list key=AgentVersion,valueSet=LATEST --output json
# or with a specific version (for example, 1.0.145 or 1.0)
aws ssm describe-instance-information --instance-information-filter-list key=AgentVersion,valueSet="2.2.120.0" --output json

