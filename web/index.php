<?php 

?>

<html>
    <head>
        <title>WEB INTERFACE</title>
    </head>
    <body>
        <h1>Liste des VM</h1>

        <div id="vm">
            <p>Name :</p>
            
            <p>IP :</p>
            <p>Statut :</p>
            <p>Date de la dernière sauvegarde :</p>

            <button value="delete">Delete</button>
            <button value="restart">Restart</button>
            <button value="add">Add</button>

            <label for="modele">Modèle : </label>
            <select id="modele">
                <option value="">--Please choose an option--</option>
                <option value="w10-Template">W10-Template</option>
            </select>     
        </div>
    </body>
</html>




<!-- // Les clients doivent pouvoir se connecter avec leurs comptes Active Directory sur l'interface.

// Il assurera certaines fonctionnalités :

// Affichez la liste des VM avec les informations suivantes :
// Nom
// IP
// Statut : Marche/Arrêt
// Date de la dernière sauvegarde
// Supprimer une VM choisie
// Redémarrer une VM choisie
// Ajoutez une nouvelle VM :
// Nom n
// IP si besoin