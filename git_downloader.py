import requests
import zipfile
import os
import sys
import shutil

# spuštění přes cmd - 2 parametry (počet python souborů, cílový adresář), ignorovat __init__.py
def find_py_files(directory):
    py_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            # if '__init__.py' in file:
            #     continue
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))
    return py_files

def extract(extracted_directory):
    print('ext_dir')
    print(extracted_directory)
    os.mkdir(os.path.join(os.getcwd(), extracted_directory))
    with zipfile.ZipFile(extracted_directory+'.zip', 'r') as zip_ref:
        zip_ref.extractall(extracted_directory)



if __name__ == "__main__":
    access_token = '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' # doplnit vlastní token

    query = 'language:python'  # You can specify any criteria you want

    url = f'https://api.github.com/search/repositories?q={query}'
    headers = {'Authorization': f'token {access_token}'}

    repo_dict = {""}
    file_count = 0
    while file_count < int(sys.argv[1]):
        response = requests.get(url, headers=headers)
        data = response.json()

    
        if 'items' in data and len(data['items']) > 0:
            random_repo = data['items'][0]
            if random_repo['html_url'] in repo_dict:
                continue
            repo_dict.add(random_repo['html_url'])
            # print(repo_dict)
            # print(random_repo['html_url'])
            random_repo_splitted = str(random_repo['html_url']).split('/')
            archive_url = f'https://api.github.com/repos/{random_repo_splitted[-2]}/{random_repo_splitted[-1]}/zipball'

            with open(random_repo_splitted[-1]+".zip", 'wb') as file:
                file.write(requests.get(archive_url).content)

            extract(random_repo_splitted)
            py_files = find_py_files(random_repo_splitted[-1])
            for file in py_files:
                # print(os.path.join(os.getcwd(), file))
                file_count += 1
                print(file_count)
                # shutil.copyfile(os.getcwd() + '\\' + file, str(sys.argv[2]))
                # os.rename(os.path.join(os.getcwd(), file), str(sys.argv[2]))
        else:
            print('No repositories found.')

