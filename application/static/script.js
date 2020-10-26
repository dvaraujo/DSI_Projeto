const button = document.querySelector('#btn_comprar');

button.addEventListener('click', event => {
    fetch('/stripe_pay')                         // Rota que contém a publick key. necessário para a inicialização da Checkout Session
    .then((result) => { return result.json(); }) // Retorna e converte para json o retorno da função fetch

    .then((data) => {                            
        var stripe = Stripe(data.checkout_public_key); // Instancia objeto do stripe, passando a Public Key vinda do Flask
        stripe.redirectToCheckout({                    // Redireciona para a página de checkout do Stripe, passando o Session Id vindo do Flask
            sessionId: data.checkout_session_id})
        .then(function (result) {
        });
    })
});