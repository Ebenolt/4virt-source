<?php
    session_start();
    set_include_path("./includes");
    require_once("header.php");

    if (key_exists('message', $_SESSION)){
        echo($_SESSION['message']);
        echo("\n");
        $_SESSION['message'] = "";
    }

    if (key_exists('vcsa_username',$_SESSION)){
        require_once("user_interface.php");
    } else {
        require_once("login.php");
    }

    require_once("footer.php");
?>
