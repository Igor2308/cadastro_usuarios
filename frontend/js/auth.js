const token = sessionStorage.getItem("token");


// ==========================================
// VERIFICA SE EXISTE UMA SESSÃO
// ==========================================

if (!token) {

    window.location.replace("/");

} else {

    fetch(
        "/validar-sessao",
        {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + token
            }
        }
    )
    .then(function (resposta) {

        if (!resposta.ok) {

            sessionStorage.removeItem("token");

            window.location.replace("/");
        }

    })
    .catch(function () {

        sessionStorage.removeItem("token");

        window.location.replace("/");
    });
}


// ==========================================
// CONTROLA O BOTÃO VOLTAR
// ==========================================

window.addEventListener(
    "popstate",
    function () {

        // Encerra a sessão desta guia
        sessionStorage.removeItem("token");

        // Volta para o login
        window.location.replace("/");
    }
);


// ==========================================
// CRIA UMA ENTRADA NO HISTÓRICO
// ==========================================

history.pushState(
    null,
    "",
    window.location.href
);