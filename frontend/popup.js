// Status message helper
function showStatus(message, isError = false) {
  const statusEl = document.getElementById('status-indicator');
  statusEl.textContent = message;
  statusEl.classList.add('visible');
  
  if (isError) {
    statusEl.style.backgroundColor = 'var(--error)';
  } else {
    statusEl.style.backgroundColor = 'var(--primary)';
  }
  
  setTimeout(() => {
    statusEl.classList.remove('visible');
  }, 3000);
}

// Authentication state manager
class AuthManager {
  constructor() {
    this.isAuthenticated = false;
    this.userInfo = null;
    this.authButton = document.getElementById('auth-btn');
    this.authText = this.authButton.querySelector('.auth-text');
    this.authStatus = this.authButton.querySelector('.auth-status');
    
    // Initialize auth state
    this.init();
    
    // Set up event listeners
    this.authButton.addEventListener('click', () => this.handleAuthClick());
  }
  
  async init() {
    // Check if user is already authenticated
    try {
      const token = await this.getAuthToken(false); // non-interactive check
      if (token) {
        await this.getUserInfo(token);
        this.setAuthenticatedState(true);
      } else {
        this.setAuthenticatedState(false);
      }
    } catch (error) {
      console.error('Auth init error:', error);
      this.setAuthenticatedState(false);
    }
  }
  
  setAuthenticatedState(isAuthenticated) {
    this.isAuthenticated = isAuthenticated;
    
    if (isAuthenticated) {
      this.authButton.classList.add('signed-in');
      this.authText.textContent = 'Signed In';
      this.authStatus.textContent = '✓';
      
      // Enable UI elements
      document.getElementById('task-input').disabled = false;
      document.getElementById('add-task-btn').disabled = false;
      document.getElementById('ai-prioritize-btn').disabled = false;
      document.getElementById('schedule-btn').disabled = false;
      document.getElementById('email-btn').disabled = false;
      document.getElementById('search-btn').disabled = false;
      
      showStatus('Connected to Google Calendar');
    } else {
      this.authButton.classList.remove('signed-in');
      this.authText.textContent = 'Sign In';
      this.authStatus.textContent = '';
      
      // Disable calendar-dependent features
      document.getElementById('schedule-btn').disabled = true;
      
      // Note: We don't disable task input as users might want to add tasks
      // without calendar integration
    }
  }
  
  async handleAuthClick() {
    if (this.isAuthenticated) {
      // Sign out
      await this.signOut();
    } else {
      // Sign in
      await this.signIn();
    }
  }
  
  async signIn() {
    try {
      this.authButton.disabled = true;
      this.authText.textContent = 'Signing in...';
      
      const token = await this.getAuthToken(true); // interactive
      if (token) {
        await this.getUserInfo(token);
        this.setAuthenticatedState(true);
        showStatus('Successfully signed in');
      }
    } catch (error) {
      console.error('Sign in error:', error);
      showStatus('Failed to sign in', true);
    } finally {
      this.authButton.disabled = false;
    }
  }
  
  async signOut() {
    try {
      this.authButton.disabled = true;
      this.authText.textContent = 'Signing out...';
      
      // Get current token
      const token = await this.getAuthToken(false);
      if (token) {
        // Remove the token from Chrome's cache
        await new Promise((resolve) => {
          chrome.identity.removeCachedAuthToken({ token }, resolve);
        });
      }
      
      this.setAuthenticatedState(false);
      this.userInfo = null;
      showStatus('Signed out successfully');
    } catch (error) {
      console.error('Sign out error:', error);
      showStatus('Failed to sign out', true);
    } finally {
      this.authButton.disabled = false;
    }
  }
  
  async getAuthToken(interactive = false) {
    return new Promise((resolve, reject) => {
      chrome.identity.getAuthToken({ 
        interactive: interactive,
        scopes: ['https://www.googleapis.com/auth/calendar']
      }, (token) => {
        if (chrome.runtime.lastError) {
          console.error('Auth token error:', chrome.runtime.lastError);
          reject(chrome.runtime.lastError);
        } else {
          resolve(token);
        }
      });
    });
  }
  
  async getUserInfo(token) {
    try {
      const response = await fetch('https://www.googleapis.com/oauth2/v2/userinfo', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        throw new Error(`Failed to get user info: ${response.status}`);
      }
      
      this.userInfo = await response.json();
      console.log('User info:', this.userInfo);
    } catch (error) {
      console.error('Get user info error:', error);
    }
  }
}

// Task Manager that communicates with the background script
class TaskManager {
  constructor() {
    this.tasks = [];
    this.taskInput = document.getElementById('task-input');
    this.addTaskButton = document.getElementById('add-task-btn');
    this.tasksContainer = document.getElementById('tasks-container');
    this.taskCount = document.getElementById('task-count');
    this.prioritizeButton = document.getElementById('ai-prioritize-btn');
    this.scheduleButton = document.getElementById('schedule-btn');
    
    // Initialize event listeners
    this.init();
  }
  
  init() {
    // Load tasks on popup open
    this.loadTasks();
    
    // Add task event
    this.addTaskButton.addEventListener('click', () => this.addTask());
    
    // Handle enter key in textarea
    this.taskInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.addTask();
      }
    });
    
    // Prioritize button
    this.prioritizeButton.addEventListener('click', () => this.prioritizeTasks());
    
    // Schedule to calendar button
    this.scheduleButton.addEventListener('click', () => this.scheduleTasks());
    
    // Listen for task updates from background
    chrome.runtime.onMessage.addListener((message) => {
      if (message.type === 'tasks_updated') {
        this.tasks = message.tasks;
        this.renderTasks();
      }
    });
  }
  
  async loadTasks() {
    return new Promise((resolve) => {
      chrome.storage.sync.get(['tasks'], (result) => {
        this.tasks = result.tasks || [];
        this.renderTasks();
        resolve();
      });
    });
  }
  
  async addTask() {
    const taskText = this.taskInput.value.trim();
    if (!taskText) return;
    
    try {
      // Extract priority from hashtags if present
      let priority = 'medium';
      if (taskText.includes('#high')) priority = 'high';
      if (taskText.includes('#medium')) priority = 'medium';
      if (taskText.includes('#low')) priority = 'low';
      
      // Clean text by removing hashtags
      const cleanText = taskText
        .replace(/#high/g, '')
        .replace(/#medium/g, '')
        .replace(/#low/g, '')
        .trim();
      
      const response = await chrome.runtime.sendMessage({
        action: 'add_task',
        text: cleanText,
        priority: priority
      });
      
      if (response && response.success) {
        this.taskInput.value = '';
        this.loadTasks(); // Refresh task list
        showStatus('Task added');
      } else {
        showStatus('Failed to add task', true);
      }
    } catch (error) {
      console.error('Add task error:', error);
      showStatus('Error adding task', true);
    }
  }
  
  async deleteTask(taskId) {
    try {
      const response = await chrome.runtime.sendMessage({
        action: 'delete_task',
        taskId: taskId
      });
      
      if (response && response.success) {
        this.loadTasks(); // Refresh task list
        showStatus('Task deleted');
      } else {
        showStatus('Failed to delete task', true);
      }
    } catch (error) {
      console.error('Delete task error:', error);
      showStatus('Error deleting task', true);
    }
  }
  
  async prioritizeTasks() {
    if (this.tasks.length === 0) {
      showStatus('No tasks to prioritize');
      return;
    }
    
    try {
      this.prioritizeButton.disabled = true;
      showStatus('Prioritizing tasks...');
      
      const response = await chrome.runtime.sendMessage({
        action: 'prioritize_tasks'
      });
      
      if (response && response.success) {
        this.loadTasks(); // Refresh task list
        showStatus('Tasks prioritized');
      } else {
        showStatus('Failed to prioritize tasks', true);
      }
    } catch (error) {
      console.error('Prioritize tasks error:', error);
      showStatus('Error prioritizing tasks', true);
    } finally {
      this.prioritizeButton.disabled = false;
    }
  }
  
  async scheduleTasks() {
    if (this.tasks.length === 0) {
      showStatus('No tasks to schedule');
      return;
    }
    
    if (!authManager.isAuthenticated) {
      showStatus('Please sign in first', true);
      return;
    }
    
    try {
      this.scheduleButton.disabled = true;
      showStatus('Scheduling to calendar...');
      
      const response = await chrome.runtime.sendMessage({
        action: 'schedule_all_tasks'
      });
      
      if (response && response.success) {
        this.tasks = response.tasks;
        this.renderTasks();
        showStatus('Tasks scheduled to calendar');
      } else {
        showStatus('Failed to schedule tasks', true);
      }
    } catch (error) {
      console.error('Schedule tasks error:', error);
      showStatus('Error scheduling tasks', true);
    } finally {
      this.scheduleButton.disabled = false;
    }
  }
  
  async scheduleTask(taskId) {
    if (!authManager.isAuthenticated) {
      showStatus('Please sign in first', true);
      return;
    }
    
    try {
      showStatus('Scheduling task...');
      
      const response = await chrome.runtime.sendMessage({
        action: 'schedule_task',
        taskId: taskId
      });
      
      if (response && response.success) {
        this.loadTasks(); // Refresh task list
        showStatus('Task scheduled to calendar');
      } else {
        showStatus(response.error || 'Failed to schedule task', true);
      }
    } catch (error) {
      console.error('Schedule task error:', error);
      showStatus('Error scheduling task', true);
    }
  }
  
  renderTasks() {
    this.tasksContainer.innerHTML = '';
    this.taskCount.textContent = this.tasks.length;
    
    if (this.tasks.length === 0) {
      const emptyState = document.createElement('div');
      emptyState.className = 'empty-state';
      emptyState.textContent = 'No tasks yet. Add one above!';
      this.tasksContainer.appendChild(emptyState);
      return;
    }
    
    this.tasks.forEach(task => {
      const taskElement = document.createElement('div');
      taskElement.className = `task-item priority-${task.priority || 'medium'}`;
      
      const taskContent = document.createElement('div');
      taskContent.className = 'task-content';
      
      const taskText = document.createElement('div');
      taskText.className = 'task-text';
      taskText.textContent = task.text;
      
      const taskPriority = document.createElement('div');
      taskPriority.className = 'task-priority';
      taskPriority.textContent = task.priority || 'medium';
      
      taskContent.appendChild(taskText);
      taskContent.appendChild(taskPriority);
      
      const actionsContainer = document.createElement('div');
      actionsContainer.className = 'task-actions';
      
      // Calendar button (show checkmark if already scheduled)
      const calendarButton = document.createElement('button');
      calendarButton.className = 'task-action-btn';
      calendarButton.innerHTML = task.scheduled ? '✓' : '📅';
      calendarButton.title = task.scheduled ? 'Already scheduled' : 'Schedule to calendar';
      calendarButton.disabled = task.scheduled;
      calendarButton.addEventListener('click', () => this.scheduleTask(task.id));
      
      // Delete button
      const deleteButton = document.createElement('button');
      deleteButton.className = 'task-action-btn';
      deleteButton.innerHTML = '🗑️';
      deleteButton.title = 'Delete task';
      deleteButton.addEventListener('click', () => this.deleteTask(task.id));
      
      actionsContainer.appendChild(calendarButton);
      actionsContainer.appendChild(deleteButton);
      
      taskElement.appendChild(taskContent);
      taskElement.appendChild(actionsContainer);
      
      this.tasksContainer.appendChild(taskElement);
    });
  }
}

// Initialize managers
const authManager = new AuthManager();
const taskManager = new TaskManager();

// Extra CSS for task actions
const style = document.createElement('style');
style.textContent = `
  .task-content {
    flex: 1;
  }
  
  .task-actions {
    display: flex;
    gap: var(--space-sm);
  }
  
  .task-action-btn {
    background: none;
    border: none;
    cursor: pointer;
    font-size: var(--font-size-md);
    padding: var(--space-xs);
    border-radius: 50%;
    transition: background-color 0.2s;
  }
  
  .task-action-btn:hover {
    background-color: var(--secondary-dark);
  }
  
  .task-action-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .empty-state {
    text-align: center;
    color: var(--text-light);
    padding: var(--space-xl);
  }
`;
document.head.appendChild(style);