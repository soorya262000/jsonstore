@ECHO OFF
pip uninstall jstore
echo y
cd C:\Users\soorya\Desktop\jsonstore1
python setup.py sdist
python setup.py bdist_wheel
cd dist
pip install jstore-0.1-py3-none-any.whl
PAUSE