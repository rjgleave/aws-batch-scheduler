import re
import json

# set up regular expressions
# use https://regexper.com to visualize these if required
rx_dict = {
    'boxname': re.compile(r'box_name:(?P<boxname>.*)\n'),
    'jobname': re.compile(r'insert_job:(?P<jobname>.*)\n'),
    'command': re.compile(r'command:(?P<command>.*)\n'),
    'machine': re.compile(r'machine:(?P<machine>.*)\n'),
    'description': re.compile(r'description:(?P<description>.*)\n'),
    'condition': re.compile(r'condition:(?P<condition>.*)\n'),
    'alarm': re.compile(r'alarm_if_fail:(?P<alarm>.*)\n'),
}

def _parse_line(line):
    """
    Do a regex search against all defined regexes and
    return the key and match result of the first matching regex

    """

    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None


def pparse(filepath):
    """
    Parse text at given filepath

    Parameters
    ----------
    filepath : str
        Filepath for file_object to be parsed
    """
    # Reset all the record variables
    boxname=''
    seq=0
    sequence=''
    jobname=''
    recordtype=''
    command=''
    machine=''
    alarm=''
    recordtype=''
    description=''
    condition=''

    data = []  # create an empty list to collect the data
    # open the file and read through it line by line
    with open(filepath, 'r') as file_object:
        line = file_object.readline()
        while line:
            # at each line check for a match with a regex
            key, match = _parse_line(line)

            # extract school name
            if key:

                # extract school name
                if key == 'jobname':
                    m = match.group('jobname')
                    s = m.split()
                    jobname = s[0]
                    recordtype = s[2]

                # schedule name (box name)
                if key == 'boxname':
                    boxname = match.group('boxname')
                    if recordtype == 'BOX':
                        boxname = jobname

                # target machine
                if key == 'machine':
                    machine = match.group('machine')

                # remote command 
                if key == 'command':
                    command = match.group('command')

                # description
                if key == 'description':
                    description = match.group('description')

                # dependencies
                if key == 'condition':
                    condition = match.group('condition')

                # alarm indicator (and end of row)
                if key == 'alarm':
                    alarm = match.group('alarm')
                    # Append a new row
                    seq += 10
                    sequence = str(seq)
                    row = {
                        'ScheduleName': boxname,
                        'Sequence': sequence,
                        'JobName': jobname,
                        'TargetHost': machine,
                        'Command': command,
                        'RecordType': recordtype,
                        'Description': description,
                        'JobDependencies': condition,
                    }
                    data.append(row)

                    # Reset all the record variables
                    boxname=''
                    sequence=''
                    jobname=''
                    recordtype=''
                    command=''
                    machine=''
                    alarm=''
                    recordtype=''
                    description=''
                    condition=''  

            line = file_object.readline()

    return data


if __name__ == '__main__':
    filepath = 'EDW_Recycle_CalcConsumer_Box.jil'
    data = pparse(filepath)
    jdata = json.dumps(data)
    print(jdata)