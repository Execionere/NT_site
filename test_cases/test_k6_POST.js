import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    scenarios: {
        ramping_test: {
            executor: 'ramping-arrival-rate',
            startRate: 1, // Начальная скорость запросов
            timeUnit: '1s', // Время для достижения целевой скорости
            preAllocatedVUs: 1, // Предварительно выделенные VUs
            stages: [
                { target: 2, duration: '1m' }, // Поддерживаем 1 RPS в течение первой минуты
                { target: 2, duration: '2m' }, // Увеличиваем до 2 RPS за одну минуту
                { target: 4, duration: '1m' }, // Поддерживаем 2 RPS в течение двух минут
                { target: 4, duration: '2m' }, // Увеличиваем до 4 RPS за одну минуту
                // { target: 4, duration: '2m' }, // Поддерживаем 4 RPS в течение двух минут
                // { target: 0, duration: '30s' }, // Останавливаем нагрузку за полминуты
            ],
            // stage_2: {
            //     executor: 'constant-arrival-rate',
            //     preAllocatedVUs: 10,
            //     maxVUs: 10,
            //     rate: 1,
            //     timeUnit: '1s',
            //     duration: '1m',
            // },
            // stage_3: {
            //     executor: 'constant-arrival-rate',
            //     preAllocatedVUs: 2,
            //     maxVUs: 2,
            //     rate: 1,
            //     timeUnit: '1s',
            //     duration: '1m',
            // }
        }
    }
}
export default function () {
    const url = 'http://192.168.3.17:5000/data_add'; // URL вашего API
    // Генерируем новый UUID
    const new_uuid = Math.random().toString(36).substring(2, 15); // Генерация случайного UUID

    // Создаем полезную нагрузку (payload)
    const payload = JSON.stringify({
        uuid: new_uuid,
        test_data_string: "Тестовая строка" // Фиксированное значение
    });

    // Определяем заголовки
    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    // Отправляем POST-запрос
    const response = http.post(url, payload, params);
    //
    // // Проверяем, что ответ успешный (код 200)
    // check(response, {
    //     'is status 200': (r) => r.status === 200,
    //     'response time < 200ms': (r) => r.timings.duration < 200,
    // });

    // Выводим ответ в консоль
    console.log('Response body: ' + response.body);
}
