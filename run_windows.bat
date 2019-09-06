if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit
python -m pip install --upgrade pip
pip install --upgrade selenium
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install --upgrade PyQt5
cd /D "%~dp0"
python get_creds.py
python down_creds.py
python read_site.py
python write_courses.py
python calendar_compre_input.py
python calendar_courses_input.py
exit

