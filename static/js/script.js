  localStorage = window.localStorage;

  usuarioinfo = document.getElementById("nombre");

  nombreusuario = document.getElementById("nombreusuario");

  cerrarsesion = document.getElementById("cerrarsesion");

  if (usuarioinfo.value != '') {
    localStorage.setItem("usuarioinfo", usuarioinfo.value)
  }

  if(localStorage.getItem("usuarioinfo")) {
    nombreusuario.innerHTML = localStorage.getItem("usuarioinfo")

    navLogOut.removeAttribute('style', 'display:block')
    navLogOut.setAttribute('style', 'display:none')

    navLogIn.removeAttribute('style', 'display:none')
    navLogIn.setAttribute('style', 'display:block')
  } else {
    navLogOut.removeAttribute('style', 'display:none')
    navLogOut.setAttribute('style', 'display:block')

    navLogIn.removeAttribute('style', 'display:block')
    navLogIn.setAttribute('style', 'display:none')
  }

  cerrarsesion.addEventListener('click', function() {
    localStorage.clear();
    window.location = '/home';
  })

  inventoryRef = document.getElementById('inventoryRef');
  if(inventoryRef !== null){
        inventoryRef.setAttribute("href","/inventory/"+localStorage.getItem("usuarioinfo"));
  }

    profileRef = document.getElementById('profileRef');
    if(profileRef !== null){
          profileRef.setAttribute("href","/profile/"+localStorage.getItem("usuarioinfo"));
    }

 
