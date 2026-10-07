const email = document.getElementById("email");
const senha = document.getElementById("senha");
const mostrarSenha = document.getElementById("mostrarSenha");

const erroEmail = document.getElementById("erroEmail");
const erroSenha = document.getElementById("erroSenha");


// ==========================================
// LIMPA MENSAGENS DE ERRO
// ==========================================

email.addEventListener("input", function () {
    erroEmail.textContent = "";
});

senha.addEventListener("input", function () {
    erroSenha.textContent = "";
});


// ==========================================
// MOSTRAR / OCULTAR SENHA
// ==========================================

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


// ==========================================
// LOGIN
// ==========================================

document.getElementById("loginForm").addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        let valido = true;


        // Validação do e-mail

        if (!email.checkValidity()) {

            erroEmail.textContent =
                "⚠ Digite um e-mail válido, por exemplo: exemplo@gmail.com";

            valido = false;
        }


        // Validação da senha

        if (!senha.checkValidity()) {

            erroSenha.textContent =
                "⚠ A senha precisa ter pelo menos 6 caracteres, uma letra maiúscula, uma minúscula, um número e um caractere especial.";

            valido = false;
        }


        if (!valido) {
            return;
        }


        // Envia os dados para o backend

        const dados = new FormData();

        dados.append("email", email.value);
        dados.append("senha", senha.value);


        try {

            const resposta = await fetch(
                "/login",
                {
                    method: "POST",
                    body: dados
                }
            );

            const resultado = await resposta.json();


            if (!resultado.sucesso) {

                const mensagem =
                    document.getElementById(
                        "erroCredenciais"
                    );

                if (mensagem) {
                    mensagem.textContent =
                        "Credenciais inválidas.";
                }

                return;
            }


            // Guarda o token somente nesta guia

            sessionStorage.setItem(
                "token",
                resultado.token
            );


            // Vai para a área protegida

            window.location.href = "/cadastro";

        } catch (erro) {

            console.error(erro);

            const mensagem =
                document.getElementById(
                    "erroCredenciais"
                );

            if (mensagem) {
                mensagem.textContent =
                    "Não foi possível realizar o login.";
            }
        }
    }
);