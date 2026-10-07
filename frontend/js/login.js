const email = document.getElementById("email");
const senha = document.getElementById("senha");
const mostrarSenha = document.getElementById("mostrarSenha");

const erroEmail = document.getElementById("erroEmail");
const erroSenha = document.getElementById("erroSenha");


// Validação do e-mail

email.addEventListener("input", function () {

    erroEmail.textContent = "";

});


// Validação da senha

senha.addEventListener("input", function () {

    erroSenha.textContent = "";

});


// Mostra ou esconde a senha

mostrarSenha.addEventListener("click", function () {

    if (senha.type === "password") {

        senha.type = "text";

        mostrarSenha.textContent = "🙈";

        mostrarSenha.setAttribute(
            "aria-label",
            "Ocultar senha"
        );

    } else {

        senha.type = "password";

        mostrarSenha.textContent = "👁";

        mostrarSenha.setAttribute(
            "aria-label",
            "Mostrar senha"
        );

    }

});


// Validação antes de enviar

document.getElementById("loginForm").addEventListener(
    "submit",
    function (event) {

        let valido = true;


        if (!email.checkValidity()) {

            erroEmail.textContent =
                "⚠ Digite um e-mail válido, por exemplo: exemplo@gmail.com";

            valido = false;

        }


        if (!senha.checkValidity()) {

            erroSenha.textContent =
                "⚠ A senha precisa ter pelo menos 6 caracteres, uma letra maiúscula, uma minúscula, um número e um caractere especial.";

            valido = false;

        }


        if (!valido) {

            event.preventDefault();

        }

    }
);