// DOM Elements
const elements = {
  taskInput: document.getElementById('task-input'),
  addTaskBtn: document.getElementById('add-task-btn'),
  aiPrioritizeBtn: document.getElementById('ai-prioritize-btn'),
  authBtn: document.getElementById('auth-btn'),
  tasksContainer: document.getElementById('tasks-container'),
  scheduleBtn: document.getElementById('schedule-btn'),
  emailBtn: document.getElementById('email-btn'),
  searchBtn: document.getElementById('search-btn'),
  statusIndicator: document.createElement('div')
};

class PopupUI {
  constructor() {
    this.taskManager = window.taskManager || new TaskManager();
    this.setupUI().catch(console.error);
  }

  async setupUI() {
    elements.statusIndicator.className = 'status-indicator';
    document.body.appendChild(elements.statusIndicator);
    this.setupEventListeners();
    await this.updateAuthStatus();
    await this.renderTasks();
  }

  setupEventListeners() {
    // Task management
    elements.addTaskBtn.addEventListener('click', () => this.handleAddTask());
    elements.taskInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') this.handleAddTask();
    });

    // AI actions
    elements.aiPrioritizeBtn.addEventListener('click', async () => {
      this.showStatus('Prioritizing tasks...');
      await chrome.runtime.sendMessage({ action: 'prioritizeTasks' });
      this.showStatus('Tasks prioritized!', 2000);
    });

    // Quick actions
    elements.scheduleBtn.addEventListener('click', async () => {
      this.showStatus('Scheduling to calendar...');
      await chrome.runtime.sendMessage({ action: 'scheduleTasks' });
      this.showStatus('Tasks scheduled!', 2000);
    });

    elements.emailBtn.addEventListener('click', () => {
      chrome.runtime.sendMessage({ action: 'draft_email' });
      this.showStatus('Opening email draft...', 2000);
    });

    elements.searchBtn.addEventListener('click', () => {
      const query = elements.taskInput.value.trim();
      if (query) chrome.runtime.sendMessage({ action: 'web_search', query });
    });

    // Auth button
    elements.authBtn.addEventListener('click', () => this.handleAuth());
  }

  async handleAddTask() {
    const text = elements.taskInput.value.trim();
    if (text) {
      this.showStatus('Adding task...');
      await chrome.runtime.sendMessage({ 
        action: 'addTask', 
        text 
      });
      elements.taskInput.value = '';
      this.showStatus('Task added!', 1500);
    }
  }

  async handleAuth() {
    this.showStatus('Authenticating...');
    const token = await new Promise(resolve => {
      chrome.identity.getAuthToken({ interactive: true }, resolve);
    });
    this.updateAuthStatus(!!token);
    this.showStatus(token ? 'Signed in!' : 'Sign-in failed', 2000);
  }

  async updateAuthStatus(forceAuthenticated) {
    const authenticated = forceAuthenticated ?? await new Promise(resolve => {
      chrome.identity.getAuthToken({ interactive: false }, (token) => {
        resolve(!!token);
      });
    });
    elements.authBtn.textContent = authenticated ? 'Signed In' : 'Sign In';
    elements.authBtn.className = authenticated ? 'auth-button signed-in' : 'auth-button';
  }
// GET
  async renderTasks() {
    const { tasks } = await chrome.storage.sync.get('tasks');
    elements.tasksContainer.innerHTML = '';
    (tasks || []).forEach(task => {
      const taskEl = document.createElement('div');
      taskEl.className = `task-item priority-${task.priority || 'medium'}`;
      taskEl.innerHTML = `
        <span class="task-text">${task.text}</span>
        <span class="task-priority">${task.priority || ''}</span>
      `;
      elements.tasksContainer.appendChild(taskEl);
    });
  }

  showStatus(message, duration = 0) {
    elements.statusIndicator.textContent = message;
    elements.statusIndicator.style.display = 'block';
    if (duration > 0) {
      setTimeout(() => {
        elements.statusIndicator.style.display = 'none';
      }, duration);
    }
  }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  new PopupUI();
});