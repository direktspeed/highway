from ubuntu:12.04
maintainer evan hazlett <ejhazlett@gmail.com>
run apt-get update
run DEBIAN_FRONTEND=noninteractive apt-get -y upgrade
run apt-get install -y python-dev python-setuptools libxml2-dev libxslt-dev git-core
run easy_install pip
run pip install uwsgi
env APP_DIR /app
add . $APP_DIR
run pip install -r $APP_DIR/requirements.txt
expose 8000
cmd ["uwsgi", "--ini", "/app/app.ini"]
