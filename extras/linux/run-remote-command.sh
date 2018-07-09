
# ======================================================
# RUNNING REMOTE COMMANDS ==============================
# ======================================================
# ---EXAMPLES ---  SENDING SIMPLE COMMANDs to an instance
# -- Example 1 --- Running Services (service --status-all)
# Step 1: send a simple command to a single instance to retrieve the services running 
# on the instance.  It will only return a command ID, which you send to the next command 
# below to retrieve the results.   NOTE: specifying JSON as the output will make reading it easier.
aws ssm send-command --document-name "AWS-RunShellScript" --comment "listing MY services" --instance-ids "i-06eea61bed4d5882a" --parameters commands="service --status-all" --region us-east-2 --output json
# Step 2: returns the result of the command above
aws ssm list-command-invocations --command-id "<INSERT COMMAND ID FROM STEP 1 ABOVE>" --details

# --Example 2 --- Running PROCESSES (ps aux)
# Step 1: send a simple command to a single instance to to provide information about the currently running processes 
# on the instance.  It will only return a command ID, which you send to the next command 
# below to retrieve the results.   NOTE: specifying JSON as the output will make reading it easier.
aws ssm send-command --document-name "AWS-RunShellScript" --comment "listing RUNNING PROCESSES" --instance-ids "i-06eea61bed4d5882a" --parameters commands="ps aux" --region us-east-2 --output json
# Step 2: returns the result of the command above
aws ssm list-command-invocations --command-id "<INSERT COMMAND ID FROM STEP 1 ABOVE>" --details

# ----OTHER EXAMPLES TO PRACTICE --------
# This example gets the IP information about an instance.
aws ssm send-command --instance-ids "i-0cb2b964d3e14fd9f" --document-name "AWS-RunShellScript" --comment "IP config" --parameters "commands=ifconfig" --output text
# This example runs an echo command on a target instance.
aws ssm send-command --document-name "AWS-RunPowerShellScript" --parameters commands=["echo helloWorld"] --targets "Key=instanceids,Values=i-0cb2b964d3e14fd9f"
# USING TAG IDs):  send command to a TARGET using the TAG IDs
aws ssm send-command --document-name "AWS-RunShellScript" --comment "listing RUNNING PROCESSES for a TARGET machine tag" --targets Key=tag:"targetID",Values="Instance-0001" --parameters commands="ps aux" --region us-east-2 --output json

# MULTIPLE INSTANCES: send command to multiple instances USING THE INSTANCE PARAMETER
aws ssm send-command --document-name name --targets Key=tag:tag_name,Values=tag_value [...]  # <<< NOTE: don't include [] !!!!
aws ssm send-command --document-name "AWS-RunShellScript" --comment "listing RUNNING PROCESSES ON MULTIPLE INSTANCES" --instance-ids "i-06eea61bed4d5882a" "i-008209845c755399b" --parameters commands="ps aux" --region us-east-2 --output json
# MULTIPLE TARGETS (using INSTANCE IDs): send command to multiple INSTANCES using the TARGET PARAMETER (instead of INSTANCE parameter)
aws ssm send-command --document-name name --targets Key=instanceids,Values=ID1,ID2,ID3 [...]   # <<< NOTE: don't include [] !!!!
aws ssm send-command --document-name "AWS-RunShellScript" --comment "listing RUNNING PROCESSES ON MULTIPLE INSTANCES" --targets Key=instanceids,Values="i-06eea61bed4d5882a","i-008209845c755399b" --parameters commands="ps aux" --region us-east-2 --output json

# MULTIPLE INSTANCES (using TAG IDs):  send command to multiple TARGETS using the TAG IDs
aws ssm send-command --document-name name --targets Key=tag:tag_name,Values=tag_value [...]   # <<< NOTE: don't include [] !!!!
aws ssm send-command --document-name "AWS-RunShellScript" --comment "listing RUNNING PROCESSES ON MULTIPLE TARGET Tags" --targets Key=tag:"targetID",Values="Instance-0001","Instance-0002" --parameters commands="ps aux" --region us-east-2 --output json

# Scratch Pad
aws ssm send-command --document-name "AWS-RunShellScript"  --targets Key=tag:"targetID",Values="Instance-0001" --parameters commands="ps aux" --region us-east-2 --output json

aws ssm send-command --document-name "AWS-RunShellScript" --parameters commands=["echo helloWorld"] --targets Key=tag:"targetID",Values="Instance-0001" --output json

# ======================================================
# USING PARAMETERS WITH A SSM COMMAND ================
# ======================================================
# STEP 1: store the parameter
aws ssm put-parameter --name "/Practice/SSM/simple-response" --value "Hello World" --type String
# STEP 2: use the parameter in a command  NOTE: CAN'T GET THIS TO WORK YET
aws ssm send-command --document-name "AWS-RunShellScript" --parameters "commands=["echo {{ssm:/Practice/SSM/simple-response}}"]" --targets "Key=instance-ids,Values=the ID of an instance configured for Systems Manager"
aws ssm send-command --document-name "AWS-RunShellScript" --parameters "commands=["echo {{ssm:/Practice/SSM/simple-response}}"]" --targets Key=tag:"targetID",Values="Instance-0001"








# Scratch Pad
aws ssm send-command --document-name "AWS-RunShellScript"  --targets Key=tag:"targetID",Values="Instance-0001" --parameters commands="ps aux" --region us-east-2 --output json