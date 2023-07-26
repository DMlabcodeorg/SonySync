import os
import paramiko

def list_remote_folder(remote_host, remote_path):
    folder_list = []
    try:
        # Create an SSH client instance
        ssh_client = paramiko.SSHClient()

        # Automatically add the server's host key (this is insecure and should be done with caution)
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote server using the private key for authentication
        ssh_client.connect(hostname=remote_host, username='anchen.sun')

        # Execute the command to list the contents of the remote folder
        command = f"ls -l {remote_path}"
        stdin, stdout, stderr = ssh_client.exec_command(command)

        # Read and print the output of the command
        output = stdout.read().decode()

        # Split the output into lines and extract folder names
        for line in output.splitlines():
            if line.startswith('d'):
                folder_name = line.split()[-1]
                folder_list.append(folder_name)

        ssh_client.close()

        # Close the SSH connection
        ssh_client.close()

    except paramiko.ssh_exception.AuthenticationException:
        print("Authentication failed. Please check your SSH key.")
    except paramiko.ssh_exception.SSHException as e:
        print(f"SSH error: {e}")
    except Exception as e:
        print(f"Error: {e}")

    return folder_list

def main():
    Classroom_list = [['Debbie_School', 'StarFish']]

    for school, classroom in Classroom_list:
        home_pth = '/nethome/anchen.sun/IBSS/{}/{}/{}_2223'.format(school, classroom, classroom)
        date_list = list_remote_folder('pegasus.ccs.miami.edu', home_pth)
        print(date_list)

if __name__ == '__main__':
    main()