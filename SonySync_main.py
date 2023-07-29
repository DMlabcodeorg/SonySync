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
    Classroom_list = [['Debbie_School', 'StarFish', ['2022']]]

    for school, classroom, year_list in Classroom_list:
        home_pth = '/nethome/anchen.sun/IBSS/{}/{}/{}_2223'.format(school, classroom, classroom)
        date_list = list_remote_folder('pegasus.ccs.miami.edu', home_pth)
        for year in year_list:
            for date in date_list:
                if date.split('-')[-1] == year:
                    date_pth = '{}/{}'.format(home_pth, date)
                    data_folder = list_remote_folder('pegasus.ccs.miami.edu', date_pth)
                    subfolder_flag = 0
                    if 'Spencer_Data' in data_folder:
                        data_folder_name = 'Spencer_Data'
                        subfolder_flag = 1
                    elif 'SPENCER_DATA' in data_folder:
                        data_folder_name = 'SPENCER_DATA'
                        subfolder_flag = 1
                    elif 'SONY_Data' in data_folder:
                        data_folder_name = 'SONY_Data'
                    elif 'LENA_Data' in data_folder:
                        data_folder_name = 'LENA_Data'
                    else:
                        print('Error: Not able to detect Data in {}'.format(date_pth))
                        break

                    audio_pth = '{}/{}'.format(date_pth, data_folder_name)
                    if subfolder_flag == 1:
                        folder_get = list_remote_folder('pegasus.ccs.miami.edu', audio_pth)
                        if len(folder_get) == 1:
                            audio_pth = '{}/{}'.format(audio_pth, folder_get[0])
                            folder_get = list_remote_folder('pegasus.ccs.miami.edu', audio_pth)
                            if 'Audio' in folder_get:
                                audio_pth = '{}/Audio'.format(audio_pth)
                            else:
                                print('Error: Not able to detect audio path in {}'.format(audio_pth))
                                break
                        elif 'SONY_Data' in folder_get:
                            audio_pth = '{}/SONY_Data'.format(audio_pth)
                        else:
                            print('Error: Not able to detect audio path in {}'.format(audio_pth))
                            break
                    date_file_dic = '{}_{}'.format(classroom, date)
                    command = 'scp -r anchen.sun@pegasus.ccs.miami.edu:{} {}'.format(audio_pth, date_file_dic)
                    os.system(command)
                    command = 'python test_flag_class.py --input_path {} --output_path {}'.format(date_file_dic, date_file_dic)
                    os.system(command)
                    print('Successfully generate {}'.format(date_file_dic))


if __name__ == '__main__':
    main()