# ======================================================
# GENERAL DOCUMENT COMMANDS ============================
# ======================================================
# RETRIEVING META DATA AND INFORMATION (e.g. parameters, options) ABOUT DOCUMENTS
# Use the following command to view a description of the Systems Manager JSON document
aws ssm describe-document --name "AWS-RunShellScript" --query "[Document.Name,Document.Description]"
# Use the following command to view the available parameters and details about those parameters.
aws ssm describe-document --name "AWS-RunShellScript" --query "Document.Parameters[*]"

