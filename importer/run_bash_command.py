from subprocess import Popen, PIPE, STDOUT


def runrealcmd(command):
    '''Run command in bash and wait until done to run the next one'''
    print(str(command))
    process = Popen(command, stdout=PIPE, shell=True, stderr=STDOUT, bufsize=1, close_fds=True)
    for line in iter(process.stdout.readline, b''):
        print(line.rstrip().decode('utf-8'))
    process.stdout.close()
    process.wait()
    return process.returncode