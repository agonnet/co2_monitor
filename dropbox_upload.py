import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

# Add OAuth2 access token here.
# You can generate one for yourself in the App Console.
# See <https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/>
TOKEN = 'sl.u.AGN22lrgoRMzGSmwuMiMp1SvK7SRsh7WP0qFx64vMyO0WOkeOgUjfxWu_rrJwIwjkOAAc_Ljy1EJO5z07X_tn-rc9928l2oE-RR5oe2R8tB9sG8cCzdVgmG0A-JEw6speKUoF_JTAihbxw-b6qER5AlgVDuRWMW3oI1EUWcUIL65b-K9y3i_sC4n54oK9Q0TVYxnTEVa9ttaa-p50QMg1D5jgOrIzKvQO9A86dxq75YLMDFZsRNcMBzWP750wWqCnbxaMKneP1wnxxcUeg-knpf7Cvxte0aMtLh7pbA-Dcf0iEKvq1P5GJ0U5IjXaI37muHEBRCSXNhQbHbd32-AY0PDWPwRURDqH7duRnsn73d9TNNx9-coNmXs50d9QbA37gUwxh8dZvIlBQ3p_d1mq-L_tYSrtT2msuZuaZjmy7Xti0KZeK8fU4ZpQUhPIovNW2teKo0jJwqurb-SJV1Lkqa-eRT_kaQ7dscN9Ss9RSXYjJ42UX80zPu888c6OOtm6rWtoqpGpxqL_ec_qVPmOWmevAYx_W5jtErb0LEEegFL7PY2BQq0X_kMTqjdm6HHOHYdzZt0k7XawR6F8i_WaIcLLfgHV0vkAquKYqyNvTq460uoLIe10Mkxw86SRffI-s9LbGXRhDK-_fWD3PekNkmwjzRsmCry_T_6ug8oDG3RFUiOaF4J3yOKWyM-FGSkV4TB_TVyY4LCg_YSiy1EXFpbe2NJa4f2Kh9dXgdtrHwp66-TcfNDnvk1Mp7AuhxZyjxG7f-tqV_hQE85nW2Rh5MIyX_DVuQ6O8ITgKps66v7zfmgVdgZzaPrbW3QpCuWHPwB9rp22QWWcJsuMOEQ-InI2n2Q1ap1eWE5K3rUDw6fVNXvkDn92RUl-zbgXTGW2My4toIJnPrcy0CQg2ajBI7mPh65TmL5DQBMCLnteBNEv8QsIfWj8NdFtqpAeQM64UJHvXFvRIl4mxh7G8niH8f-EIxh6xf37Ky1rbpUZ5cc9axDC0RUk10Dhv33LWAGJhSDaHkwuAdEnweYyYehITqgiZY5ZCdzK350W1jUWId7cJBqd9NcnrrIDQhAiW8v_WndnIUGXLQb1Nyla3pDFttkCL5Tc2QPeEij9AvsJvEzJQaX7DHNjDQjLx2_3bAFwQDMEkZ3eEgK3hIDrbvWz_D-nngW_F_nISe1zxkL9TbJK2MeopKdf17bl_piIVmMjECPjF6In2ULmphX7BxT1DmmaSarALlOAUuNoMNUnCOidw'

def upload_to_dropbox(local_file_name: str):
    with dropbox.Dropbox(TOKEN) as dbx:

        # Check that the access token is valid
        try:
            dbx.users_get_current_account()
        except AuthError as e:
            print(f"Dropbox AuthError {e}")
            return False

    # Upload
    backup_path = f"CO2_Monitor/{local_file_name}"
    with open(local_file_name, 'rb') as f:
        try:
            dbx.files_upload(f.read(), backup_path, mode=WriteMode('overwrite'))
        except ApiError as e:
            print(f"Dropbox ApiError {e}")
            return False

    return True


