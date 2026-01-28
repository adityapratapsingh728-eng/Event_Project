document.addEventListener("DOMContentLoaded",() =>{
    const College_id = document.getElementById("College_id");
    const role = document.querySelectorAll('input[name="role"]');
    const msg = document.getElementById("idMessage");
    const button = document.getElementsByClassName("reg-btn")[0];
    
    function validate() {
    const id = College_id.value.trim();
    const selectedRole = document.querySelector('input[name="role"]:checked');

    button.disabled= true;

    // Step 1: ID empty
    if (!id) {
        msg.innerText = "";
        return;
    }
    // Step 3: Role not selected yet
    if (!selectedRole) {
        msg.innerText = "⚠ Select a role";
        msg.style.color = "orange";
        return;
    }
    // Step 3: Match role and ID prefix
    if (!/^\d{13}$/.test(id)) { // validate 14-digit numeric ID
        msg.innerText = "❌ Invalid ID format";
        msg.style.color = "red";
        button.disabled = true;
    }
    else {
        msg.innerText = "⚠ ID format ok, role will be verified on submit";
        msg.style.color = "orange";
        button.disabled = false;
    }
}
    College_id.addEventListener("input", validate);
    role.forEach(r => r.addEventListener("change", validate));
}

);