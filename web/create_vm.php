<?php

?>

<html>
    <body>
        <h1>Création d'une VM</h1>
        <form>
        <p>Name :</p>
        <input type="text">
        <p>IP (facultatif):</p>
        <input type="text">
        <br><br>
        <label for="modele">Modèle : </label>
        <select id="modele">
            <option value="">--Please choose an option--</option>
            <option value="w10-Template">W10-Template</option>
        </select>
        <br><br> 
        <input type="submit" value="Create">
        </form>
    </body>
</html>