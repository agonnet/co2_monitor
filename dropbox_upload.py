import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError


DB_KEY = "tdtmmvro1im5uvg"
DB_SEC = "s33hjmr7iel05at"
DB_REF_TOK = "daXjwJJFMroAAAAAAAAAAa43cVC_RCnoNlf0YSArFop8F_AObP01EJhdpASBYEys"


def get_dropbox_refresh_token():
    auth_flow = DropboxOAuth2FlowNoRedirect(DB_KEY, DB_SEC, token_access_type='offline')

    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print("2. Click \"Allow\" (you might have to log in first).")
    print("3. Copy the authorization code.")
    auth_code = input("Enter the authorization code here: ").strip()

    oauth_result = auth_flow.finish(auth_code)

    print(f"refresh_token = {oauth_result.refresh_token}")


def upload_to_dropbox(local_file_name: str):
    with dropbox.Dropbox(app_key=DB_KEY, app_secret=DB_SEC, oauth2_refresh_token=DB_REF_TOK) as dbx:

        # Check that the access token is valid
        try:
            dbx.users_get_current_account()
        except AuthError as e:
            print(f"Dropbox AuthError {e}")
            return False

    # Upload
    backup_path = f"/{local_file_name}"
    with open(local_file_name, 'rb') as f:
        try:
            dbx.files_upload(f.read(), backup_path, mode=WriteMode('overwrite'))
        except ApiError as e:
            print(f"Dropbox ApiError {e}")
            return False

    return True

# Use to get refresh token only!
if __name__ == '__main__':
    get_dropbox_refresh_token(DB_KEY, DB_SEC)