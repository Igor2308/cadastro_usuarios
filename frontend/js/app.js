const nome = document.getElementById("nome");
const email = document.getElementById("email");
const telefone = document.getElementById("telefone");
const cidade = document.getElementById("cidade");
const botao = document.getElementById("botaoCadastrar");

const erroNome = document.getElementById("erroNome");
const erroEmail = document.getElementById("erroEmail");
const erroTelefone = document.getElementById("erroTelefone");
const erroCidade = document.getElementById("erroCidade");


// Libera o e-mail quando o nome for preenchido

nome.addEventListener("input", function () {

    email.disabled = nome.value.trim() === "";

    erroNome.textContent = "";

});


// Libera o telefone quando o e-mail for preenchido

email.addEventListener("input", function () {

    telefone.disabled = email.value.trim() === "";

    erroEmail.textContent = "";

});


// Verifica o e-mail quando o usuário sair do campo

email.addEventListener("blur", function () {

    if (email.value.trim() === "") {

        erroEmail.textContent = "Informe o seu e-mail.";

        return;
    }

    if (!email.checkValidity()) {

        erroEmail.textContent =
            "Digite um e-mail válido terminado em .com ou .com.br.";

    } else {

        erroEmail.textContent = "";

    }

});


// Libera a cidade quando o telefone for preenchido

telefone.addEventListener("input", function () {

    // Remove tudo que não for número
    let numeros = telefone.value.replace(/\D/g, "");

    // Limita a quantidade máxima de números
    numeros = numeros.substring(0, 11);

    // Telefone celular com 11 números
    if (numeros.length <= 11) {

        if (numeros.length <= 2) {

            telefone.value = "(" + numeros;

        } else if (numeros.length <= 7) {

            telefone.value =
                "(" +
                numeros.substring(0, 2) +
                ") " +
                numeros.substring(2);

        } else {

            telefone.value =
                "(" +
                numeros.substring(0, 2) +
                ") " +
                numeros.substring(2, 7) +
                "-" +
                numeros.substring(7);
        }
    }

    // Libera o próximo campo somente quando
    // o telefone estiver completo
    cidade.disabled = numeros.length < 11;

    erroTelefone.textContent = "";
});

// Libera o botão quando todos os campos estiverem preenchidos

cidade.addEventListener("input", function () {

    erroCidade.textContent = "";

    botao.disabled =
        nome.value.trim() === "" ||
        email.value.trim() === "" ||
        telefone.value.trim() === "" ||
        cidade.value.trim() === "";

});


// Validação antes de enviar o formulário

document.querySelector("form").addEventListener("submit", function (event) {

    let formularioValido = true;


    // Validação do Nome

    if (nome.value.trim() === "") {

        erroNome.textContent =
            "Informe o nome do cliente.";

        formularioValido = false;

    }


    // Validação do E-mail

    if (email.value.trim() === "") {

        erroEmail.textContent =
            "Informe o e-mail do cliente.";

        formularioValido = false;

    } else if (!email.checkValidity()) {

        erroEmail.textContent =
            "Digite um e-mail válido terminado em .com ou .com.br.";

        formularioValido = false;

    }


    // Validação do Telefone

    if (telefone.value.trim() === "") {

        erroTelefone.textContent =
            "Informe o telefone do cliente.";

        formularioValido = false;

    }


    // Validação da Cidade

    if (cidade.value.trim() === "") {

        erroCidade.textContent =
            "Informe a cidade do cliente.";

        formularioValido = false;

    }


    // Impede o envio se houver algum erro

    if (!formularioValido) {

        event.preventDefault();

    }

});