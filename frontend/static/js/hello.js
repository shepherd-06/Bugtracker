function registration_form() {
    el = document.querySelector('.registration_form');
    register_btn = document.querySelector('.registration_btn');

    if (el.style.display == 'none') {
        el.style.display = 'block';
        register_btn.style.display = 'none';
    }
}



function login_form() {
    el = document.querySelector('.login_form');
    login_btn = document.querySelector('.login_btn');

    if (el.style.display == 'none') {
        el.style.display = 'block';
        login_btn.style.display = 'none';
    }
}


function org_form() {
    alert("Org form");
}

function project_form() {
    alert("Project form");
}


function set_storage(data) {
    console.log(data);
}

function set_local_storage_data(key, data) {
    if (window.localStorage) {
        // do stuff with localStorage
        // no need to use window anymore
        localStorage.setItem(key, JSON.stringify(data));
    }
}


function get_local_storage_data(key) {
    var data = [];
    if (localStorage.getItem(key)) {
        data = JSON.parse(localStorage.getItem(key));
        console.log(data);
    }
    return data;
}


function get_org_from_localStorage(key) {
    return get_local_storage_data(key);
}

function org_selected(org_name) {
    alert(org_name)
}