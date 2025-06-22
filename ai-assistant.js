// ==========================================================================================
// ВАЖНО: Вставьте ваш API-ключ от OpenAI (ChatGPT) сюда
// IMPORTANT: Paste your API key from OpenAI (ChatGPT) here
const OPENAI_API_KEY = "ВАШ_API_КЛЮЧ_ЗДЕСЬ";
// ==========================================================================================

const aiInputField = document.getElementById('ai-input');
const aiSphereButton = document.getElementById('ai-sphere-btn');
const aiResponseContainer = document.getElementById('ai-response-container');

if (!OPENAI_API_KEY || OPENAI_API_KEY === "ВАШ_API_КЛЮЧ_ЗДЕСЬ") {
    aiResponseContainer.innerHTML = `<p style="color: red; font-weight: bold;">Внимание: API-ключ OpenAI не найден. Пожалуйста, добавьте его в файл ai-assistant.js.</p>`;
    console.error("AI Assistant Error: OpenAI API Key is missing. Please add it to ai-assistant.js");
}

const askAI = async () => {
    const question = aiInputField.value.trim();
    // Не отправляем запрос, если поле пустое или ключ не вставлен
    if (!question || !OPENAI_API_KEY || OPENAI_API_KEY === "ВАШ_API_КЛЮЧ_ЗДЕСЬ") {
        if (!question) aiResponseContainer.innerHTML = `<p>Пожалуйста, введите вопрос.</p>`;
        return;
    }

    // Очищаем предыдущий ответ и показываем состояние загрузки
    aiInputField.disabled = true;
    aiResponseContainer.innerHTML = '<p>ChatGPT думает...</p>';
    aiSphereButton.classList.add('loading');

    try {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${OPENAI_API_KEY}`
            },
            body: JSON.stringify({
                model: 'gpt-3.5-turbo', // Вы можете поменять модель на gpt-4, если у вас есть доступ
                messages: [{ role: 'user', content: question }],
                temperature: 0.7
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Ошибка API OpenAI: ${response.status} - ${errorData.error.message}`);
        }

        const data = await response.json();
        const aiMessage = data.choices[0].message.content;

        // Отображаем ответ
        aiResponseContainer.innerHTML = `<p>${aiMessage}</p>`;

    } catch (error) {
        console.error("AI Assistant Error:", error);
        aiResponseContainer.innerHTML = `<p style="color: red;">Произошла ошибка при обращении к ChatGPT. Пожалуйста, проверьте консоль. (${error.message})</p>`;
    } finally {
        // Включаем поле ввода и убираем анимацию загрузки
        aiInputField.disabled = false;
        aiInputField.value = ''; // Очищаем поле ввода
        aiSphereButton.classList.remove('loading');
    }
};

aiInputField.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        askAI();
    }
});

aiSphereButton.addEventListener('click', () => {
    askAI();
}); 