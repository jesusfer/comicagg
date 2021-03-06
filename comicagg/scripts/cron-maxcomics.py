#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Limit the number of unread comics a user can have."""
import os
import sys
import time
from datetime import datetime
# Add the root folder to the python path
d = os.path.dirname(os.path.abspath(sys.argv[0]))
d = os.path.join(d, '..')
d = os.path.join(d, '..')
d = os.path.abspath(d)
sys.path.insert(0, d)

os.environ['DJANGO_SETTINGS_MODULE'] = "comicagg.settings"

import django
django.setup()

from django.contrib.auth.models import User

starttime = datetime.now()
if len(sys.argv) > 1:
    uid = int(sys.argv[1])
    allusers = User.objects.order_by('id').filter(id__gte=uid)
else:
    allusers = User.objects.all()
for user in allusers:
    now = datetime.now() - starttime
    if now.seconds > 3000:
        print("Ending: continue from ID=%s" % user.id)
        sys.exit()
    print(user)
    subs = user.subscription_set.all()
    for sub in subs:
        unreads = user.unreadcomic_set.filter(comic__exact=sub.comic).order_by('-id')
        if unreads.count() > 20:
            print(" %s %s" % (sub.comic, unreads.count()))
            sid = unreads[20].id
            deletes = user.unreadcomic_set.filter(comic__exact=sub.comic).order_by('-id').filter(id__lte=sid)
            deletes.delete()
    time.sleep(0.1)
