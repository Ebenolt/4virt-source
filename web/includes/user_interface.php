<h1> VMs :</h1>
<?php
    $return = [];
    exec("python3 management.py -u ".$_SESSION["vcsa_username"]." -p ".$_SESSION["vcsa_password"]." -t ".$_SESSION["vcsa_token"]." -a get", $return);
    $result = json_decode($return[0], true);

    if ($result['success']){
        foreach ($result['message'] as $vm){?>
            <div class='vm'>
                <p class='name'> <?php echo($vm['name']) ?> </p>
                <p class='id'><i><?php echo($vm['id']) ?></i></p>
                <p class='spec'><h4>Status:</h4> <?php echo($vm['status']) ?> </p><br>
                <p class='spec'><h4>IP:</h4> <?php echo($vm['ip']) ?> </p><br>
                <p class='spec'><h4>CPU:</h4> <?php echo($vm['cpu']) ?> vCPU </p><br>
                <p class='spec'><h4>RAM:</h4> <?php echo($vm['ram']) ?>MB </p><br>
                <p class='spec'><h4>Networks:</h4>
                    <ul>
            <?php
            foreach ($vm['networks'] as $net){
                echo ("<li>".$net."</li>\n");
            }?>
                    </ul>
                </p>
                <p class='spec'>
                    <h4>Backups:</h4>
                    <ul>
            <?php    
            foreach ($vm['backups'] as $back){
                echo ("<li>".$back."</li>\n");
            }?>
                    </ul>
                </p>
            <p class='actions'>
                <h4>Actions:</h4>
                <button type='button' class='vm_power_on' value='<?php echo $vm['id'] ?>'>Allumer</button>
                <button type='button' class='vm_power_off' value='<?php echo $vm['id'] ?>'>Eteindre</button>
                <button type='button' class='vm_power_reset' value='<?php echo $vm['id'] ?>'>Redémarrer</button>
                <button type='button' class='vm_power_suspend' value='<?php echo $vm['id'] ?>'>Suspendre</button>
                <button type='button' class='vm_backup' value='<?php echo $vm['id'] ?>'>Backup</button>
                <button type='button' class='vm_delete' value='<?php echo $vm['id'] ?>'>Delete</button>
            </p>
            </div>
    <?php
        }?>
    <div id='vm_create'>
                <h4>VM Creation :</h4>
                <form>
                    
                    <p>VM Name: <input type="text" id='vm_name' name="vm_name" placeholder="My super VM" /></p>
                    <p>Model:
                        <select id='vm_model' name="vm_model" />
                            <option value="W10-Template"> W10-Template </option>
                        </select>
                    </p>
                    <p>IP: <input type="text" id='vm_ip' name="vm_ip" placeholder="192.168.20.XX" /></p>
                    <p>Gateway: <input type="text" id='vm_gw' name="vm_gw" placeholder="192.168.20.XX" /></p>
                    <p>DNS: <input type="text" id='vm_dns' name="vm_dns" placeholder="1.1.1.1" /></p>

                    <input type="hidden" id="action" id='action' name="action" value="vm_create"/>
                    <input type="submit" id="vm_create_button" value="Create">
                </form>
            </div>
    <?php
    } else {
        echo("Error while retrieving VMs");
    }
?>