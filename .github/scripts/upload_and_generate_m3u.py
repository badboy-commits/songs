import os
from github import Github

def upload_files_to_github(repo, folder_path, commit_message):
    uploaded_files = []

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            with open(file_path, 'rb') as file:
                content = file.read()
            
            relative_path = os.path.relpath(file_path, folder_path)
            
            try:
                repo.get_contents(relative_path)
                file_exists = True
            except:
                file_exists = False
            
            try:
                if file_exists:
                    repo_file = repo.get_contents(relative_path)
                    repo.update_file(repo_file.path, commit_message, content, repo_file.sha)
                    print(f'Successfully updated {relative_path}')
                else:
                    repo.create_file(relative_path, commit_message, content)
                    print(f'Successfully uploaded {relative_path}')
                uploaded_files.append(relative_path)
            except Exception as e:
                print(f'Error uploading {relative_path}: {e}')

    if uploaded_files:
        create_and_upload_m3u(repo, uploaded_files, commit_message)

def create_and_upload_m3u(repo, file_paths, commit_message):
    m3u_content = "#EXTM3U\n"
    base_url = "https://badboy-commits.github.io/songs/"
    
    for file_path in file_paths:
        m3u_content += f"{base_url}{file_path}\n"
    
    m3u_path = "playlist.m3u"
    
    try:
        repo_file = repo.get_contents(m3u_path)
        repo.update_file(repo_file.path, commit_message, m3u_content, repo_file.sha)
        print(f'Successfully updated {m3u_path}')
    except:
        repo.create_file(m3u_path, commit_message, m3u_content)
        print(f'Successfully uploaded {m3u_path}')

def main():
    repo_name = 'songs'
    folder_path = ''  # Adjust the path to match where files will be uploaded
    commit_message = 'Update files and generate M3U playlist'
    github_token = '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'
  
    g = Github(github_token)
    user = g.get_user()
    repo = user.get_repo(repo_name)
    
    upload_files_to_github(repo, folder_path, commit_message)

if __name__ == "__main__":
    main()
