import requests
from pathlib import Path
import toml

def updateMastodon(token, MESSAGE):
    response = requests.post(
        'https://mastodon.social/api/v1/statuses',
        data={'access_token': token, 'status': MESSAGE},
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    return response


if __name__ == '__main__':
    key = toml.loads(Path('.env').read_text(encoding='utf-8'))['mastodon']['access_token']
    version = toml.loads(Path('pyproject.toml').read_text(encoding='utf-8'))['project']['version']
    
    print(f"\n Access Token: {key} \n")
    print(f"\n App Version: {version} \n")
    
    message = f"""Continuing to improve my Python packaging skills.
    New version of my first deployed app 'gslogger' {version} now up! (https://pypi.org/project/gslogger/)
    Any suggestions or critique would be welcome, please don't judge, I'm sensitive. 😜"""

    # message = "This is a test message, please ignore."
    response = updateMastodon(key, message)
    
    here = Path(".junk")
    target = here / 'mastodon_response.json'
    target.write_text(response.json(), encoding='utf-8')
    
    