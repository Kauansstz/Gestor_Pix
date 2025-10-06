document.addEventListener('DOMContentLoaded', () => {
    const listaConversas = document.getElementById('lista-conversas');
    const chatMensagens = document.getElementById('chat-mensagens');
    const chatHeader = document.getElementById('chat-header');
    const form = document.getElementById('form-enviar');
    const inputMsg = document.getElementById('mensagem');

    let numeroAtual = null;

    // 🔹 Carregar conversas
    fetch('/conversas/')
        .then(res => res.json())
        .then(conversas => {
            conversas.forEach(conv => {
                const div = document.createElement('div');
                div.className = 'p-3 hover:bg-gray-100 border-b cursor-pointer';
                div.innerHTML = `<p class="font-semibold">${conv.nome}</p><p class="text-sm text-gray-500">${conv.ultima_msg}</p>`;
                div.addEventListener('click', () => abrirConversa(conv.numero, conv.nome));
                listaConversas.appendChild(div);
            });
        });

    // 🔹 Abrir conversa
    function abrirConversa(numero, nome) {
        numeroAtual = numero;
        chatHeader.textContent = nome;
        chatMensagens.innerHTML = '';
        fetch(`/mensagens/${numero}/`)
            .then(res => res.json())
            .then(data => {
                data.mensagens.forEach(msg => {
                    const p = document.createElement('p');
                    p.className = `my-1 px-3 py-2 inline-block rounded-lg ${msg.tipo === 'enviada' ? 'bg-blue-200 ml-auto text-right' : 'bg-gray-200 mr-auto text-left'}`;
                    p.textContent = msg.texto;
                    chatMensagens.appendChild(p);
                });
                chatMensagens.scrollTop = chatMensagens.scrollHeight;
            });
    }

    // 🔹 Enviar mensagem
    form.addEventListener('submit', e => {
        e.preventDefault();
        if (!numeroAtual) return alert('Selecione uma conversa.');

        const formData = new FormData(form);
        formData.append('numero', numeroAtual);

        fetch('/enviar/', {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value }
        })
        .then(res => res.json())
        .then(resp => {
            console.log('Enviado:', resp);
            inputMsg.value = '';
            abrirConversa(numeroAtual); // recarrega mensagens
        });
    });

    // 🔔 Recebe notificações (simulação)
    setInterval(() => {
        if (numeroAtual) abrirConversa(numeroAtual);
    }, 5000); // a cada 5 segundos verifica novas mensagens
});
