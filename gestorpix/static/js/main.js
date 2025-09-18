document.addEventListener("DOMContentLoaded", function () {

    // ---------------------------
    // Modal Dinâmico
    // ---------------------------
    const modalTriggers = document.querySelectorAll('[data-modal-target]');
    const modals = document.querySelectorAll('.modal');
    const modalCloses = document.querySelectorAll('.modal .close');

    modalTriggers.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = document.querySelector(btn.dataset.modalTarget);
            if(target) target.style.display = 'flex';
        });
    });

    modalCloses.forEach(btn => {
        btn.addEventListener('click', () => {
            btn.closest('.modal').style.display = 'none';
        });
    });

    window.onclick = function(event) {
        modals.forEach(modal => {
            if(event.target == modal){
                modal.style.display = 'none';
            }
        });
    }

    // ---------------------------
    // Alert Dinâmico (fade out)
    // ---------------------------
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 4000); // desaparece após 4s
    });

    // ---------------------------
    // Menu Mobile Toggle
    // ---------------------------
    const menuBtn = document.getElementById('menu-btn');
    const navMenu = document.getElementById('nav-menu');

    if(menuBtn && navMenu){
        menuBtn.addEventListener('click', () => {
            navMenu.classList.toggle('hidden');
        });
    }

    // ---------------------------
    // Tabela Dinâmica (ordenar colunas)
    // ---------------------------
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        const headers = table.querySelectorAll('th');
        headers.forEach((th, idx) => {
            th.style.cursor = 'pointer';
            th.addEventListener('click', () => {
                sortTable(table, idx);
            });
        });
    });

    function sortTable(table, col) {
        const rows = Array.from(table.querySelectorAll('tr:nth-child(n+2)'));
        const asc = table.asc = !table.asc;

        rows.sort((a,b) => {
            const tdA = a.children[col].innerText;
            const tdB = b.children[col].innerText;

            if(!isNaN(tdA) && !isNaN(tdB)){
                return asc ? tdA - tdB : tdB - tdA;
            } else {
                return asc ? tdA.localeCompare(tdB) : tdB.localeCompare(tdA);
            }
        });

        rows.forEach(row => table.appendChild(row));
    }

    // ---------------------------
    // Botão Dinâmico (feedback)
    // ---------------------------
    const dynamicBtns = document.querySelectorAll('button[data-action]');
    dynamicBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const action = btn.dataset.action;
            console.log(`Ação executada: ${action}`);
        });
    });

});
module.exports = {
    darkMode: 'class', // ou 'media'
    content: ["./templates/**/*.html", "./static/**/*.js"],
    theme: {
        extend: {},
    },
    plugins: [],
}
