import requests

GITEA_DOMAIN = ''
GITEA_USERNAME = ''
GITEA_PASSWORD = ''
GITHUB_USERNAME = ''

response_github = requests.get(f'https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100')

# List Github repos

if response_github.status_code == 200:
    for repo in response_github.json():
        if not repo['fork']:
            repo_clone_url = repo['clone_url']
            repo_name = repo['name']

            # Get user Gitea
            response_user = requests.get(f'https://{GITEA_DOMAIN}/api/v1/users/{GITEA_USERNAME}')

            # Create mirror
            if response_user.status_code == 200:
                print('Creating mirror repository: ' + repo_name)
                url_migrate = f'https://{GITEA_DOMAIN}/api/v1/repos/migrate'
                response_migrate = requests.post(
                        url_migrate,
                        json={
                            'clone_addr': repo_clone_url,
                            'mirror': True,
                            'private': True,
                            'repo_name': repo_name,
                            'uid': response_user.json()['id']
                        },
                        auth=(GITEA_USERNAME, GITEA_PASSWORD)
                    )
                print('Mirror repository created!')
            else:
                print('Error user Gitea')
else:
    print('Error list Github repos')
