const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');
const { v4: uuidv4 } = require('uuid');

// Настройки
const RATE_LIMIT_MS = 10000; // 10 секунд
const UUID_UPDATE_INTERVAL = 60 * 60 * 1000; // 1 час
const MESSAGE_LIMIT = 5; // Каждые 5 сообщений

// Хранилища состояния
const lastRequestTime = {}; // Последнее время запроса от пользователя
const userData = {}; // Информация по пользователю: UUID, время обновления, счетчик сообщений

// Инициализация WhatsApp клиента
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: false,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

// Генерация QR кода
client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
});

// Готовность бота
client.on('ready', () => {
    console.log('✅ Бот подключен и готов к работе!');
});

// Обработка сообщений
client.on('message', async (message) => {
    const sender = message.from;
    const now = Date.now();

    if (sender.endsWith('@g.us')) return; // Игнорируем групповые чаты

    // Инициализация данных пользователя
    if (!userData[sender]) {
        userData[sender] = {
            uuid: uuidv4(),
            lastUpdated: now,
            messageCount: 0
        };
    }

    const user = userData[sender];

    // Проверка необходимости обновления UUID
    const shouldUpdateUUID =
        (now - user.lastUpdated >= UUID_UPDATE_INTERVAL) || (user.messageCount >= MESSAGE_LIMIT);

    if (shouldUpdateUUID) {
        user.uuid = uuidv4();
        user.lastUpdated = now;
        user.messageCount = 0;
        console.log(`🔄 Обновлен UUID для ${sender}: ${user.uuid}`);
    }

    // Проверка лимита запросов по времени
    if (lastRequestTime[sender] && (now - lastRequestTime[sender]) < RATE_LIMIT_MS) {
        const remaining = ((RATE_LIMIT_MS - (now - lastRequestTime[sender])) / 1000).toFixed(1);
        await message.reply(`⏱ Подождите ${remaining} секунд перед следующим вопросом.`);
        return;
    }

    // Обновление состояния
    lastRequestTime[sender] = now;
    user.messageCount += 1;

    console.log(`📩 Запрос от ${sender}: ${message.body} (UUID: ${user.uuid})`);

    // Запрос к FastAPI серверу
    try {
        const response = await axios.post('http://127.0.0.1:8000/ask_ai/', {
            query: message.body,
            platform: 'Whatsapp',
            uuid: user.uuid
        });

        const aiReply = response.data.answer;
        await message.reply(`Вам ответил искуственный интеллект, чтобы уточнить вопрос позвоните консультанту по этому же номеру. 🤖Ответ ИИ ${aiReply}.`);
    } catch (error) {
        if (error.response) {
            console.error('❌ Ошибка ответа от сервера:', error.response.data);
        } else {
            console.error('❌ Ошибка соединения с сервером:', error.message);
        }
        await message.reply('⚠️ Ошибка при обращении к серверу. Попробуйте позже.');
    }
});

// Запуск клиента
client.initialize();
