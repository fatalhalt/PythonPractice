import os
import subprocess

# coded against Python 3.7.0
# this little script needs to be ran with python under admin user for .rename() etc to have have access in System32


CompatTelemetry = os.environ['windir']+ '\\System32\\CompatTelRunner.exe'

if os.path.isfile(CompatTelemetry):
    print('Let\'s nuke CompatTelRunner.exe\n')
    
    #output = subprocess.check_output('attrib %WINDIR%\System32\CompatTelRunner.exe', shell=True)
    #print('File attributes:\n' + output.decode("utf-8"))

    print("taking ownership of %s" % (CompatTelemetry))
    os.system('takeown /f %WINDIR%\System32\CompatTelRunner.exe')
    os.system('icacls %WINDIR%\System32\CompatTelRunner.exe /grant administrators:F')

    if os.path.isfile(CompatTelemetry + '.bak'):
        os.remove(CompatTelemetry + '.bak')

    os.system('taskkill /F /IM CompatTelRunner.exe')

    # .rename requires elevated permissions
    print("renaming to *.bak")
    os.rename(CompatTelemetry, CompatTelemetry + '.bak')
