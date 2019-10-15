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

function localize_time(id, text, date) {
    date = new Date(date);
    date = date.toLocaleString();
    document.getElementById(id).innerHTML = text + date;
}