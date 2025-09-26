// Espera a que la página se cargue por completo
document.addEventListener('DOMContentLoaded', () => {

    // Obtiene los elementos de la pantalla. Ahora todos están dentro del mismo scope.
    const welcomeScreen = document.getElementById('welcome-screen');
    const quizScreen = document.getElementById('quiz-screen');
    const recommendationScreen = document.getElementById('recommendation-screen');
    const startButton = document.getElementById('start-button');
    const recommendButton = document.getElementById('recommend-button');
    const restartButton = document.getElementById('restart-button');

    // Datos de las preguntas y opciones (4 preguntas)
    const questions = [
        {
            question: "¿Qué tipo de producto te gustaría?",
            options: ["Paleta", "Helado", "Agua", "Especialidad"],
            category: "type"
        },
        {
            question: "¿Prefieres que sea a base de agua o de leche?",
            options: ["Agua", "Leche"],
            category: "base"
        },
        {
            question: "¿Qué sabor te apetece más?",
            options: ["Dulce", "Ácido", "Cremoso", "Algo con chile"],
            category: "flavor"
        },
        {
            question: "¿Te gustan los sabores originales o clásicos?",
            options: ["Original", "Clásico"],
            category: "style"
        }
    ];

    // Muestra la pantalla del cuestionario
    function showQuizScreen() {
        welcomeScreen.classList.remove('active');
        welcomeScreen.classList.add('hidden');
        quizScreen.classList.remove('hidden');
        quizScreen.classList.add('active');
        renderQuestions();
    }

    // Renderiza las preguntas en la pantalla del cuestionario
    function renderQuestions() {
        const questionsContainer = document.getElementById('questions');
        questionsContainer.innerHTML = '';
        questions.forEach((q, index) => {
            const questionDiv = document.createElement('div');
            questionDiv.classList.add('question-item');
            questionDiv.innerHTML = `
                <h2>${index + 1}. ${q.question}</h2>
                <div class="options-grid">
                    ${q.options.map(option => `
                        <button class="option-button" data-category="${q.category}" data-value="${option}">${option}</button>
                    `).join('')}
                </div>
            `;
            questionsContainer.appendChild(questionDiv);
        });

        // Agrega el evento de clic a cada botón de opción
        document.querySelectorAll('.option-button').forEach(button => {
            button.addEventListener('click', handleOptionClick);
        });
    }

    // Maneja la selección de opciones
    function handleOptionClick(event) {
        const selectedButton = event.target;
        const category = selectedButton.dataset.category;

        document.querySelectorAll(`.option-button[data-category="${category}"]`).forEach(button => {
            button.classList.remove('selected');
        });

        selectedButton.classList.add('selected');

        const allAnswered = questions.every(q => 
            document.querySelector(`.option-button.selected[data-category="${q.category}"]`)
        );

        if (allAnswered) {
            recommendButton.style.display = 'block';
        }
    }

    // Asigna los eventos de clic
    startButton.addEventListener('click', showQuizScreen);

    recommendButton.addEventListener('click', async () => {
        const selectedOptions = {};
        document.querySelectorAll('.option-button.selected').forEach(button => {
            selectedOptions[button.dataset.category] = button.dataset.value;
        });

        try {
            const response = await fetch('/recommend', { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(selectedOptions),
            });

            const recommendation = await response.json();

            document.getElementById('recommendation-title').textContent = "¡La Michoacana Recomienda!";
            document.getElementById('recommended-product-name').textContent = recommendation.product_name;
            document.getElementById('recommended-product-price').textContent = "Precio: $" + recommendation.product_price;
            document.getElementById('recommendation-reason').textContent = recommendation.reason;
            document.getElementById('recommended-product-img').src = recommendation.image_url;

            quizScreen.classList.remove('active');
            quizScreen.classList.add('hidden');
            recommendationScreen.classList.remove('hidden');
            recommendationScreen.classList.add('active');

        } catch (error) {
            console.error('Error al obtener la recomendación:', error);
            alert('Hubo un error al obtener la recomendación. Por favor, inténtalo de nuevo.');
        }
    });

    restartButton.addEventListener('click', () => {
        recommendationScreen.classList.remove('active');
        recommendationScreen.classList.add('hidden');
        welcomeScreen.classList.remove('hidden');
        welcomeScreen.classList.add('active');

        document.querySelectorAll('.option-button.selected').forEach(button => {
            button.classList.remove('selected');
        });

        recommendButton.style.display = 'none';
    });

    // Muestra la pantalla de bienvenida al cargar la página
    welcomeScreen.classList.add('active');

});
