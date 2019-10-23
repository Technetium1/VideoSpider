if [[ "$(python3 -V)" =~ "Python 3" ]]; then
	echo "Python 3 is installed"
else
	read -p "Python 3 is not installed! Press [Enter] to exit!"
fi
cd `pwd`
read -p "After installing requirements.txt with \"pip install -r /path/to/requirements.txt\" press [Enter] to continue building the executable!"
pyinstaller -F -i web.ico --clean VideoSpider.py
mv `pwd`/dist/VideoSpider `pwd`
rm -rf __pycache__ build dist VideoSpider.spec
