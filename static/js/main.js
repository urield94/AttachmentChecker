function turn_buttons_off(){
    $("#download").prop("disabled", true);
    $("#scan").prop("disabled", true);
    $("#download_scan").prop("disabled", true);
}

function turn_buttons_on(){
    $("#download").prop("disabled", false);
    $("#scan").prop("disabled", false);
    $("#download_scan").prop("disabled", false);
}

function download_and_scan() {
    download();
    scan();
}

function download() {
    turn_buttons_off();
    let username = $("#username");
    let password = $("#password");
    let data = {'username': username.val(), 'password': password.val()};
    $.post("/download", data).done(function () {
        alert("Done downloading attachments");
    });
    turn_buttons_on();
}

function scan() {
    turn_buttons_off();
    $("#formContent").hide();
    $(".loader").show();
    $.post("/scan").done(function (res_str) {
        let res = JSON.parse(res_str);
        let results_div = $("#results");
        $(".loader").hide();
        let result_table = document.createElement('table');
        result_table.setAttribute("style", "width:100%;");
        let titles = ["FileName", "From", "Subject", "Status"];
        let tr_titles = document.createElement('tr');
        for (let title in titles) {
            if (titles.hasOwnProperty(title)) {
                let th = document.createElement('th');
                // th.setAttribute("style", "padding:6px; font-size: 25px");
                th.innerText = titles[title];
                tr_titles.appendChild(th);
            }
        }
        result_table.append(tr_titles);
        for (let filename in res) {
            if (res.hasOwnProperty(filename)) {
                let tr = document.createElement('tr');
                let td_filname = document.createElement('td');
                td_filname.innerText = " " + filename + " ";
                tr.appendChild(td_filname);
                for (let attr in res[filename]) {
                    if (res[filename].hasOwnProperty(attr)) {
                        let td = document.createElement('td');
                        if (res[filename][attr] === "Clean!") {
                            td.setAttribute("style", "color:green;");
                        }
                        if (res[filename][attr] === "Infected!") {
                            td.setAttribute("style", "color:red;");
                        }
                        if (res[filename][attr] === "Might be infected") {
                            td.setAttribute("style", "color:#c9a82e;");
                        }
                        td.innerText = " " + res[filename][attr] + " ";
                        tr.appendChild(td);
                    }
                }
                result_table.append(tr);
            }
        }
        results_div.append(result_table);
        results_div.show();
    });
    turn_buttons_on();
}