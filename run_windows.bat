if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit
python -m pip install --upgrade pip
pip install selenium
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
cd /D "%~dp0"
python read_site.py
python write_courses.py
python calendar_input.py
exit

