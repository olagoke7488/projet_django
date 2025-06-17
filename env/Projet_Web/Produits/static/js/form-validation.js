function validate(val) {
    let v1 = document.getElementById("fname");
    let v2 = document.getElementById("lname");
    let v3 = document.getElementById("email");
    let v4 = document.getElementById("mob");
    let v5 = document.getElementById("job");
    let v6 = document.getElementById("ans");

    let flags = [true, true, true, true, true, true];
    let fields = [v1, v2, v3, v4, v5, v6];

    for (let i = 1; i <= 6; i++) {
        if (val >= i || val === 0) {
            if (fields[i - 1].value === "") {
                fields[i - 1].style.borderColor = "red";
                flags[i - 1] = false;
            } else {
                fields[i - 1].style.borderColor = "green";
                flags[i - 1] = true;
            }
        }
    }

    return flags.every(Boolean);
}
