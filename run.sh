#!/bin/bash
APP_DIR=/app
# syncdb & migrate
cd $APP_DIR
python manage.py syncdb --noinput
python manage.py migrate --noinput
if [ ! -z "${ADMIN_PASS}" ] ; then
    python manage.py update_admin_user --username=admin --password=${ADMIN_PASS}
fi
uwsgi --ini /app/app.ini
