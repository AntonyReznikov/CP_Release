// API клиент для взаимодействия с backend
const API_BASE_URL = 'http://127.0.0.1:8000';

// Утилита для выполнения HTTP запросов
async function fetchAPI(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;

    const config = {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
    };

    try {
        const response = await fetch(url, config);

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(error.detail || `HTTP error! status: ${response.status}`);
        }

        // Для DELETE запросов с 204 No Content
        if (response.status === 204) {
            return null;
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);

        // Более понятные сообщения об ошибках
        if (error.message.includes('Failed to fetch') || error.name === 'TypeError') {
            throw new Error('Не удается подключиться к серверу. Убедитесь, что Backend запущен на http://127.0.0.1:8000 и откройте Frontend через HTTP сервер (запустите start_frontend.bat)');
        }

        throw error;
    }
}

// ==================== Employees API ====================

const employeesAPI = {
    // Получить всех сотрудников
    getAll: () => fetchAPI('/employees/'),

    // Получить сотрудника по ID
    getById: (id) => fetchAPI(`/employees/${id}`),

    // Создать нового сотрудника
    create: (data) => fetchAPI('/employees/', {
        method: 'POST',
        body: JSON.stringify(data),
    }),

    // Обновить сотрудника
    update: (id, data) => fetchAPI(`/employees/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
    }),

    // Удалить сотрудника
    delete: (id) => fetchAPI(`/employees/${id}`, {
        method: 'DELETE',
    }),
};

// ==================== Resources API ====================

const resourcesAPI = {
    // Получить все ресурсы
    getAll: () => fetchAPI('/resources/'),

    // Получить ресурс по ID
    getById: (id) => fetchAPI(`/resources/${id}`),

    // Создать новый ресурс
    create: (data) => fetchAPI('/resources/', {
        method: 'POST',
        body: JSON.stringify(data),
    }),

    // Обновить ресурс
    update: (id, data) => fetchAPI(`/resources/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
    }),

    // Удалить ресурс
    delete: (id) => fetchAPI(`/resources/${id}`, {
        method: 'DELETE',
    }),
};

// ==================== Bookings API ====================

const bookingsAPI = {
    // Получить все бронирования
    getAll: () => fetchAPI('/bookings/'),

    // Получить бронирование по ID
    getById: (id) => fetchAPI(`/bookings/${id}`),

    // Получить бронирования на сегодня
    getToday: () => fetchAPI('/bookings/today'),

    // Получить бронирования по ресурсу
    getByResource: (resourceId) => fetchAPI(`/bookings/by_resource/${resourceId}`),

    // Получить бронирования по сотруднику
    getByEmployee: (employeeId) => fetchAPI(`/bookings/by_employee/${employeeId}`),

    // Создать новое бронирование
    create: (data) => fetchAPI('/bookings/', {
        method: 'POST',
        body: JSON.stringify(data),
    }),

    // Обновить бронирование
    update: (id, data) => fetchAPI(`/bookings/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
    }),

    // Удалить бронирование
    delete: (id) => fetchAPI(`/bookings/${id}`, {
        method: 'DELETE',
    }),
};

// ==================== Reports API ====================

const reportsAPI = {
    // Получить отчет по загрузке ресурсов
    getResourceUsage: () => fetchAPI('/bookings/report/resource_usage'),
};

// Экспортируем API модули
window.api = {
    employees: employeesAPI,
    resources: resourcesAPI,
    bookings: bookingsAPI,
    reports: reportsAPI,
};
