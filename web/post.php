<?php
    session_start();

    $home_page = $_SERVER['REQUEST_SCHEME']."://".$_SERVER['HTTP_HOST'];

    $username = "";
    $password = "";
    $action = "";
    $elem_id = "";

    switch(htmlspecialchars($_POST['action'])){
        case "login":
            if (key_exists('username', $_POST)){
                $username = htmlspecialchars($_POST['username']);
            }
            if (key_exists('password', $_POST)){
                $password = htmlspecialchars($_POST['password']);
            }

            if ( ($username != "") and ($password != "")){
                $return = [];
                exec("python3 get_token.py ".$username." ".$password, $return);
            
                $result = json_decode($return[0], true);

                if ($result["success"]){
                    $_SESSION['vcsa_username'] = $result['message']['username'];
                    $_SESSION['vcsa_password'] = $result['message']['password'];
                    $_SESSION['vcsa_token'] = $result['message']['token'];
                    $reply = array(
                        'success' => true,
                        'message' => "Login success"
                    );
                    echo(json_encode($reply));
                } else {
                    $reply = array(
                        'success' => false,
                        'message' => $result['message']
                    );
                    echo(json_encode($reply));
                }
            } else {
                $reply = array(
                    'success' => false,
                    'message' => "Missing args"
                );
                echo(json_encode($reply));
            }
            break;

        case "vm_power_up":
            if (key_exists('id', $_POST)){
                $elem_id = htmlspecialchars($_POST['id']);
            }

            if ( ($elem_id != "") ){
                $return = [];
                $command = "python3 management.py -u ".$_SESSION['vcsa_username']." -p ".$_SESSION['vcsa_password']." -t ".$_SESSION['vcsa_token']." -a start -e ".$elem_id;

                exec($command, $return);
            
                $result = json_decode($return[0], true);
                $reply = array(
                    'success' => $result["success"],
                    'message' => $result["message"]
                );
                echo(json_encode($reply));
            } else {
                $reply = array(
                    'success' => false,
                    'message' => "Missing args"
                );
                echo(json_encode($reply));
            }
            break;

        case "vm_power_off":
            if (key_exists('id', $_POST)){
                $elem_id = htmlspecialchars($_POST['id']);
            }

            if ( ($elem_id != "") ){
                $return = [];
                $command = "python3 management.py -u ".$_SESSION['vcsa_username']." -p ".$_SESSION['vcsa_password']." -t ".$_SESSION['vcsa_token']." -a stop -e ".$elem_id;

                exec($command, $return);
            
                $result = json_decode($return[0], true);
                $reply = array(
                    'success' => $result["success"],
                    'message' => $result["message"]
                );
                echo(json_encode($reply));
            } else {
                $reply = array(
                    'success' => false,
                    'message' => "Missing args"
                );
                echo(json_encode($reply));
            }
            break;

        case "vm_power_reset":
            if (key_exists('id', $_POST)){
                $elem_id = htmlspecialchars($_POST['id']);
            }

            if ( ($elem_id != "") ){
                $return = [];
                $command = "python3 management.py -u ".$_SESSION['vcsa_username']." -p ".$_SESSION['vcsa_password']." -t ".$_SESSION['vcsa_token']." -a reset -e ".$elem_id;

                exec($command, $return);
            
                $result = json_decode($return[0], true);
                $reply = array(
                    'success' => $result["success"],
                    'message' => $result["message"]
                );
                echo(json_encode($reply));
            } else {
                $reply = array(
                    'success' => false,
                    'message' => "Missing args"
                );
                echo(json_encode($reply));
            }
            break;

        case "vm_power_suspend":
            if (key_exists('id', $_POST)){
                $elem_id = htmlspecialchars($_POST['id']);
            }

            if ( ($elem_id != "") ){
                $return = [];
                $command = "python3 management.py -u ".$_SESSION['vcsa_username']." -p ".$_SESSION['vcsa_password']." -t ".$_SESSION['vcsa_token']." -a suspend -e ".$elem_id;

                exec($command, $return);
            
                $result = json_decode($return[0], true);
                $reply = array(
                    'success' => $result["success"],
                    'message' => $result["message"]
                );
                echo(json_encode($reply));
            } else {
                $reply = array(
                    'success' => false,
                    'message' => "Missing args"
                );
                echo(json_encode($reply));
            }
            break;

        case "vm_delete":
            if (key_exists('id', $_POST)){
                $elem_id = htmlspecialchars($_POST['id']);
            }

            if ( ($elem_id != "") ){
                $return = [];
                $command = "python3 management.py -u ".$_SESSION['vcsa_username']." -p ".$_SESSION['vcsa_password']." -t ".$_SESSION['vcsa_token']." -a delete -e ".$elem_id;

                exec($command, $return);
            
                $result = json_decode($return[0], true);
                $reply = array(
                    'success' => $result["success"],
                    'message' => $result["message"]
                );
                echo(json_encode($reply));
            } else {
                $reply = array(
                    'success' => false,
                    'message' => "Missing args"
                );
                echo(json_encode($reply));
            }
            break;
        
        case "vm_backup":
            if (key_exists('id', $_POST)){
                $elem_id = htmlspecialchars($_POST['id']);
            }

            if ( ($elem_id != "") ){
                $return = [];
                $command = "python3 management.py -u ".$_SESSION['vcsa_username']." -p ".$_SESSION['vcsa_password']." -t ".$_SESSION['vcsa_token']." -a backup -e ".$elem_id." ";
                exec($command, $return);

                $result = json_decode($return[0], true);
                $reply = array(
                    'success' => $result["success"],
                    'message' => $result["message"]
                );
                echo(json_encode($reply));
            } else {
                $reply = array(
                    'success' => false,
                    'message' => "Missing args"
                );
                echo(json_encode($reply));
            }
            break;

        case "vm_create":
            $vm_name = "";
            $vm_model = "";
            $vm_ip = "";
            $vm_gw = "";
            $vm_dns = "";

            if (key_exists('vm_name', $_POST)){
                $vm_name = htmlspecialchars($_POST['vm_name']);
            }

            if (key_exists('vm_model', $_POST)){
                $vm_model = htmlspecialchars($_POST['vm_model']);
            }

            if (key_exists('vm_ip', $_POST)){
                $vm_ip = htmlspecialchars($_POST['vm_ip']);
            }

            if (key_exists('vm_gw', $_POST)){
                $vm_gw = htmlspecialchars($_POST['vm_gw']);
            }

            if (key_exists('vm_dns', $_POST)){
                $vm_dns = htmlspecialchars($_POST['vm_dns']);
            }

            if ( ($vm_name != "") and ($vm_model != "") and ($vm_ip != "") and ($vm_gw != "") and ($vm_dns != "")  ){
                $return = [];
                $command = "python3 management.py -u ".$_SESSION['vcsa_username']." -p ".$_SESSION['vcsa_password']." -t ".$_SESSION['vcsa_token']." -a create -n ".$vm_name." -i ".$vm_ip." -g ".$vm_gw." -d ".$vm_dns." ";

                exec($command, $return);

                $result = json_decode($return[0], true);
                $reply = array(
                    'success' => $result["success"],
                    'message' => $result["message"]
                );
                echo(json_encode($reply));
            } else {
                $reply = array(
                    'success' => false,
                    'message' => "Missing args"
                );
                echo(json_encode($reply));
            }
            break;
    }
?>