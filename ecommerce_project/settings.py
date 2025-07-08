from pathlib import Path #pathlib   modern yol işlemlerii çin kullanırlır   klasor ve dosya yolları     
import os #sistem  yolu klasor işlemleri için kullanılır
from decouple import config,Csv # decouple  .env dosyası üzerinden  gizli  ayarları  (şifre ,key) okumak için kullanılır / csv  ise .env den liste okumayı sağlar

BASE_DIR = Path(__file__).resolve().parent.parent #projenin ana dizini ,setting.py neredeyse onun ik üstüne  çık 


# reCAPTCHA anahtarlarını .env’den al
RECAPTCHA_SITE_KEY   = config('RECAPTCHA_PUBLIC_KEY')#both işlerimi koruması  için kullanıyoruz  buda  .env  dosyasından  alır bilgireini
RECAPTCHA_SECRET_KEY = config('RECAPTCHA_PRIVATE_KEY')
# ===============================
# ENV
# ===============================

SECRET_KEY = config('SECRET_KEY')#djangonun en onemli şifreleme anahtarı    
DEBUG = config('DEBUG', default=False, cast=bool) #debug  modu  .env dosyasından alır , eğer yoksa False olarak ayarlanırgeliştirici moduu açıp kapatır.
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1', cast=Csv())#hangi domainlerden erişim izbni var  herbirini   .env en  alır

# ===============================
# LOGIN / LOGOUT
# ===============================

LOGIN_REDIRECT_URL = '/'#giriş yaptıktan sonra  nereye      
LOGOUT_REDIRECT_URL = '/users/login/'#çıkış yaptıktan sonra  nereye  gideceğini söyler 
LOGIN_URL = '/users/login/'

# ===============================
# MEDIA
# ===============================

MEDIA_URL = '/media/' #kullanıcıın  yuklediği dosyaların yoluu belirtir 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ===============================
# STATIC
# ===============================

STATIC_URL = '/static/'#css javascprit gibi  sabit dosyalar buraya 
STATICFILES_DIRS = [ BASE_DIR / 'static' ] #dev aşamasında ki staticleri burada 

# ===============================
# Installed Apps
# ===============================

INSTALLED_APPS = [ #djangonun yuklu uygulamalrı  her apps -->  kendi  models/views  / templates yapısına sahip
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'users',
    
]

# ===============================
# Middleware
# ===============================

MIDDLEWARE = [#djangod a istek yanıt zincirinde araya gire  aktmanlar   güvenlik oturum   çeviri  crf  koruması gibi 
    'django.middleware.security.SecurityMiddleware',# temel  güvenlik başlıklarını ayarlar  ,ssl yönlendirmesi  ,güvenlik duvarı gibi kısacası tarayıcı   server iletiişmini daha  güvenli yapar
    'django.contrib.sessions.middleware.SessionMiddleware',#djangonun session sistemi çalışssın  diye  ,kullnıcının oturum  bilgisini otomatikmen  cokike de  saklar  istek kullnıcının sessionı yukler  yanıt  -->  sesionı  cookie  ye yazar    kısaca  kullnıcı  login mi  ,sepetinde  urun varmı ,oturum verisi  burada   neden başta   sonraki middle weare  ler   oturum bilgisine ihtiyaç duyar 
    'django.middleware.locale.LocaleMiddleware',#çok  dilli destek sağlar  ,kulllanıcını eksept  language  başlığına  ve sesion /cookie ye bakar  ,dajangoya hangi dilde  içerik  le doneceğin soyler 
    'django.middleware.common.CommonMiddleware',#ayar yapar wwww olmayan dosyaları  bu şekilde  yapar  ,kısaca url yapısını  temiz  ,tutarlı  hale getiriri 
    'django.middleware.csrf.CsrfViewMiddleware',#crf saldırılarını karşı korurur   form o-post  isteklerinde  CRF token  kontrolu yapar ,korumasız  formlardan siteye veri gonderilmesini engeller  ,kısaca  kullnıcının  kimliğini burunup kotu işlemler  yapılmasını  onler 
    'django.contrib.auth.middleware.AuthenticationMiddleware',#kullnıcının  kim  oldugunu  django  ua soyler 
    'django.contrib.messages.middleware.MessageMiddleware',#djangonun messaj sistemni  ekileştirir, kısaca  başarıyla  giriş yaptıınz  gibi  flash mesajlar sağlar ,nedne  auth den sorna  kulllnaıcı kimliğine gore  mesaj atabilsin diye 
    'django.middleware.clickjacking.XFrameOptionsMiddleware',# x-frame -options  :same origon  headeriını ekler  ,bşaka sitelerin senin  stene   iframe  gommesin engeller   clicjackin  saldırılarını akarşı koruma sağlar kısaca kullnıcıyı kandırıp  butonlara tıklatma saldırılarını engeller ,header eklemek için yanıtın en sonun da yapılır 
]

ROOT_URLCONF = 'ecommerce_project.urls'#ana  url yonlendirme  dosyası  tüm app lerin urlleri buraya  bağlanır 

# ===============================
# Templates
# ===============================

TEMPLATES = [ #şablon motru ayarları  ,global  templates kalsoru   belirtir,örneğin base.html  burda  olur 
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce_project.wsgi.application'#djangonun  klasik wsgi sunucu  için giriş noktası  ,prodı-oction da  gunicorn  gibi  sunucular kullnılır 

# ===============================
# Database
# ===============================

DATABASES = {#database  ayarı burda  basit  sl lite  var geliştirme ayarı 
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ===============================
# Password Validators
# ===============================

AUTH_PASSWORD_VALIDATORS = [#şifre  karmaşıklığı kontrolleri   ,güvenliği artırır
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',#şifre  kullnıcı adı  ,soyadı ,emaili gibi  verileri benziyormu ,en kritik kontrol kullnıc adını içeren şifre  neden 1. sırada   kullnıcının birebir veya çok benzeyen şifre seçmesini engeller
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',#şifrenin en az kaç karakter oldugunu denetler /neden  ikinc isırada   benzersizlikten sonra   uzunluk kritik  çok kısa  şifreleri direkt eler 
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',#çok yaygın  kolay tahmin edilebilir şifreleri engeller ,neden  3. sırada  önceki ,kiyi geçen ama  hala tahmin edilebilir  şifreleri eler   kullanıcı  uzun yazsa da bilenen bir şey se yasak
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',#sadece rakamlardan oluşan şifreleri engeller ,neden  4. sırada  çünkü sadece rakamlar  çok zayıf  şifrelerdir ,en azından harf içermeli
    },
]

# ===============================
# Internationalization
# ===============================
#çoklu dil desteği  ,varsayılan dil Türkçe olarak ayarlandı
LANGUAGE_CODE = 'tr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('tr', 'Türkçe'),
]
#dil  dosyalarının  yolu .po/.mo  çeviri dosylarını   burada  tutar 
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# ===============================
# EMAIL Settings
# ===============================
#smtp ayarlaır  kullnıcı aktivasyon şifre sıfırlama ,email  atmak için kullnılır ,şifreler .env de gizli 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ===============================
# reCAPTCHA Settings
# ===============================
#formlarda  bot koruması  için kullanılır 
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')

# ===============================
# JWT (Future Use)
# ===============================

JWT_SECRET = config('JWT_SECRET')#henuz aktifdeğil ileride api auth için  hazır.

# ===============================
# Default PK Field
# ===============================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'# django 3.2 sonrası  varsayılan  pk alan tipi  ,otomatik buyuk integer 