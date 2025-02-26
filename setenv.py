from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen, Request

from config import API_VERSION, VK_APP_ID

ENV_FILE_TEMPLATE = """
POSTGRES_DB=tgvkbot
POSTGRES_PASSWORD=postgres
BOT_TOKEN=%(tg_token)s
VK_APP_ID=%(vk_app_id)s
ALLOWED_USER_IDS=%(allowed_user_ids)s
"""

ENV_FILE = 'env_file'

def check_token(token):
    response = urlopen("https://api.telegram.org/bot{token}/{method}".format(token=token, method='getMe'))
    if response.code == 200:
        return True
    else:
        raise HTTPError


def get_auth_page(app_id):
    AUTH_URL = 'https://oauth.vk.com/authorize'
    params = {'client_id': app_id,
              'redirect_uri': 'https://oauth.vk.com/blank.html',
              'display': 'mobile',
              'response_type': 'token',
              'v': API_VERSION
              }
    post_args = urlencode(params).encode('UTF-8')
    request = Request(AUTH_URL, post_args)
    response = urlopen(request)
    if response.code == 200:
        return True
    else:
        raise HTTPError


def set_env():
    while True:
        tg_token = input('tg bot token: ')
        tg_token = tg_token.strip()
        try:
            print('Checking token...')
            check_token(tg_token)
            break
        except HTTPError:
            print('Wrong or notworking tg bot token. Try again!')

    while True:
        vk_app_id = input('VK APP ID (may leave empty): ')
        vk_app_id = vk_app_id.strip()
        if vk_app_id:
            try:
                get_auth_page(vk_app_id)
                break
            except HTTPError:
                print('wrong VK APP ID!')
        else:
            print('will be used VK APP ID {} from Kate Mobile'.format(VK_APP_ID))
            break

    with open(ENV_FILE, 'w') as env_file:
        env_file.write(
            ENV_FILE_TEMPLATE % {'tg_token': tg_token, 'vk_app_id': vk_app_id or VK_APP_ID, 'allowed_user_ids': ''})

    print('Env variables are successfully set {}'.format(ENV_FILE))


if __name__ == '__main__':
    try:
        set_env()
    except KeyboardInterrupt:
        print('\nEnv variables setup interrupted!')
