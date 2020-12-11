

function validar_formulario(){
    var nombre = document.formulario.nombre;
    var correo = document.formulario.correo;
    var clave = document.formulario.password;

    var nombre_len = nombre.value.length;


    console.log(intentos);
    if(nombre_len == 0 || nombre_len < 8){
        alert("Debes ingresar un usario con mínimo 8 caracteres");
        return false;
    }

    
    // \w+ 1 o más caracteres alfanumericos, [\.-]? puede que haya un punto o un guion \w+ uno o más caracteres alfanumericos

    var formatoCorreo = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

    if(!correo.value.match(formatoCorreo)){
        alert("Debes ingresar un correo electrónico válido")
        return false;
    }
   

    var clave_len = clave.value.length;
    if(clave_len == 0 || clave_len < 8){
        alert("Debes ingresar una clave con mínimo 8 caracteres");
        return false;
    }
     
/*
    if(nombre.value == 'test' && clave.value == 'test'){
        alert("Ingreso exitoso");
    }else{
        if(intentos > 0){
            intentos -= 1;
            alert("intentos restantes "+ (intentos+1));
        }else{
            alert("Intentos restantes: " + intentos);
            nombre.disabled = "true";
            clave.disabled = "true";
            document.getElementById('registro').disabled = "true";
        }
        return false;
    }
    */
}

function mostrarPassword(){
    var obj = document.getElementById('password');
    obj.type = "text";
}

function ocultarPassword(){
    var obj = document.getElementById('password');
    obj.type = "password";
}