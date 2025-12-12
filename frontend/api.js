// API клиент для взаимодействия с backend
const API_BASE_URL = '';  // Фронтенд и бэкенд на одном домене

// Утилита для выполнения HTTP запросов
async function fetchAPI(endpoint, options = {}) {
    // Если endpoint не начинается с /, добавляем его
    if (!endpoint.startsWith('/')) {
        endpoint = '/' + endpoint;
    }
    
    const url = `${API_BASE_URL}${endpoint}`;
    console.log('API Request:', url, options);

    const config = {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
    };

    try {
        const response = await fetch(url, config);
        console.log('API Response:', response.status, response.url, response.headers.get('content-type'));
        
        // Если это перенаправление на index.html, игнорируем его
        if (response.url.includes('/index.html') && response.redirected) {
            console.warn('Redirected to index.html - SPA routing');
            return null;
        }
        
        // Для пустого ответа (204) возвращаем null
        if (response.status === 204) {
            return null;
        }
        
        // Проверяем content-type
        const contentType = response.headers.get("content-type") || '';
        
        // Если это не JSON
        if (!contentType.includes("application/json")) {
            const text = await response.text();
            console.error('Not JSON response:', text.substring(0, 500));
            
            // Если это ошибка (status не 2xx)
            if (!response.ok) {
                // Пытаемся извлечь информацию из текста ошибки
                let errorDetail = text;
                // Если текст слишком длинный, обрезаем
                if (errorDetail.length > 200) {
                    errorDetail = errorDetail.substring(0, 200) + '...';
                }
                throw new Error(`HTTP ${response.status}: ${errorDetail}`);
            }
            
            // Если это не ошибка, но и не JSON
            throw new Error(`Expected JSON but got: ${contentType}`);
        }
        
        // Обработка JSON ответа
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || `HTTP error! status: ${response.status}`);
        }

        console.log('API Success:', data);
        return data;
    } catch (error) {
        console.error('API Error:', error.message);
        throw error;
    }
}

// ==================== Employees API ====================

const employeesAPI = {
    getAll: () => fetchAPI('/employees/'),
    getById: (id) => fetchAPI(`/employees/${id}`),
    create: (data) => fetchAPI('/employees/', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    update: (id, data) => fetchAPI(`/employees/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
    }),
    delete: (id) => fetchAPI(`/employees/${id}`, {
        method: 'DELETE',
    }),
};

// ==================== Resources API ====================

const resourcesAPI = {
    getAll: () => fetchAPI('/resources/'),
    getById: (id) => fetchAPI(`/resources/${id}`),
    create: (data) => fetchAPI('/resources/', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    update: (id, data) => fetchAPI(`/resources/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
    }),
    delete: (id) => fetchAPI(`/resources/${id}`, {
        method: 'DELETE',
    }),
};

// ==================== Bookings API ====================

const bookingsAPI = {
    getAll: () => fetchAPI('/bookings/'),
    getById: (id) => fetchAPI(`/bookings/${id}`),
    getToday: () => fetchAPI('/bookings/today'),
    getByResource: (resourceId) => fetchAPI(`/bookings/by_resource/${resourceId}`),
    getByEmployee: (employeeId) => fetchAPI(`/bookings/by_employee/${employeeId}`),
    create: (data) => fetchAPI('/bookings/', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    update: (id, data) => fetchAPI(`/bookings/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
    }),
    delete: (id) => fetchAPI(`/bookings/${id}`, {
        method: 'DELETE',
    }),
};

// ==================== Reports API ====================

const reportsAPI = {
    getResourceUsage: () => fetchAPI('/bookings/report/resource_usage'),
};

// Экспортируем API модули
window.api = {
    employees: employeesAPI,
    resources: resourcesAPI,
    bookings: bookingsAPI,
    reports: reportsAPI,
};