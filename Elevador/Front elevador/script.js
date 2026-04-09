document.addEventListener("DOMContentLoaded", () => {
    // Ordem exata dos andares
    const floorMap = ['T', '1', '2', '3'];
    let currentFloorIndex = 0; // Inicia no Térreo
    let isMoving = false;

    // Elementos do DOM
    const displaySpan = document.getElementById('floor-display');
    const doorLeft = document.getElementById('door-left');
    const doorRight = document.getElementById('door-right');
    const buttons = document.querySelectorAll('.floor-btn');

    // Adiciona o evento de clique para todos os botões
    buttons.forEach(button => {
        button.addEventListener('click', (e) => {
            const targetFloor = e.target.getAttribute('data-floor');
            requestFloor(targetFloor, e.target);
        });
    });

    /**
     * Função principal que gerencia a sequência de eventos do elevador.
     */
    async function requestFloor(targetFloorString, btnElement) {
        // Bloqueia se já estiver em movimento ou se chamou o andar atual
        if (isMoving) return;
        
        const targetIndex = floorMap.indexOf(targetFloorString);
        if (targetIndex === currentFloorIndex) return;

        isMoving = true;
        setButtonsState(true); // Desativa botões
        btnElement.classList.add('active'); // Acende o botão pressionado

        // Passo 1: Fechar portas
        await closeDoors();

        // Passo 2: Mover passando pelos andares intermediários
        await moveElevator(targetIndex);

        // Passo 3: Abrir portas
        await openDoors();

        // Limpa estados
        btnElement.classList.remove('active');
        setButtonsState(false);
        isMoving = false;
    }

    // --- Funções de Controle de Estado ---

    function setButtonsState(disabled) {
        buttons.forEach(btn => btn.disabled = disabled);
    }

    function closeDoors() {
        return new Promise(resolve => {
            doorLeft.classList.remove('open');
            doorRight.classList.remove('open');
            
            // Aguarda o tempo da transição do CSS (1s) antes de resolver a promise
            setTimeout(resolve, 1000); 
        });
    }

    function openDoors() {
        return new Promise(resolve => {
            doorLeft.classList.add('open');
            doorRight.classList.add('open');
            setTimeout(resolve, 1000);
        });
    }

    function moveElevator(targetIndex) {
        return new Promise(resolve => {
            // Determina a direção (1 para subir, -1 para descer)
            const step = currentFloorIndex < targetIndex ? 1 : -1;
            
            function stepFloor() {
                if (currentFloorIndex !== targetIndex) {
                    // Atualiza o índice interno
                    currentFloorIndex += step;
                    
                    // Atualiza o display visualmente
                    displaySpan.innerText = floorMap[currentFloorIndex];
                    
                    // Aguarda 1.5 segundos em cada andar antes de ir para o próximo
                    setTimeout(stepFloor, 1500); 
                } else {
                    // Chegou ao destino
                    resolve();
                }
            }

            // Inicia o movimento após um pequeno atraso de 500ms
            setTimeout(stepFloor, 500);
        });
    }
});