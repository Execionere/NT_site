import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    vus: 2, // 1 виртуальный пользователь
    duration: '10m', // Длительность теста 10 минут
};

export default function () {
    const url = 'http://192.168.3.17:5000/users'; // URL вашего API
    const response = http.get(url);

    // Проверяем, что ответ успешный (код 200)
    check(response, {
        'is status 200': (r) => r.status === 200,
        'response time < 200ms': (r) => r.timings.duration < 200,
    });

    // Выводим ответ в консоль
    console.log('Response body: ' + response.body);

    sleep(1); // Ждем 1 секунду перед следующим запросом
}
