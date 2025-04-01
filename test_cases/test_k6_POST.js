import http from 'k6/http';
import { check, sleep } from 'k6';
import { parse } from 'https://jslib.k6.io/papaparse/5.1.1/index.js';

const csvParamsFile = parse(open('./params.csv'), { header: true }).data;
csvParamsFile.forEach(item => {
    Object.keys(item).forEach(key => {
        const newKey = key.trim(); // Удаляем пробельные символы
        if (newKey !== key) {
            item[newKey] = item[key];
            delete item[key];
        }
    });
});
console.log(csvParamsFile);

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
            ],
        }
    }
}
export default function () {
    const currentParamsFileData = csvParamsFile[__ITER % csvParamsFile.length];
    console.log(`Отправляем значение: ${currentParamsFileData['test_data_value']}`);

    const url = 'http://192.168.3.17:5000/data_add';
    const new_uuid = Math.random().toString(36).substring(2, 15); // Генерация случайного UUID
    const payload = JSON.stringify({
        uuid: new_uuid,
        test_data_string: currentParamsFileData.test_data_value
    });

    // Определяем заголовки
    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    // Отправляем POST-запрос
    const response = http.post(url, payload, params);

    // Выводим ответ в консоль
    console.log('Response body: ' + response.body);
}
