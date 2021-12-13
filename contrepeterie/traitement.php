<!DOCTYPE html>
<html>
   <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-sale=1, schrink-to-fit=no">
      <link rel="shortcut icon" href="image/favicon.png" type="image/x-icon">
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
      <link rel="stylesheet" href="css/style.css">
      <title>Contrepéterie</title>
   </head>
   <body>
      <nav id="nvbar" class="navbar navbar-expand-lg navbar-light bg-lignt sticky-top">
         <a class="navbar-brand" href="index.html">
         <span class="border rounded ml-5 pt-2 pb-1 pl-1 pr-1">
         <img src="image/Contrepéterie.png"  class="d-inline-block align-top logoM">
         </span>
         </a>  
         <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
         <span class="navbar-toggler-icon my-toggler"></span>
         </button>
         <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
            <ul class="navbar-nav navbar-tabs">
               <li class="nav-item mr-3">
                  <a class="nav-link font" href="index.html">Présentation</a>
               </li>
                          
               <li class="nav-item mr-3">
                  <a class="nav-link font" href="contrepeterie.html">Exemple</a>
               </li>
             
               <li class="nav-item mr-5">
                  <a class="nav-link font" href="contact.html">Contact</a>
               </li>
                <form class="form-inline">
                  <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
                  <button id="search" class="btn btn-outline-dark my-2 my-sm-0" type="submit">Search</button>
              </form>
            </ul>
         </div>
      </nav>
      
      <section>
         <?php
            if(isset($_POST)['prenom'] && isset($_POST)['nom'] && isset($_POST)['email'] && isset($_POST)['objet'] && isset($_POST)['message'])){
               if(!empty('prenom') && !empty('nom') && !empty('email') && !empty('objet') && !empty('message')){
                  if filter_var($_POST['email'], FILTER_VALIDATE_EMAIL){
                     echo "<p>Voici le résultat du remplissage du formulaire</p>";
                        echo "<p>Prénom : ", $_POST['prenom'] . "</p>";
                        echo "<p>Nom : " . $_POST['nom'] . "</p>";
                        echo "<p>Adresse Mail : " . $_POST['mail'] . "</p>";
                        if ($_POST['objet']) {
                           $objet=$_POST['objet'];
                           echo "Objet : $objet";
                        }
                        if($_POST['message'])
                        {
                           $message=$_POST['message'] ;
                           echo "Message : $message";
                        }
                        echo "<p>Votre demande a été pris en compte !</p>";
                        echo "<p><a href='index.html'>Retour vers le site</a></p>";
                  }
                  else{
                     echo("L'adresse email saisie est invalide");
                     echo("Resaisir une adresse email valide");
               }
            }
            else{
               echo "<p>Vous devez remplir le formulaire à l'adresse suivante : <a href='contact.html'>Formulaire</a></p>";
            }
         ?>
      </section>
       <footer class="bg-dark bandeN">   
         <div>
            <p id="footer">
               Copyright © 2019 Contrepéterie / Confidentialité et sécurité / Mentions
            </p>
         </div>
       </footer>
   </body>
   <script src="https://code.jquery.com/jquery-3.3.1.min.js"
      crossorigin="anonymous"></script>
   <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" crossorigin="anonymous"></script>
   <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" crossorigin="anonymous"></script>
</html>
