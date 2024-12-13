[33mcommit dc8787c6550d67b702aa79cca542f992c9c49087[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mhome[m[33m, [m[1;31morigin/home[m[33m)[m
Author: Jerome Rojas <skreamlight@gmail.com>
Date:   Wed Dec 4 18:18:39 2024 -0400

    home css hotfix

[1mdiff --git a/core/templates/layouts/base.html b/core/templates/layouts/base.html[m
[1mindex 68a2a9a..014d353 100644[m
[1m--- a/core/templates/layouts/base.html[m
[1m+++ b/core/templates/layouts/base.html[m
[36m@@ -23,9 +23,6 @@[m
                 {% if user_is_authenticated %}[m
                 <li><a href="{% url 'prestamos' %}">Préstamos</a></li>[m
                 <li><a href="#">Clientes</a></li>[m
[31m-                {% else %}[m
[31m-                <li><a class="custon-login" onclick="location.href="{% url 'login' %}">Iniciar Sesión</a></li>[m
[31m-                {% endif %}[m
             </ul>[m
             <ul class="logout-container">[m
                 <li>[m
[36m@@ -35,6 +32,11 @@[m
                     </form>[m
                 </li>[m
             </ul>[m
[32m+[m[32m            {% else %}[m
[32m+[m[32m            <ul class="logout-container">[m
[32m+[m[32m                <li><a class="custon-login" onclick="location.href="{% url 'login' %}">Iniciar Sesión</a></li>[m
[32m+[m[32m            </ul>[m
[32m+[m[32m                {% endif %}[m
         </nav>=[m
     </header>[m
 [m

[33mcommit d3e3bb728f40f0285a6929a6c159a5771b77e868[m
Author: Jerome Rojas <skreamlight@gmail.com>
Date:   Wed Dec 4 18:13:41 2024 -0400

    home css

[1mdiff --git a/core/static/css/base.css b/core/static/css/base.css[m
[1mindex 1b2fc2f..fd0bcd1 100644[m
[1m--- a/core/static/css/base.css[m
[1m+++ b/core/static/css/base.css[m
[36m@@ -31,6 +31,8 @@[m [mfooter {[m
     clear: both;[m
 }[m
 [m
[32m+[m
[32m+[m
 .logo img {[m
     width: 5vh;[m
 }[m
[36m@@ -40,15 +42,29 @@[m [mfooter {[m
     position: relative;[m
 }[m
 [m
[32m+[m[32mnav {[m
[32m+[m[32m    display: flex; /* Use flexbox for the nav */ /* Align items to the right */[m
[32m+[m[32m    width: 100%; /* Ensure nav takes full width */[m
[32m+[m[32m}[m
[32m+[m
 nav ul {[m
[31m-    display: flex; /* Use flexbox for layout */[m
[31m-    list-style-type: none; /* Remove bullet points */[m
[31m-    padding: 0; /* Remove padding */[m
[31m-    margin: 0; /* Remove margin */[m
[32m+[m[32m    display: flex;[m
[32m+[m[32m    flex: 1;[m
[32m+[m[32m    width: 100%;[m
[32m+[m[32m    justify-content: left;[m
[32m+[m[32m    text-align: center;[m
[32m+[m[32m    list-style: none;[m
[32m+[m[32m    margin: 0;[m
 }[m
 [m
 nav ul li {[m
[31m-    margin-right: 20px; /* Space between items */[m
[32m+[m[32m    margin-right: 20px;[m
[32m+[m[32m    align-content: center; /* Space between items */[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.logout-container {[m
[32m+[m[32m    justify-content: right;[m
[32m+[m[32m    margin-left: auto; /* Push the logout button to the right */[m
 }[m
 [m
 nav ul li a {[m
[36m@@ -88,10 +104,7 @@[m [mnav ul li a:hover {[m
     justify-content: center;[m
     align-items: center;[m
     height: 40vh; /* Centrar verticalmente */[m
[31m-    /* overflow-y: auto; /* Add this to enable vertical scrolling */[m
     max-width: 100%; /* Add this to prevent horizontal overflow */[m
[31m-    /*box-sizing: border-box; /* Add this to include padding and border in width calculation */[m
[31m-    /*overflow-x: auto;[m
 }[m
 [m
 /* login card */[m
[36m@@ -101,7 +114,6 @@[m [mnav ul li a:hover {[m
     justify-content: center;[m
     align-items: center;[m
     height: 100%; /* Centrar verticalmente */[m
[31m-    /*overflow-y: auto;  /*Add this to enable vertical scrolling */[m
     max-width: 100%; /* Add this to prevent horizontal overflow */[m
     box-sizing: border-box; /* Add this to include padding and border in width calculation */[m
 [m
[1mdiff --git a/core/templates/layouts/base.html b/core/templates/layouts/base.html[m
[1mindex d09a0cf..68a2a9a 100644[m
[1m--- a/core/templates/layouts/base.html[m
[1m+++ b/core/templates/layouts/base.html[m
[36m@@ -21,16 +21,20 @@[m
         <nav>[m
             <ul>[m
                 {% if user_is_authenticated %}[m
[31m-                <li><a href="prestamos">Préstamos</a></li>[m
[31m-                <li><a href="clientes">Clientes</a></li>[m
[31m-                <form method="POST" action="{% url 'logout' %}">[m
[31m-                    {% csrf_token %}[m
[31m-                    <li><a class="custon-login" type="submit">Cerrar Sesión</a></li>[m
[31m-                </form>[m
[32m+[m[32m                <li><a href="{% url 'prestamos' %}">Préstamos</a></li>[m
[32m+[m[32m                <li><a href="#">Clientes</a></li>[m
                 {% else %}[m
[31m-                <li><a class="custon-login" onclick="location.href='login';">Iniciar Sesión</a></li>[m
[32m+[m[32m                <li><a class="custon-login" onclick="location.href="{% url 'login' %}">Iniciar Sesión</a></li>[m
                 {% endif %}[m
             </ul>[m
[32m+[m[32m            <ul class="logout-container">[m
[32m+[m[32m                <li>[m
[32m+[m[32m                    <form method="POST" action="{% url 'logout' %}">[m
[32m+[m[32m                        {% csrf_token %}[m
[32m+[m[32m                        <button class="btn btn-danger" type="submit">Cerrar Sesión</button>[m
[32m+[m[32m                    </form>[m
[32m+[m[32m                </li>[m
[32m+[m[32m            </ul>[m
         </nav>=[m
     </header>[m
 [m
[1mdiff --git a/core/urls.py b/core/urls.py[m
[1mindex d3abcd8..93955af 100644[m
[1m--- a/core/urls.py[m
[1m+++ b/core/urls.py[m
[36m@@ -6,5 +6,5 @@[m [murlpatterns = [[m
     path('', views.home, name='home'),[m
     path('prestamos/', views.prestamos, name='prestamos'),[m
     path('login/', auth_views.LoginView.as_view(), name='login'),[m
[31m-    path('logout/', views.signout, name='logout'),[m
[32m+[m[32m    path('logout/', auth_views.LogoutView.as_view(), name='logout'),[m
 ][m
\ No newline at end of file[m
[1mdiff --git a/meprestamos/settings.py b/meprestamos/settings.py[m
[1mindex da604b2..7764f1f 100644[m
[1m--- a/meprestamos/settings.py[m
[1m+++ b/meprestamos/settings.py[m
[36m@@ -131,6 +131,7 @@[m [mMEDIA_URL = '/media/'[m
 DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'[m
 [m
 #URL REDIRECTS[m
[31m-[m
[31m-LOGIN_REDIRECT_URL = 'home'[m
[32m+[m[32mLOGIN_URL = 'login'[m
 LOGOUT_REDIRECT_URL = 'login'[m
[32m+[m[32mLOGIN_REDIRECT_URL = 'home'[m
[41m+[m

[33mcommit 452a2a73158d49fdaedc6db057dc15a3d47409fd[m
Author: Jerome Rojas <skreamlight@gmail.com>
Date:   Wed Dec 4 17:20:22 2024 -0400

    base css and header

[1mdiff --git a/core/models.py b/core/models.py[m
[1mindex 97ba6cb..19ad9bb 100644[m
[1m--- a/core/models.py[m
[1m+++ b/core/models.py[m
[36m@@ -5,8 +5,13 @@[m [mclass Clientes(models.Model):[m
     nombre = models.CharField(max_length=50)[m
     apellido = models.CharField(max_length=50)[m
     numero_telefono = models.CharField(max_length=11)[m
[32m+[m[32m    numero_local = models.CharField(max_length=11, default=None)[m
     cedula = models.CharField(max_length=12)[m
[31m-    ciudad = models.CharField(max_length=150)[m
[32m+[m[32m    rif = models.CharField(max_length=13, default='V1234567890')[m
[32m+[m[32m    direccion_1 = models.CharField(max_length=255, default='direccion')  # Mandatory field[m
[32m+[m[32m    direccion_2 = models.CharField(max_length=255, null=True, blank=True)  # Optional field[m
[32m+[m[32m    email_1 = models.EmailField(default=None)  # Mandatory field[m
[32m+[m[32m    email_2 = models.EmailField(null=True, blank=True)  # Optional field[m
     [m
     def __str__(self):[m
         return self.nombre[m
[36m@@ -21,4 +26,4 @@[m [mclass Prestamos(models.Model):[m
     [m
     def __str__(self):[m
         return f"Préstamo de {self.cliente} - Monto: {self.monto_prestamo}"[m
[31m-    [m
\ No newline at end of file[m
[32m+[m[41m    [m
[1mdiff --git a/core/static/css/base.css b/core/static/css/base.css[m
[1mnew file mode 100644[m
[1mindex 0000000..1b2fc2f[m
[1m--- /dev/null[m
[1m+++ b/core/static/css/base.css[m
[36m@@ -0,0 +1,222 @@[m
[32m+[m[32mbody {[m
[32m+[m[32m    font-family: Arial, sans-serif;[m
[32m+[m[32m    margin: 0;[m
[32m+[m[32m    padding: 0;[m
[32m+[m[32m    display: flex; /* Hacemos el body un flex container */[m
[32m+[m[32m    flex-direction: column; /* Ordenamos los elementos de arriba hacia abajo */[m
[32m+[m[32m    min-height: 100vh; /* Asegura que la altura del body sea al menos la altura de la viewport */[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32mheader {[m
[32m+[m[32m    background-color: #696969;[m
[32m+[m[32m    padding: 20px;[m
[32m+[m[32m    display: flex;[m
[32m+[m[32m    justify-content: space-between;[m
[32m+[m[32m    align-items: center;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32mmain {[m
[32m+[m[32m    display: flex;[m
[32m+[m[32m    flex-wrap: wrap;[m
[32m+[m[32m    justify-content: center;[m
[32m+[m[32m    padding: 2em;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32mfooter {[m
[32m+[m[32m    margin-top: auto;[m
[32m+[m[32m    background-color: #444;[m
[32m+[m[32m    color: #fff;[m
[32m+[m[32m    padding: 1em;[m
[32m+[m[32m    text-align: center;[m
[32m+[m[32m    clear: both;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.logo img {[m
[32m+[m[32m    width: 5vh;[m
[32m+[m[32m}[m
[32m+[m[32m/* menu */[m
[32m+[m
[32m+[m[32m.menu {[m
[32m+[m[32m    position: relative;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32mnav ul {[m
[32m+[m[32m    display: flex; /* Use flexbox for layout */[m
[32m+[m[32m    list-style-type: none; /* Remove bullet points */[m
[32m+[m[32m    padding: 0; /* Remove padding */[m
[32m+[m[32m    margin: 0; /* Remove margin */[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32mnav ul li {[m
[32m+[m[32m    margin-right: 20px; /* Space between items */[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32mnav ul li a {[m
[32m+[m[32m    text-decoration: none; /* Remove underline from links */[m
[32m+[m[32m    color: white; /* Link color */[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32mheader nav ul li a.custom-login-link {[m
[32m+[m[32m    color: yourColor; /* Replace with your desired color */[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32mnav ul li a:hover {[m
[32m+[m[32m    color: white;[m
[32m+[m[32m    text-decoration: underline; /* Underline on hover */[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.show {[m
[32m+[m[32m    display:grid;[m
[32m+[m[32m}[m
[32m+[m[32m.main-card {[m
[32m+[m[32m    background-color: #ffffff;[m
[32m+[m[32m    padding: 4vmin;[m
[32m+[m[32m    margin-top: 3vh;[m
[32m+[m[32m    margin-bottom: 3vh;[m
[32m+[m[32m    border: 1px solid #ccc;[m
[32m+[m[32m    border-radius: 15px;[m
[32m+[m[32m    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);[m
[32m+[m[32m    width: 100%;[m
[32m+[m[32m    height: 70vh;[m
[32m+[m[32m    max-width: 80vw; /* Ancho máximo de la tarjeta */[m
[32m+[m[32m    overflow-y: auto;[m
[32m+[m[32m    display: auto;[m
[32m+[m[32m}[m
[32m+[m[32m/* main card */[m
[32m+[m[32m.container-login {[m
[32m+[m[32m    display: flex;[m
[32m+[m[32m    justify-content: center;[m
[32m+[m[32m    align-items: center;[m
[32m+[m[32m    height: 40vh; /* Centrar verticalmente */[m
[32m+[m[32m    /* overflow-y: auto; /* Add this to enable vertical scrolling */[m
[32m+[m[32m    max-width: 100%; /* Add this to prevent horizontal overflow */[m
[32m+[m[32m    /*box-sizing: border-box; /* Add this to include padding and border in width calculation */[m
[32m+[m[32m    /*overflow-x: auto;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m/* login card */[m
[32m+[m[32m.login-card {[m
[32m+[m[32m    display: block;[m
[32m+[m[32m    flex-direction: column;[m
[32m+[m[32m    justify-content: center;[m
[32m+[m[32m    align-items: center;[m
[32m+[m[32m    height: 100%; /* Centrar verticalmente */[m
[32m+[m[32m    /*overflow-y: auto;  /*Add this to enable vertical scrolling */[m
[32m+[m[32m    max-width: 100%; /* Add this to prevent horizontal overflow */[m
[32m+[m[32m    box-sizing: border-box; /* Add this to include padding and border in width calculation */[m
[32m+[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.login-card h2 {[m
[32m+[m[32m    margin-bottom: 20px; /* Add some space between the h2 and the form */[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.login-card form {[m
[32m+[m[32m    display: block;[m
[32m+[m[32m    flex: 1;[m
[32m+[m[32m    flex-direction: column;[m
[32m+[m[32m    align-items: center;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.login-card th {[m
[32m+[m[32m    background-color: #f2f2f2;[m
[32m+[m[32m    cursor: pointer;[m
[32m+[m[32m    background-repeat: no-repeat;[m
[32m+[m[32m    background-position: center right;[m
[32m+[m[32m    padding-right: 21px;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.login-card label {[m
[32m+[m[32m    margin-bottom: 10px;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.form-group p {[m
[32m+[m[32m    align-items: left;[m
[32m+[m[32m    margin-bottom: 5vh;[m
[32m+[m[32m    text-align: left;[m
[32m+[m[32m    width: 100%;[m
[32m+[m[32m    padding: 10px;[m
[32m+[m[32m    border-radius: 5px;[m
[32m+[m[32m    border: 1px solid #ccc;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.form-group input {[m
[32m+[m[32m    width: 94%; /* Hacer que los campos ocupen todo el ancho */[m
[32m+[m[32m    padding: 10px;[m
[32m+[m[32m    border-radius: 5px;[m
[32m+[m[32m    border: 1px solid #ccc;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m/* boostrap buttons */[m
[32m+[m[32m.btn:hover {[m
[32m+[m[32m    background-color: #0056b3;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.btn-primary {[m
[32m+[m[32m    background-color: #007bff;[m
[32m+[m[32m    color: white;[m
[32m+[m[32m}[m
[32m+[m[32m.btn-primary:hover {[m
[32m+[m[32m    background-color: #0062cc;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.btn-secondary {[m
[32m+[m[32m    background-color: #949ca2;[m
[32m+[m[32m    color: white;[m
[32m+[m[32m}[m
[32m+[m[32m.btn-secondary:hover {[m
[32m+[m[32m    background-color: #545b62;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.btn-success {[m
[32m+[m[32m    background-color: #28a745;[m
[32m+[m[32m    color: white;[m
[32m+[m[32m}[m
[32m+[m[32m.btn-success:hover {[m
[32m+[m[32m    background-color: #208038;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.btn-danger {[m
[32m+[m[32m    background-color: #dc3545;[m
[32m+[m[32m    color: white;[m
[32m+[m[32m}[m
[32m+[m[32m.btn-danger:hover {[m
[32m+[m[32m    background-color: #c82333;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.btn-warning {[m
[32m+[m[32m    background-color: #ffc107;[m[41m  [m
[32m+[m
[32m+[m[32m    color: black;[m
[32m+[m[32m}[m
[32m+[m[32m.btn-warning:hover {[m
[32m+[m[32m    background-color: #d39e00;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.btn-info {[m
[32m+[m[32m    background-color: #b7d5d4;[m
[32m+[m[32m    color: white;[m
[32m+[m[32m}[m
[32m+[m[32m.btn-info:hover {[m
[32m+[m[32m    background-color: #117a8b;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m/* sort table or list */[m
[32m+[m
[32m+[m[32mth.sort-asc {[m
[32m+[m[32m    background-image: url(/static/img/sort_up.svg);[m
[32m+[m[32m    background-repeat: no-repeat;[m
[32m+[m[32m    background-position: center right;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32mth.sort-desc {[m
[32m+[m[32m    background-image: url(/static/img/sort_down.svg);[m
[32m+[m[32m    background-repeat: no-repeat;[m
[32m+[m[32m    background-position: center right;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32mth.sort-both {[m
[32m+[m[32m    background-image: url(/static/img/sort_both.svg);[m
[32m+[m[32m    background-repeat: no-repeat;[m
[32m+[m[32m    background-position: center right;[m
[32m+[m[32m}[m
\ No newline at end of file[m
[1mdiff --git a/core/static/css/styles.css b/core/static/css/styles.css[m
[1mdeleted file mode 100644[m
[1mindex 0f51cf7..0000000[m
[1m--- a/core/static/css/styles.css[m
[1m+++ /dev/null[m
[36m@@ -1,292 +0,0 @@[m
[31m-body {[m
[31m-    font-family: Arial, sans-serif;[m
[31m-    margin: 0;[m
[31m-    padding: 0;[m
[31m-    display: flex; /* Hacemos el body un flex container */[m
[31m-    flex-direction: column; /* Ordenamos los elementos de arriba hacia abajo */[m
[31m-    min-height: 100vh; /* Asegura que la altura del body sea al menos la altura de la viewport */[m
[31m-}[m
[31m-[m
[31m-[m
[31m-header {[m
[31m-    background-color: #f0f0f0;[m
[31m-    padding: 2vmin;[m
[31m-    display: flex;[m
[31m-    justify-content: space-between;[m
[31m-    align-items: center;[m
[31m-}[m
[31m-[m
[31m-footer {[m
[31m-    margin-top: auto; /* Empuja el footer al final */[m
[31m-    background-color: #f0f0f0;[m
[31m-    padding: 1vmin;[m
[31m-    display: flex;[m
[31m-    justify-content: space-between;[m
[31m-    align-items: center;[m
[31m-}[m
[31m-[m
[31m-.logo img {[m
[31m-    width: 10vw;[m
[31m-}[m
[31m-[m
[31m-/* alternar modo claro y oscuro [m
[31m-.mode-toggle img {[m
[31m-    cursor: pointer;[m
[31m-    width: 25px;  [m
[31m-} */[m
[31m-[m
[31m-.menu {[m
[31m-    position: relative;[m
[31m-}[m
[31m-[m
[31m-.menu img {[m
[31m-    cursor: pointer;[m
[31m-    width: 2vw;[m
[31m-}[m
[31m-[m
[31m-.menu-items {[m
[31m-    display: none;[m
[31m-    border-radius: 15px;[m
[31m-    position: absolute;[m
[31m-    padding: 2vmin;[m
[31m-    background-color: #f9f9f9;[m
[31m-    min-width: 8vw;[m
[31m-    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);[m
[31m-    z-index: 1;[m
[31m-    right: 0;[m
[31m-    text-align: right;[m
[31m-}[m
[31m-[m
[31m-.show {[m
[31m-    display:grid;[m
[31m-}[m
[31m-[m
[31m-.container-login {[m
[31m-    display: flex;[m
[31m-    justify-content: center;[m
[31m-    align-items: center;[m
[31m-    height: 80vh; /* Centrar verticalmente */[m
[31m-    overflow-y: auto; /* Add this to enable vertical scrolling */[m
[31m-    max-width: 100%; /* Add this to prevent horizontal overflow */[m
[31m-    box-sizing: border-box; /* Add this to include padding and border in width calculation */[m
[31m-    overflow-x: auto;[m
[31m-}[m
[31m-[m
[31m-.container-proveedores {[m
[31m-    display: flex;[m
[31m-    flex-grow: 1; /* make the container flexible */[m
[31m-    justify-content: center;[m
[31m-    align-items: center;[m
[31m-    height: 80vh;[m
[31m-    overflow-y: auto;[m
[31m-    overflow-x: auto;[m
[31m-    max-width: 100%;[m
[31m-    box-sizing: border-box;[m
[31m-}[m
[31m-[m
[31m-.container-inventario {[m
[31m-    display: flex;[m
[31m-    justify-content: center;[m
[31m-    align-items: center;[m
[31m-    height: auto;[m
[31m-}[m
[31m-[m
[31m-.container-update {[m
[31m-    display: flex;[m
[31m-    justify-content: center;[m
[31m-    align-items: center;[m
[31m-    height: auto;[m
[31m-}[m
[31m-[m
[31m-.login-card {[m
[31m-    background-color: #ffffff;[m
[31m-    padding: 6vmin;[m
[31m-    border: 1px solid #e5e5e5;[m
[31m-    border-radius: 15px;[m
[31m-    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);[m
[31m-    max-width: 100% ; /* Ancho máximo de la tarjeta */[m
[31m-    text-align: center;  /* Centramos el título */[m
[31m-    display: block;[m
[31m-    overflow-y: auto;[m
[31m-}[m
[31m-[m
[31m-.inventario-card {[m
[31m-    background-color: #ffffff;[m
[31m-    padding: 4vmin;[m
[31m-    margin-top: 3vh;[m
[31m-    margin-bottom: 3vh;[m
[31m-    border: 1px solid #e5e5e5;[m
[31m-    border-radius: 15px;[m
[31m-    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);[m
[31m-    width: 100%;[m
[31m-    max-width: 80vw; /* Ancho máximo de la tarjeta */[m
[31m-    text-align: center;  /* Centramos el título */[m
[31m-    overflow-y: auto;[m
[31m-    display: auto;[m
[31m-}[m
[31m-[m
[31m-.update-card {[m
[31m-    background-color: #ffffff;[m
[31m-    padding: 6vmin;[m
[31m-    border: 1px solid #e5e5e5;[m
[31m-    border-radius: 15px;[m
[31m-    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);[m
[31m-    width: 100%;[m
[31m-    max-width: 35vw; /* Ancho máximo de la tarjeta */[m
[31m-    text-align: center;  /* Centramos el título */[m
[31m-    display: block;[m
[31m-}[m
[31m-[m
[31m-.inventario-card .form-group {[m
[31m-    display: grid;[m
[31m-[m
[31m-}[m
[31m-[m
[31m-.login-card h2,[m
[31m-.inventario-card h2,[m
[31m-.inventario-card h1 {[m
[31m-    margin-bottom: 1.5vh;[m
[31m-    font-size: 6vmin;[m
[31m-}[m
[31m-[m
[31m-.inventario-card table,[m
[31m-.login-card table{[m
[31m-    width: 100%;[m
[31m-    border-collapse: collapse;[m
[31m-    margin-bottom: 2vh;[m
[31m-    margin-right: 2vh;[m
[31m-}[m
[31m-[m
[31m-.login-card th,[m
[31m-.login-card td, [m
[31m-.inventario-card th,[m
[31m-.inventario-card td {[m
[31m-    padding: 1vmin 2vmin;[m
[31m-    text-align: left;[m
[31m-    border-bottom: 2px solid #ddd;[m
[31m-}[m
[31m-[m
[31m-.buttons-div {[m
[31m-    text-align: center;[m
[31m-}[m
[31m-.inventario-card th,[m
[31m-.login-card th {[m
[31m-    background-color: #f2f2f2;[m
[31m-    cursor: pointer;[m
[31m-    background-repeat: no-repeat;[m
[31m-    background-position: center right;[m
[31m-    padding-right: 21px;[m
[31m-}[m
[31m-[m
[31m-th.sort-asc {[m
[31m-    background-image: url(/static/img/sort_up.svg);[m
[31m-    background-repeat: no-repeat;[m
[31m-    background-position: center right;[m
[31m-}[m
[31m-[m
[31m-th.sort-desc {[m
[31m-    background-image: url(/static/img/sort_down.svg);[m
[31m-    background-repeat: no-repeat;[m
[31m-    background-position: center right;[m
[31m-}[m
[31m-[m
[31m-th.sort-both {[m
[31m-    background-image: url(/static/img/sort_both.svg);[m
[31m-    background-repeat: no-repeat;[m
[31m-    background-position: center right;[m
[31m-}[m
[31m-.inventario-card td,[m
[31m-.login-card td {[m
[31m-    font-size: 3vmin;[m
[31m-}[m
[31m-[m
[31m-.form-group {[m
[31m-    margin-bottom: 5vh;[m
[31m-    text-align: left; /* Alinear los campos del formulario a la izq */[m
[31m-}[m
[31m-[m
[31m-.form-group input,[m
[31m-.form-group textarea {[m
[31m-    width: 94%; /* Hacer que los campos ocupen todo el ancho */[m
[31m-    padding: 10px;[m
[31m-    border-radius: 5px;[m
[31m-    border: 1px solid #ccc;[m
[31m-}[m
[31m-[m
[31m-.form-group select {[m
[31m-    width: 92%; /* Hacer que los campos ocupen todo el ancho */[m
[31m-    padding: 10px;[m
[31m-    border-radius: 5px;[m
[31m-    border: 1px solid #ccc;[m
[31m-}[m
[31m-[m
[31m-.btn {[m
[31m-    padding: 10px 15px;[m
[31m-    border: none;[m
[31m-    border-radius: 5px;[m
[31m-    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);[m
[31m-    cursor: pointer;[m
[31m-    margin: 6px;[m
[31m-}[m
[31m-[m
[31m-.form-group p {[m
[31m-    margin-bottom: 5vh;[m
[31m-    text-align: left; /* Alinear los campos del formulario a la derecha */[m
[31m-    width: 97%; /* Hacer que los campos ocupen todo el ancho */[m
[31m-    padding: 10px;[m
[31m-    border-radius: 5px;[m
[31m-    border: 1px solid #ccc;[m
[31m-}[m
[31m-[m
[31m-.btn:hover {[m
[31m-    background-color: #0056b3;[m
[31m-}[m
[31m-[m
[31m-.btn-primary {[m
[31m-    background-color: #007bff;[m
[31m-    color: white;[m
[31m-}[m
[31m-.btn-primary:hover {[m
[31m-    background-color: #0062cc;[m
[31m-}[m
[31m-[m
[31m-.btn-secondary {[m
[31m-    background-color: #949ca2;[m
[31m-    color: white;[m
[31m-}[m
[31m-.btn-secondary:hover {[m
[31m-    background-color: #545b62;[m
[31m-}[m
[31m-[m
[31m-.btn-success {[m
[31m-    background-color: #28a745;[m
[31m-    color: white;[m
[31m-}[m
[31m-.btn-success:hover {[m
[31m-    background-color: #208038;[m
[31m-}[m
[31m-[m
[31m-.btn-danger {[m
[31m-    background-color: #dc3545;[m
[31m-    color: white;[m
[31m-}[m
[31m-.btn-danger:hover {[m
[31m-    background-color: #c82333;[m
[31m-}[m
[31m-[m
[31m-.btn-warning {[m
[31m-    background-color: #ffc107;  [m
[31m-[m
[31m-    color: black;[m
[31m-}[m
[31m-.btn-warning:hover {[m
[31m-    background-color: #d39e00;[m
[31m-}[m
[31m-[m
[31m-.btn-info {[m
[31m-    background-color: #17a2b8;[m
[31m-    color: white;[m
[31m-}[m
[31m-.btn-info:hover {[m
[31m-    background-color: #117a8b;[m
[31m-}[m
\ No newline at end of file[m
[1mdiff --git a/core/static/img/logo.png b/core/static/img/logo.png[m
[1mnew file mode 100644[m
[1mindex 0000000..cb5f0fb[m
Binary files /dev/null and b/core/static/img/logo.png differ
[1mdiff --git a/core/static/img/menu.svg b/core/static/img/menu.svg[m
[1mnew file mode 100644[m
[1mindex 0000000..d915b79[m
[1m--- /dev/null[m
[1m+++ b/core/static/img/menu.svg[m
[36m@@ -0,0 +1 @@[m
[32m+[m[32m<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="#9a9996" d="M0 96C0 78.3 14.3 64 32 64l384 0c17.7 0 32 14.3 32 32s-14.3 32-32 32L32 128C14.3 128 0 113.7 0 96zM0 256c0-17.7 14.3-32 32-32l384 0c17.7 0 32 14.3 32 32s-14.3 32-32 32L32 288c-17.7 0-32-14.3-32-32zM448 416c0 17.7-14.3 32-32 32L32 448c-17.7 0-32-14.3-32-32s14.3-32 32-32l384 0c17.7 0 32 14.3 32 32z"/></svg>[m
\ No newline at end of file[m
[1mdiff --git a/core/static/img/moon.svg b/core/static/img/moon.svg[m
[1mnew file mode 100644[m
[1mindex 0000000..4a0d2c0[m
[1m--- /dev/null[m
[1m+++ b/core/static/img/moon.svg[m
[36m@@ -0,0 +1,7 @@[m
[32m+[m[32m<?xml version="1.0" encoding="iso-8859-1"?>[m
[32m+[m[32m<!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->[m
[32m+[m[32m<svg height="800px" width="800px" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"[m[41m [m
[32m+[m	[32m viewBox="0 0 56 56" xml:space="preserve">[m
[32m+[m[32m<path style="fill:#A5A5A4;" d="M29,28c0-11.917,7.486-22.112,18-26.147C43.892,0.66,40.523,0,37,0C21.561,0,9,12.561,9,28[m
[32m+[m	[32ms12.561,28,28,28c3.523,0,6.892-0.66,10-1.853C36.486,50.112,29,39.917,29,28z"/>[m
[32m+[m[32m</svg>[m
\ No newline at end of fil