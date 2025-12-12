// Главный файл приложения с логикой интерфейса

// Глобальное состояние
let currentEmployees = [];
let currentResources = [];
let currentBookings = [];

// ==================== Инициализация ====================

document.addEventListener('DOMContentLoaded', async () => {
    console.log('Приложение загружено');

    // Загружаем начальные данные
    await loadInitialData();

    // Загружаем бронирования
    await loadAllBookings();
});

// Загрузка начальных данных
async function loadInitialData() {
    try {
        [currentEmployees, currentResources] = await Promise.all([
            api.employees.getAll(),
            api.resources.getAll(),
        ]);

        // Заполняем фильтры
        populateFilters();
    } catch (error) {
        showError('Ошибка загрузки данных: ' + error.message);
        // Показываем уведомление
        alert('Не удалось загрузить данные с сервера. Убедитесь, что бэкенд запущен на порту 8000.\n\nПодробности: ' + error.message);
    }
}

// ==================== Навигация по вкладкам ====================

function showTab(tabName) {
    // Скрываем все секции
    document.querySelectorAll('.tab-content').forEach(section => {
        section.classList.remove('active');
    });

    // Убираем активный класс со всех кнопок
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });

    // Показываем выбранную секцию
    const section = document.getElementById(`${tabName}-section`);
    if (section) {
        section.classList.add('active');
    }

    // Активируем соответствующую кнопку
    event.target.classList.add('active');

    // Загружаем данные для секции
    switch (tabName) {
        case 'bookings':
            loadAllBookings();
            break;
        case 'resources':
            loadResources();
            break;
        case 'employees':
            loadEmployees();
            break;
        case 'reports':
            // Отчеты загружаются по нажатию кнопки
            break;
    }
}

// ==================== Бронирования ====================

async function loadAllBookings() {
    try {
        currentBookings = await api.bookings.getAll();
        renderBookingsTable(currentBookings);
    } catch (error) {
        showError('Ошибка загрузки бронирований: ' + error.message);
    }
}

async function loadTodayBookings() {
    try {
        currentBookings = await api.bookings.getToday();
        renderBookingsTable(currentBookings);
    } catch (error) {
        showError('Ошибка загрузки бронирований: ' + error.message);
    }
}

async function filterByResource() {
    const resourceId = document.getElementById('resourceFilter').value;
    if (!resourceId) {
        await loadAllBookings();
        return;
    }

    try {
        currentBookings = await api.bookings.getByResource(resourceId);
        renderBookingsTable(currentBookings);
    } catch (error) {
        showError('Ошибка фильтрации: ' + error.message);
    }
}

async function filterByEmployee() {
    const employeeId = document.getElementById('employeeFilter').value;
    if (!employeeId) {
        await loadAllBookings();
        return;
    }

    try {
        currentBookings = await api.bookings.getByEmployee(employeeId);
        renderBookingsTable(currentBookings);
    } catch (error) {
        showError('Ошибка фильтрации: ' + error.message);
    }
}

function renderBookingsTable(bookings) {
    const tbody = document.getElementById('bookingsTableBody');

    if (bookings.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="empty-state">Нет бронирований</td></tr>';
        return;
    }

    tbody.innerHTML = bookings.map(booking => `
        <tr>
            <td>${booking.id}</td>
            <td>${booking.resource?.name || 'N/A'}</td>
            <td>${booking.employee?.full_name || 'N/A'}</td>
            <td>${booking.date}</td>
            <td>${booking.start_time}</td>
            <td>${booking.end_time}</td>
            <td>
                <button class="btn btn-danger btn-small" onclick="deleteBooking(${booking.id})">Удалить</button>
            </td>
        </tr>
    `).join('');
}

// ==================== Ресурсы ====================

async function loadResources() {
    try {
        currentResources = await api.resources.getAll();
        renderResourcesTable(currentResources);
    } catch (error) {
        showError('Ошибка загрузки ресурсов: ' + error.message);
    }
}

function renderResourcesTable(resources) {
    const tbody = document.getElementById('resourcesTableBody');

    if (resources.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="empty-state">Нет ресурсов</td></tr>';
        return;
    }

    tbody.innerHTML = resources.map(resource => `
        <tr>
            <td>${resource.id}</td>
            <td>${resource.name}</td>
            <td>${resource.type}</td>
            <td>${resource.capacity || 'N/A'}</td>
            <td>
                <button class="btn btn-danger btn-small" onclick="deleteResource(${resource.id})">Удалить</button>
            </td>
        </tr>
    `).join('');
}

// ==================== Сотрудники ====================

async function loadEmployees() {
    try {
        currentEmployees = await api.employees.getAll();
        renderEmployeesTable(currentEmployees);
    } catch (error) {
        showError('Ошибка загрузки сотрудников: ' + error.message);
    }
}

function renderEmployeesTable(employees) {
    const tbody = document.getElementById('employeesTableBody');

    if (employees.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="empty-state">Нет сотрудников</td></tr>';
        return;
    }

    tbody.innerHTML = employees.map(employee => `
        <tr>
            <td>${employee.id}</td>
            <td>${employee.full_name}</td>
            <td>${employee.email}</td>
            <td>
                <button class="btn btn-danger btn-small" onclick="deleteEmployee(${employee.id})">Удалить</button>
            </td>
        </tr>
    `).join('');
}

// ==================== Отчеты ====================

async function loadResourceUsageReport() {
    try {
        const report = await api.reports.getResourceUsage();
        renderReportTable(report);
    } catch (error) {
        showError('Ошибка загрузки отчета: ' + error.message);
    }
}

function renderReportTable(report) {
    const tbody = document.getElementById('reportTableBody');

    if (report.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" class="empty-state">Нет данных</td></tr>';
        return;
    }

    tbody.innerHTML = report.map(item => `
        <tr>
            <td>${item.resource_id}</td>
            <td>${item.resource_name}</td>
            <td>${item.total_hours.toFixed(2)} ч</td>
        </tr>
    `).join('');
}

// ==================== Формы ====================

function showCreateBookingForm() {
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>Новое бронирование</h2>
        <form id="bookingForm" onsubmit="handleCreateBooking(event)">
            <div class="form-group">
                <label>Ресурс</label>
                <select name="resource_id" required>
                    <option value="">Выберите ресурс</option>
                    ${currentResources.map(r => `<option value="${r.id}">${r.name}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>Сотрудник</label>
                <select name="employee_id" required>
                    <option value="">Выберите сотрудника</option>
                    ${currentEmployees.map(e => `<option value="${e.id}">${e.full_name}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>Дата</label>
                <input type="date" name="date" required>
            </div>
            <div class="form-group">
                <label>Время начала</label>
                <input type="time" name="start_time" required>
            </div>
            <div class="form-group">
                <label>Время окончания</label>
                <input type="time" name="end_time" required>
            </div>
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Отмена</button>
                <button type="submit" class="btn btn-primary">Создать</button>
            </div>
        </form>
    `;
    openModal();
}

function showCreateResourceForm() {
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>Новый ресурс</h2>
        <form id="resourceForm" onsubmit="handleCreateResource(event)">
            <div class="form-group">
                <label>Название</label>
                <input type="text" name="name" required>
            </div>
            <div class="form-group">
                <label>Тип</label>
                <input type="text" name="type" required placeholder="комната, проектор и т.д.">
            </div>
            <div class="form-group">
                <label>Вместимость</label>
                <input type="number" name="capacity" min="0">
            </div>
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Отмена</button>
                <button type="submit" class="btn btn-primary">Создать</button>
            </div>
        </form>
    `;
    openModal();
}

function showCreateEmployeeForm() {
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>Новый сотрудник</h2>
        <form id="employeeForm" onsubmit="handleCreateEmployee(event)">
            <div class="form-group">
                <label>ФИО</label>
                <input type="text" name="full_name" required>
            </div>
            <div class="form-group">
                <label>Email</label>
                <input type="email" name="email" required>
            </div>
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Отмена</button>
                <button type="submit" class="btn btn-primary">Создать</button>
            </div>
        </form>
    `;
    openModal();
}

// ==================== Обработчики форм ====================

async function handleCreateBooking(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {
        resource_id: parseInt(formData.get('resource_id')),
        employee_id: parseInt(formData.get('employee_id')),
        date: formData.get('date'),
        start_time: formData.get('start_time'),
        end_time: formData.get('end_time'),
    };

    try {
        await api.bookings.create(data);
        showSuccess('Бронирование создано');
        closeModal();
        await loadAllBookings();
    } catch (error) {
        showError('Ошибка создания бронирования: ' + error.message);
    }
}

async function handleCreateResource(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {
        name: formData.get('name'),
        type: formData.get('type'),
        capacity: formData.get('capacity') ? parseInt(formData.get('capacity')) : null,
    };

    try {
        await api.resources.create(data);
        showSuccess('Ресурс создан');
        closeModal();
        await loadInitialData();
        await loadResources();
    } catch (error) {
        showError('Ошибка создания ресурса: ' + error.message);
    }
}

async function handleCreateEmployee(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {
        full_name: formData.get('full_name'),
        email: formData.get('email'),
    };

    try {
        await api.employees.create(data);
        showSuccess('Сотрудник создан');
        closeModal();
        await loadInitialData();
        await loadEmployees();
    } catch (error) {
        showError('Ошибка создания сотрудника: ' + error.message);
    }
}

// ==================== Удаление ====================

async function deleteBooking(id) {
    if (!confirm('Вы уверены, что хотите удалить это бронирование?')) return;

    try {
        await api.bookings.delete(id);
        showSuccess('Бронирование удалено');
        await loadAllBookings();
    } catch (error) {
        showError('Ошибка удаления: ' + error.message);
    }
}

async function deleteResource(id) {
    if (!confirm('Вы уверены, что хотите удалить этот ресурс?')) return;

    try {
        await api.resources.delete(id);
        showSuccess('Ресурс удален');
        await loadInitialData();
        await loadResources();
    } catch (error) {
        showError('Ошибка удаления: ' + error.message);
    }
}

async function deleteEmployee(id) {
    if (!confirm('Вы уверены, что хотите удалить этого сотрудника?')) return;

    try {
        await api.employees.delete(id);
        showSuccess('Сотрудник удален');
        await loadInitialData();
        await loadEmployees();
    } catch (error) {
        showError('Ошибка удаления: ' + error.message);
    }
}

// ==================== Модальное окно ====================

function openModal() {
    document.getElementById('modal').classList.add('active');
}

function closeModal() {
    document.getElementById('modal').classList.remove('active');
}

// Закрытие по клику вне модального окна
window.onclick = function (event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        closeModal();
    }
};

// ==================== Утилиты ====================

function populateFilters() {
    // Заполняем фильтр ресурсов
    const resourceFilter = document.getElementById('resourceFilter');
    resourceFilter.innerHTML = '<option value="">Все ресурсы</option>' +
        currentResources.map(r => `<option value="${r.id}">${r.name}</option>`).join('');

    // Заполняем фильтр сотрудников
    const employeeFilter = document.getElementById('employeeFilter');
    employeeFilter.innerHTML = '<option value="">Все сотрудники</option>' +
        currentEmployees.map(e => `<option value="${e.id}">${e.full_name}</option>`).join('');
}

function showSuccess(message) {
    alert('✓ ' + message);
}

function showError(message) {
    alert('✗ ' + message);
}

function showConnectionBanner() {
    const banner = document.getElementById('connectionBanner');
    if (banner) {
        banner.style.display = 'block';
    }
}

function hideConnectionBanner() {
    const banner = document.getElementById('connectionBanner');
    if (banner) {
        banner.style.display = 'none';
    }
}
