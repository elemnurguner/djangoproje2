"""
ASGI config for ecommerce_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""
#Django projesinin  asynchronus  server getaway  interface (ASGI) giriş noktasıdır . Kısacası web sunucusu -->django uylamsı arasında  iletişimi sağlar

import os # işletim sistemi ile iletişimi sağlar

from django.core.asgi import get_asgi_application #django ya asgi uyumlu bir web aunucusu  üzerinden  bağlanmayı sağlar (daphe  yada  Uvicorn)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')#djangoya   hangi ayar dosyasının kullanıcıgını söyler ,ortam değişkenini  ayarla eğer zaten  ayarlanmışşsa değiştirilmez.

application = get_asgi_application()#get_Asgi_aplication  dajango uygulamsını  asgı protouloune uygın bir  aplication  callabe   nesnesine    donuşturur.
#asgı  djangonun  asenkron ozelliklerine   (web socket  ,bacground task   )hazır sunucu  arayuzdur  
