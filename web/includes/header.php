<html lang="fr">
    <head>
        <meta charset="UTF-8">
        <html lang="en">
        <meta name="theme-color" content="#00CEEE"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="style/normalize.css">
        <link rel="stylesheet" href="style/custom.css">
        <link href="https://fonts.googleapis.com/css?family=Montserrat&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <?php
            if (key_exists('vcsa_username', $_SESSION)){
                echo("<title>Cloudis - ".$_SESSION['vcsa_username']."</title>");
            } else {
                echo("<title>Cloudis - Login</title>");
            }
        ?>
    </head>