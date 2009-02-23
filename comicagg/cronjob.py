#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, settings_local, threading, time
from traceback import *
from datetime import datetime

sys.path.insert(0, settings_local.ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = "comicagg.settings"

from comicagg.agregator.models import *
from django.core.mail import send_mail
from comicagg.agregator.check import check_comic

#check all comics
all = list(Comic.objects.all())
new = 0
no_change = 0
errors_active = list()
errors_inactive = list()

class CheckThread(threading.Thread):
	def __init__(self, all, errors_active, errors_inactive):
		threading.Thread.__init__(self)
		self.all = all
		self.errors_active = errors_active
		self.errors_inactive = errors_inactive

	def run(self):
		global new
		global no_change

		comic = self.next()
		while comic:
			h_obj = None
			try:
				h_obj = check_comic(comic)
			except KeyboardInterrupt:
				print '*** Matado %s ***' % (datetime.now())
				sys.exit()
			except NoMatchException:
				s = '   Error comprobando %s\n' % comic.name.encode('utf-8')
				if comic.activo:
					self.errors_active.append(s)
				else:
					self.errors_inactive.append(s)
				#continue
			except:
				#print_exc()
				s = '   Error inesperado %s: %s\n' % (comic.name.encode('utf-8'), sys.exc_info()[1])
				if comic.activo:
					self.errors_active.append(s)
				else:
					self.errors_inactive.append(s)
				#raise
				#continue
			if h_obj:
				new += 1
				#foreach user who has a subscription, create the unreadcomic object
				subscriptions = comic.subscription_set.all()
				for subscription in subscriptions:
					unread = UnreadComic.objects.get_or_create(user=subscription.user, history=h_obj, comic=subscription.comic)
				#si es un comic desactivado o terminado y se actualiza notificar posible activacion
				if not comic.activo or comic.ended:
					s = '  El desactivado o terminado %s se ha actualizado.\n' % (comic.name,)
					self.errors_inactive.append(s)
			else:
				no_change += 1
			comic = self.next()

	def next(self):
		print "%s: %d left" % (self.getName(), len(self.all))
		if len(self.all):
			return self.all.pop(0)

print '\n*** Ejecución de cronjob.py (%s) ***' % datetime.now()

salida = "Hora comienzo: %s\n" % datetime.now()
thread_list = list()
for i in xrange(6):
	t = CheckThread(all, errors_active, errors_inactive)
	thread_list.append(t)
	t.start()

for t in thread_list:
	t.join()

salida += "Comics activos\n"
for s in errors_active:
  salida += s

salida += "-------------------------\n"
salida += "Comics desactivados\n"
for s in errors_inactive:
  salida += s

salida += "%s nuevos, %s sin cambios, %s errores\n" % (new, no_change, (len(errors_active)+len(errors_inactive)))
salida += "Hora fin: %s\n" % datetime.now()

send_mail('[CA] Salida de la tarea de cron', salida, 'robot@comicagg.com', ['esu@kumomi.es'])
