
function addFeedback(good, feedback){
    removeFeedback();
    let text = document.createTextNode(feedback);
    feeddiv = document.createElement('div');
    feeddiv.setAttribute('id', 'feedback');
    feeddiv.appendChild(text);
    if(good){
        feeddiv.classList.add('ok');
    } else {
        feeddiv.classList.add('notok');
    }
    feeddiv.classList.add('row', 'justify-content-center', 'sticky-bottom', 'offset-sm-2', 'offset-md-3', 'offset-lg-4', 'col-sm-8', 'col-md-6', 'col-lg-4');
    document.body.appendChild(feeddiv);
    setTimeout(removeFeedback, 5000);
};

function removeFeedback(){
    if(document.getElementById('feedback')!=null){
        document.body.removeChild(document.getElementById('feedback'));
    };
};

if(document.getElementById("login_button") != null){
    let login_button = document.getElementById('login_button');

    login_button.addEventListener('click', function(event){
        event.preventDefault();
        let data = new FormData();
        data.append('username', document.getElementById("username").value);
        data.append('password', document.getElementById("password").value);
        data.append('action', document.getElementById("action").value)
        let xhr = new XMLHttpRequest();
        xhr.responseType = "json" // remove for txt
        xhr.open('POST', 'post.php', true);
        xhr.onload = function () {
                // let response = this.responseText;
                let response = this.response;
                // console.log(response);
                if(response != undefined){
                    if(response.success){
                        addFeedback(true, 'Login successfull !');
                        location.reload();
                    } else {
                        addFeedback(false, response.message);
                    }
                } else {
                    addFeedback(0, "Error while contacting server");
                }
            };
        xhr.send(data);
    });
}




let vm_power_on_buttons = document.querySelectorAll('.vm_power_on');

vm_power_on_buttons.forEach(function(button) {
        button.addEventListener('click', function(event){
                event.preventDefault();
                let data = new FormData();
                data.append('id', button.value);
                data.append('action', 'vm_power_up')

                let xhr = new XMLHttpRequest();
                xhr.responseType = "json" 
                xhr.open('POST', 'post.php', true);
                xhr.onload = function () {
                    // let response = this.responseText;
                    // console.log(response);
                    let response = this.response;
                    if(response != undefined){
                        addFeedback(response.success, response.message)
                    } else {
                        addFeedback(0, "Error while contacting server");
                    }
                };
                xhr.send(data);
        });
});


let vm_power_off_buttons = document.querySelectorAll('.vm_power_off');

vm_power_off_buttons.forEach(function(button) {
        button.addEventListener('click', function(event){
                event.preventDefault();
                let data = new FormData();
                data.append('id', button.value);
                data.append('action', 'vm_power_off')

                let xhr = new XMLHttpRequest();
                xhr.responseType = "json" 
                xhr.open('POST', 'post.php', true);
                xhr.onload = function () {
                    // let response = this.responseText;
                    // console.log(response);
                    let response = this.response;
                    if(response != undefined){
                        addFeedback(response.success, response.message)
                    } else {
                        addFeedback(0, "Error while contacting server");
                    }
                };
                xhr.send(data);
        });
});

let vm_power_reset_buttons = document.querySelectorAll('.vm_power_reset');

vm_power_reset_buttons.forEach(function(button) {
        button.addEventListener('click', function(event){
                event.preventDefault();
                let data = new FormData();
                data.append('id', button.value);
                data.append('action', 'vm_power_reset')

                let xhr = new XMLHttpRequest();
                xhr.responseType = "json" 
                xhr.open('POST', 'post.php', true);
                xhr.onload = function () {
                    // let response = this.responseText;
                    // console.log(response);
                    let response = this.response;
                    if(response != undefined){
                        addFeedback(response.success, response.message)
                    } else {
                        addFeedback(0, "Error while contacting server");
                    }
                };
                xhr.send(data);
        });
});



let vm_power_suspend_buttons = document.querySelectorAll('.vm_power_suspend');

vm_power_suspend_buttons.forEach(function(button) {
        button.addEventListener('click', function(event){
                event.preventDefault();
                let data = new FormData();
                data.append('id', button.value);
                data.append('action', 'vm_power_suspend')

                let xhr = new XMLHttpRequest();
                xhr.responseType = "json" 
                xhr.open('POST', 'post.php', true);
                xhr.onload = function () {
                    // let response = this.responseText;
                    // console.log(response);
                    let response = this.response;
                    if(response != undefined){
                        addFeedback(response.success, response.message)
                    } else {
                        addFeedback(0, "Error while contacting server");
                    }
                };
                xhr.send(data);
        });
});

let vm_delete_buttons = document.querySelectorAll('.vm_delete');

vm_delete_buttons.forEach(function(button) {
        button.addEventListener('click', function(event){
                event.preventDefault();
                let data = new FormData();
                data.append('id', button.value);
                data.append('action', 'vm_delete')

                let xhr = new XMLHttpRequest();
                xhr.responseType = "json" 
                xhr.open('POST', 'post.php', true);
                xhr.onload = function () {
                    // let response = this.responseText;
                    // console.log(response);
                    let response = this.response;
                    if(response != undefined){
                        addFeedback(response.success, response.message)
                    } else {
                        addFeedback(0, "Error while contacting server");
                    }
                };
                xhr.send(data);
        });
});

let vm_backup_buttons = document.querySelectorAll('.vm_backup');

vm_backup_buttons.forEach(function(button) {
        button.addEventListener('click', function(event){
                event.preventDefault();
                let data = new FormData();
                data.append('id', button.value);
                data.append('action', 'vm_backup')

                let xhr = new XMLHttpRequest();
                xhr.responseType = "json" 
                xhr.open('POST', 'post.php', true);
                xhr.onload = function () {
                    // let response = this.responseText;
                    // console.log(response);
                    let response = this.response;
                    if(response != undefined){
                        addFeedback(response.success, response.message)
                    } else {
                        addFeedback(0, "Error while contacting server");
                    }
                };
                xhr.send(data);
        });
});





if(document.getElementById("vm_create_button") != null){
    let vm_create_button = document.getElementById('vm_create_button');
    
    vm_create_button.addEventListener('click', function(event){
        event.preventDefault();
        let data = new FormData();
        data.append('vm_name', document.getElementById("vm_name").value);
        data.append('vm_model', document.getElementById("vm_model").value);
        data.append('vm_ip', document.getElementById("vm_ip").value);
        data.append('vm_gw', document.getElementById("vm_gw").value);
        data.append('vm_dns', document.getElementById("vm_dns").value);
        data.append('action', "vm_create");

        let xhr = new XMLHttpRequest();
        xhr.responseType = "json" // remove for txt
        xhr.open('POST', 'post.php', true);
        xhr.onload = function () {
                // let response = this.responseText;
                let response = this.response;
                // console.log(response);
                if(response != undefined){
                    addFeedback(response.success, response.message);
                } else {
                    addFeedback(0, "Error while contacting server");
                }
            };
        xhr.send(data);
    });
};
