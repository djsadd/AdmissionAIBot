const { v4: uuidv4 } = require('uuid');
const axios = require('axios');

async function testAskAI() {
    try {
        const response = await axios.post('http://192.168.115.194:8000/ask_ai/', {
            uuid: uuidv4(), // добавлен uuid
            query: 'В чем ваше преисущество перед другими университетами?',
            platform: 'Whatsapp'
        });

        console.log('✅ Ответ от сервера:', response.data);

    } catch (error) {
        if (error.response) {
            console.error('❌ Ответ с ошибкой от сервера:', error.response.data);
        } else {
            console.error('❌ Ошибка при запросе:', error.message);
        }
    }
}

testAskAI();