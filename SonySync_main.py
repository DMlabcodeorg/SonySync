import os
import paramiko

def list_remote_folder(remote_host, remote_path):
    try:
        # Create an SSH client instance
        ssh_client = paramiko.SSHClient()

        # Automatically add the server's host key (this is insecure and should be done with caution)
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Load your private key (SSH key pair) for passwordless authentication
        # Replace 'path/to/your/private_key' with the actual path to your private key
        private_key_path = 'path/to/your/private_key'
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

        # Connect to the remote server using the private key for authentication
        ssh_client.connect(hostname=remote_host, username='your_username', pkey=private_key)

        # Execute the command to list the contents of the remote folder
        command = f"ls -l {remote_path}"
        stdin, stdout, stderr = ssh_client.exec_command(command)

        # Read and print the output of the command
        output = stdout.read().decode()
        print(output)

        # Close the SSH connection
        ssh_client.close()

    except paramiko.ssh_exception.AuthenticationException:
        print("Authentication failed. Please check your SSH key.")
    except paramiko.ssh_exception.SSHException as e:
        print(f"SSH error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    Classroom_list = [['Debbie_School', 'StarFish']]

    for school, classroom in Classroom_list:
        home_pth = '/nethome/anchen.sun/IBSS/{}/{}/{}_2223'.format(school, classroom, classroom)
        list_remote_folder('anchen.sun@pegasus.ccs.miami.edu', home_pth)

if __name__ == '__main__':
    main()